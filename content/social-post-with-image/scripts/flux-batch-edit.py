#!/usr/bin/env python3
"""Flux Kontext batch edit: upload source, submit N graphs, poll history, download.

Usage:
    python3 flux-batch-edit.py <src-image> <graph1.json> [<graph2.json> ...]
    python3 flux-batch-edit.py --canvas 1024x1024 <graph1.json> [...]

--canvas WxH generates a solid dark canvas at that size instead of reading a
source file (for pure text-to-image: put the full design in the positive text).

Env:
    IMAGE_GEN_URL    required (ComfyUI base URL)
    IMAGE_GEN_OUT    download dir, default /tmp/image-gen
    IMAGE_GEN_POLL   total poll seconds, default 480

One call replaces the curl upload -> submit -> poll -> download loop.
stdlib only. Graphs must come from the known-good template
(templates/comfyui-kontext-edit.json) — expects node id `img0` = LoadImage and
reads the output name from the SaveImage node's filename_prefix.

Exit codes: 0 = all renders downloaded, 2 = some pending/errored (prompt_ids are
printed so renders can be resumed via GET /history/<id> without resubmitting).
"""
import json
import mimetypes
import os
import sys
import time
import urllib.parse
import urllib.request
import uuid
import zlib

BASE = os.environ.get("IMAGE_GEN_URL", "").rstrip("/")
OUT_DIR = os.environ.get("IMAGE_GEN_OUT", "/tmp/image-gen")
POLL_BUDGET = int(os.environ.get("IMAGE_GEN_POLL", "480"))
POLL_EVERY = 15


def die(msg):
    print("FATAL:", msg)
    sys.exit(1)


def http(url, data=None, headers=None, method=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def http_json(url, payload=None, method=None, timeout=60):
    if payload is not None:
        st, body = http(url, data=json.dumps(payload).encode(),
                        headers={"Content-Type": "application/json"},
                        method="POST", timeout=timeout)
    else:
        st, body = http(url, timeout=timeout)
    return st, json.loads(body)


def multipart_upload(path):
    boundary = uuid.uuid4().hex
    with open(path, "rb") as f:
        content = f.read()
    ctype = mimetypes.guess_type(path)[0] or "image/png"
    name = os.path.basename(path)
    parts = [
        ('--%s\r\nContent-Disposition: form-data; name="image"; filename="%s"\r\n'
         'Content-Type: %s\r\n\r\n' % (boundary, name, ctype)).encode(),
        content,
        ('\r\n--%s\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n'
         '--%s--\r\n' % (boundary, boundary)).encode(),
    ]
    st, resp = http("%s/upload/image" % BASE, data=b"".join(parts),
                    headers={"Content-Type": "multipart/form-data; boundary=%s" % boundary},
                    method="POST", timeout=180)
    return json.loads(resp)


def make_canvas(size, path):
    """Write a WxH solid dark-canvas PNG (stdlib only: zlib + struct, no PIL)."""
    w, h = (int(x) for x in size.lower().split("x"))
    # 8-bit RGB PNG, one row per filter-type-prefixed line
    raw = b"".join(b"\x00" + bytes((18, 18, 26)) * w for _ in range(h))

    def chunk(tag, data):
        c = tag + data
        return len(data).to_bytes(4, "big") + c + (zlib.crc32(c) & 0xFFFFFFFF).to_bytes(4, "big")

    ihdr = w.to_bytes(4, "big") + h.to_bytes(4, "big") + bytes((8, 2, 0, 0, 0))
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return path


def save_prefix(graph):
    for node in graph["prompt"].values():
        if node.get("class_type") == "SaveImage":
            return node["inputs"].get("filename_prefix", "edit")
    return "edit"


def history_result(pid):
    st, h = http_json("%s/history/%s" % (BASE, pid))
    if st != 200 or pid not in h:
        return None
    entry = h[pid]
    status = entry.get("status", {})
    if status.get("status_str") == "error":
        return {"error": json.dumps(status.get("messages", []))[:500]}
    for node in entry.get("outputs", {}).values():
        imgs = node.get("images")
        if imgs:
            im = imgs[0]
            return {"filename": im["filename"], "subfolder": im.get("subfolder", "")}
    return None


def download(filename, subfolder, dest):
    url = "%s/view?filename=%s&subfolder=%s&type=output" % (
        BASE, urllib.parse.quote(filename), urllib.parse.quote(subfolder))
    st, body = http(url, timeout=180)
    with open(dest, "wb") as f:
        f.write(body)
    return len(body)


def main():
    if not BASE:
        die("IMAGE_GEN_URL not set")
    args = sys.argv[1:]
    canvas_mode = "--canvas" in args
    size = None
    if canvas_mode:
        i = args.index("--canvas")
        size = args[i + 1]
        args = args[:i] + args[i + 2:]
    if len(args) < 1:
        die("usage: flux-batch-edit.py [--canvas WxH] <graph1.json> [...]  "
            "(or <src-image> <graph...> for edits)")
    if canvas_mode:
        os.makedirs(OUT_DIR, exist_ok=True)
        src = os.path.join(OUT_DIR, "canvas_%s.png" % str(size).replace("x", "_"))
        make_canvas(size, src)
        print("canvas: %s -> %s" % (size, src), flush=True)
    else:
        src, args = args[0], args[1:]
        if not os.path.exists(src):
            die("source image not found: %s" % src)
    graph_paths = args

    up = multipart_upload(src)
    upname = up.get("name")
    if not upname:
        die("upload failed: %s" % up)
    print("uploaded: %s -> %s" % (src, upname), flush=True)

    jobs = []  # (prompt_id, filename_prefix)
    for gp in graph_paths:
        with open(gp) as f:
            graph = json.load(f)
        graph["prompt"]["img0"]["inputs"]["image"] = upname
        prefix = save_prefix(graph)
        st, resp = http_json("%s/prompt" % BASE,
                             payload={"prompt": graph["prompt"], "client_id": "image-gen"})
        pid = resp.get("prompt_id")
        if st != 200 or not pid:
            die("submit %s failed: %s" % (gp, resp))
        jobs.append((pid, prefix))
        print("submitted %s: %s (prefix %s)" % (gp, pid, prefix), flush=True)

    deadline = time.time() + POLL_BUDGET
    pending = dict(jobs)
    done = {}
    while pending and time.time() < deadline:
        for pid in list(pending):
            info = history_result(pid)
            if info:
                done[pid] = (pending.pop(pid), info)
        if pending:
            time.sleep(POLL_EVERY)

    ok = True
    for pid, (prefix, info) in done.items():
        if "error" in info:
            ok = False
            print("%s: RENDER ERROR %s" % (prefix, info["error"]))
            continue
        dest = os.path.join(OUT_DIR, "%s.png" % prefix)
        n = download(info["filename"], info["subfolder"], dest)
        print("%s: saved %s (%d bytes) from %s" % (prefix, dest, n, info["filename"]))
    if pending:
        ok = False
        print("PENDING after %ds (resume via GET %s/history/<id>, do NOT resubmit):"
              % (POLL_BUDGET, BASE))
        for pid, prefix in pending.items():
            print("  %s = %s" % (prefix, pid))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
