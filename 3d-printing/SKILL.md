---
name: 3d-printing
description: >
  Programmatic CAD/mesh editing for 3D printing — modifying existing mesh models
  (STL/3MF) with trimesh + manifold3d: measuring real geometry, building fixture
  parts (flanges, enclosures, bolt bosses), boolean assembly, and printability
  checks. Use when a user asks to modify, extend, or enclose an existing 3D
  model, or to generate companion/printable parts around a scanned or provided
  mesh. No CAD software required.
---

# 3D Printing: Mesh-Based CAD Modifications

Workflow for taking an existing 3D model (STL/3MF — e.g. a downloaded design) and
adding or modifying geometry programmatically, without CAD software. Built from
the "Destaco clamp rack v8" enclosure project (Sep 2026): adding a bolt-on
enclosure tub + deck flanges to a bike rack by slicing and measuring the
original mesh, then building mating parts around it.

Toolchain: Python venv with `trimesh[manifold]` (booleans via manifold3d),
`numpy`, `matplotlib` (for rendering previews), `uv` to bootstrap.

Companion files in this directory:

- `case-study-rack-enclosure.md` — the full worked example with the 3-iteration
  clash-fix log and verification transcript. Read alongside SKILL.md on first use.
- `destaco-rack-reference.md` — measured geometry + mating-interface reference
  for the rack in the case study (reuse when returning to that project).

---

## Core Responsibilities

1. **Inspect before you touch.** Parse the original files, identify every part,
   its transform, orientation, units, and health (manifoldness, stray shells).
2. **Measure in a frame that makes sense.** Not the file's coordinate system —
   a derived "design frame" aligned with the part's functional axes.
3. **Design mating parts from measured data.** Wall positions, heights,
   clearances all read off the original mesh, never eyeballed.
4. **Verify with booleans, then render.** Prove non-intersection numerically;
   render orthographic previews as a visual check.
5. **Deliver print-ready artifacts.** Correct orientation for the printer,
   fastener specs, and fillet/overhang notes the slicer will care about.

---

## Workflow

### 1. Recon — parse the original files

- **STL** is a raw triangle soup with no metadata. Parse with `trimesh.load()`
  or numpy (`struct`) for binary STL. All parts already sit at build transforms.
- **3MF** is a ZIP: `3D/3dmodel.model` (XML, meshes by object id), `3D/Objects/
  *.model`, `Metadata/` (`project_settings.config` = printer/filament/layer
  settings; `cut_information.xml` = cut/parts layout; plate thumbnails).
  ```python
  from zipfile import ZipFile
  ZipFile('model.3mf').extractall('/tmp/extract/')
  # parse XML: <object id><mesh><vertices>/<triangles>
  # coordinates are in mm by 3MF spec
  ```
- Extract each part's mesh to `.npy` (vertices + face indices) once, then load
  arrays directly in later scripts. Re-parsing the XML/STL every time is slow.
- Read `project_settings.config` first: printer model, material, nozzle, layer
  height. These set constraints for everything downstream (bed size, material
  shrinkage, minimum features).

### 2. Mesh health check — before any modification

```python
import trimesh
m = trimesh.Trimesh(vertices=v, faces=f, process=False)
print(m.is_watertight, m.is_winding_consistent, m.volume)
```

- **Stray shells** (floaters, logo dots offset ~0.3 mm off surfaces) break
  booleans. Find them: `m.split(only_watertight=False)` → components whose
  volume is ~0 or that duplicate state of the main body. Delete them by
  rebuilding a mesh from the largest connected watertight component, or by
  keeping components with `len(comp.faces) > threshold`.
- **Duplicate coincident faces / self-intersections** — `trimesh.boolean` will
  still usually work (manifold3d is tolerant), but verify the boolean result is
  watertight and its volume is the *expected* sum. An unexpected volume = hidden
  mesh problems.
- If the file is non-manifold garbage, stop and tell the user. Don't hand-patch
  50k triangles.

### 3. Build a design frame

File coordinates are usually arbitrary. Derive a working frame aligned to the
part's function, then treat the mesh analytically:

```python
# example: find the big flat "deck" face by normal clustering
tris = v[f]
n = np.cross(tris[:,1]-tris[:,0], tris[:,2]-tris[:,0])
n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
# cluster by normal direction (round to 0.05 rad bins) and pick the cluster
# with the largest area; its plane offsets define the "floor" of your design
```

- Cluster faces by **normal direction × planar offset** to find walls, floors,
  rail tops, boss faces. The rack had its deck plane at a non-axis-aligned tilt
  (`normal (0.46, 0, 0.888)`), invisible in raw XYZ but obvious once clustered.
- Then define normalized coordinates: e.g. `u = distance along slope axis`,
  `y = across`, `w = height above floor plane`. All design dims become clean
  numbers against that frame, and constraint checks ("rail top", "inner wall y")
  are single query functions.

### 4. Measure everything you depend on

For each mating surface you plan to reference, measure from the mesh — not from
what you assumed:

- Wall positions and extents (e.g. inner wall face `|y| = 56.0` — constant? it
  was constant to u≈40 then bulged inboard toward the tower; see case study).
- Plan tops/bottoms (rail top plane, floor plane offsets).
- Sweep/keepout zones for moving parts (latch-handle swing, lid rotation).
- Fastener/shaft features to preserve (Ø5 pin bores, snap fit tabs).
- Cut-through gaps (open front/rear of the deck area — you'll fill or mount into them).

Store measurements in a constants block at the top of the build script. Every
dimension in the new geometry traces back to a measured number.

### 5. Build new geometry (primitives + booleans)

Use `trimesh.creation.box` / `.cylinder` positioned in the design frame, and
`trimesh.boolean.union/difference/intersection` for combining. Keep the build
script **idempotent and linear**: constants at top, primitives in functions,
one boolean chain, explicit export. Example pieces:

- **Flange pad** on each rail top:
  ```python
  pad = box([L, W, H]); pad.apply_translation([x, side*y0, rail_top + H/2])
  pad -= cylinder(Øpilot, depth) at each fastener (axis horizontal into rail)
  ```
- **Enclosure walls**: a ring (floor plate) at the mating plane + wall boxes
  outside the rail faces + a descending skirt inside the rail channel
  (clearance 0.4–0.8 mm from measured inner faces).
- **Fastener path**: through-bore + counterbore in the mating part; pilot +
  heat-set pocket in the base part. Drill both from the mating face downward
  into material you've verified is solid.
- **Weep/vent holes**: horizontal Ø3.5 cylinders low in any enclosed pocket
  that sits outside.

### 6. Verify, verify, verify

Every build script ends with checks that print BEFORE the files are handed off:

```python
for target in (plain_mesh, modified_mesh):
    clash = trimesh.boolean.intersection([tub, target])
    vol = abs(clash.volume) if len(clash.faces) else 0.0
    assert vol < 1.0, f"clash {vol} mm3"
```

- Volumes watertight on every output mesh.
- `intersection(new_part, everything_else).volume ≈ 0` (expected bolts/weep
  holes excepted).
- Cross-section slice spot-checks (see clip/section idiom below) at several
  stations along the part, confirming walls in the bands you planned:
  ```python
  sec = mesh.section(plane_origin=[u,0,0], plane_normal=[1,0,0])  # plane normal along u
  sec.vertices  # then band-check |y| ranges vs expected wall bands
  ```
- Export + reload the exported STL (parse-back check), not just in-memory mesh —
  STL round-trip is where some boolean result defects first show up.
- Render 3 orthographic projections (PolyCollection of projected triangles) of
  original + modified + new part overlaid, and attach it for the user.

### 7. Print orientation and deliverables

- Choose the print orientation the same way a human would: minimize supports,
  put the largest flat face on the bed, respect the printer's max height.
  Examples: an open tub prints open-face-down; a deck-mounted part prints
  deck-down. Deliver BOTH: a "working frame" STL and a "print-oriented" STL
  (`apply_transform(rotation 180° about X)`).
- Report AS-BUILT numbers: envelope (bbox), clashing volume, list of fasteners
  ("M3 × 10 pan head, 8×", "Ø5 × 40 mm dowel pin, 6×"), material specifics.
- If the file is someone else's design (printables/Makerworld/Thingiverse),
  confirm the license. File mods for personal use are usually fine; publishing
  derivatives usually isn't. State the constraint in your summary.

---

## Decision Framework

| Situation | Approach |
|---|---|
| Need a one-off fix, not a parametric model | Mesh booleans (this workflow) |
| Need parametric replicate/resize | Tell the user: OpenSCAD/CadQuery would serve better; this workflow delivers STL artifacts |
| Mesh is junk (non-manifold, >100 stray shells) | Repair (`merge_vertices`, `process()`) with limits; if beyond repair, stop and report |
| Adding a part that must mate to measured geometry | Design from measured constraints in a derived design frame |
| Moving parts near preserved geometry | Stop BEFORE the keepout zone in your new geometry; find the sweep bbox and leave 2–3 mm |
| Fastening to existing features | Drill into the thickest section you measured; surface-mount parts only rest ON measured planes |
| Print in PETG/ASA vs PLA | PETG: +0.1–0.15mm clearance tolerances (shrinkage); keep walls ≥3 mm; add weeps in any pocket that could pool water |

---

## Collaboration Patterns

- **User** provides the original model, target function ("enclose the rack"),
  printer/material, and confirmed strategy among ranked options.
- **hermes-agent / skill_view** may be available in-session to layer in more
  general 3D tooling guidance.
- **GitHub PR workflow**: deliverables live in the skills repo as workflow docs;
  the STL/3MF artifacts ship through Slack or a file share, not into git.

---

## Key Principles

1. **Never eyeball constraints.** Read them off the mesh. Measure, then build.
2. **Derive a design frame** before writing build code — raw file coordinates
   hide the functional structure.
3. **Booleans verified numerically**, not visually. Render for humans; compute
   for go/no-go.
4. **Preserve what's already validated.** Don't touch mechanism geometry
   someone else tuned (clamp strength, latch sweep, pin fits).
5. **Print orientation is part of design.** Deliver the rotated/positioned
   version the user will actually slice.
6. **License-aware.** Somebody's model entered your session — their license
   terms govern what you can publish.

---

## Pitfalls (Lessons Learned)

- **Wall faces are not constant.** The rack rails had a straight inner face at
  |y|=56 for most of the length, then a **bulge to |y|=51.4 → 43.2 → 31.1**
  between u=50 and 64 toward the tower. Measure at several stations, never at
  one. A wall you assume constant will clash exactly where you weren't looking
  (cost: 3 build iterations re-tracked this).
- **Mating planes stack.** Ring floor plate MUST sit on top of the flange bead's
  top surface, not on the rail. Compute every mating plane from the *previous*
  layer's top, not the first: `PAD_TOP = railtop + bead_h`; `RING_BOT = PAD_TOP`.
  A floor plate assumed at rail-top intersected the beads (7.9 cm³ clash).
- **Convert clash to clearance early.** A bolt bore's cylindrical edge at a
  clash surface reads as a wall face; getting the clearance direction wrong
  shows up as a residual e.g. 2.6 cm³ intersection after the big structures are
  correct. Slice the intersection volume's bbox to find the actual offending
  feature (shrink the mating face, not the bolt bore).
- **Booleans produce watertight garbage silently.** A mesh can be manifold yet
  have faces wound inside-out or overlap seams; volumes and `is_watertight` are
  necessary but NOT sufficient. Slice spot-checks + render + volume reconciliation
  (expected vs actual) catch what watertight checks miss.
- **Section vertices ≠ feature outlines.** `mesh.section()` output vertices
  include union-seam artifacts (e.g. vertices at y=8.8 where walls have no
  feature at y=8.8). They look like holes; they're seams. Confirm with `u` of
  each odd vertex before "fixing" geometry that is actually fine.
- **Bambu A1 plate size** (256 × 256 × 256 mm) is the envelope budget for every
  delivered part; a tub over 160 mm long must orient or split. Check envelope
  BEFORE building details, not after.
- **trimesh version churn**: boolean API moved (`trimesh.boolean` namespace now
  requires `import trimesh.boolean`; older `mesh.difference()` form still works
  but is deprecated). Pin the venv once (`uv venv` + `uv pip install trimesh
  numpy matplotlib scipy networkx`) and reuse it; don't re-resolve mid-task.
- **The mesh XML in 3MF may contain the parts**, but transforms and cut-layout
  metadata live elsewhere; a single modeling XML file's `object_*.model` can be
  parsed similarly — extract each `<object>` + mesh and map by object id from
  the main 3dmodel.model's composition.
- **Thin drivers don't fail loudly**: numpy/npy-script loops can dry-run with
  exit 0 but do nothing if the loaded array shape mismatched. Print shapes and
  a couple of sentinel values (`v.shape`, `v[:1]`) at script start — cheap
  guard against 20 minutes of silent nothing.

---

## Quick Reference

```python
# environment (one-time)
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python trimesh numpy matplotlib scipy networkx
# note: pull in networkx/scipy so mesh.section() works (graph paths for Path3D)

# load STL parts
import trimesh, numpy as np
m = trimesh.load('part.stl')          # process=False if you want as-is geometry
v, f = m.vertices.copy(), m.faces.copy()
np.save('v.npy', v); np.save('f.npy', f)

# 3MF
from zipfile import ZipFile
import xml.etree.ElementTree as ET
```

Design-frame derivation from a dominant tilted plane:

```python
tris = v[f]
n = np.cross(tris[:,1]-tris[:,0], tris[:,2]-tris[:,0])
unit = n / np.linalg.norm(n, axis=1, keepdims=True)
# cluster unit normals by rounding, area-weight them, pick dominant cluster,
# extract plane offset, then build orthonormal basis (u, y, w) from its normal.
```

Preview render (orthographic projection of all triangles):

```python
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.collections as mc
fig, ax = plt.subplots(figsize=(16, 10))
ax.add_collection(mc.PolyCollection(v[f][:, :, [a, b]], facecolors='#c8c8c8'))
ax.set_aspect('equal')  # plus xlim/ylim set from mesh bounds
```

Orient for print (flip open-face down):

```python
import trimesh.transformations as tf
tub.apply_transform(tf.rotation_matrix(np.pi, [1, 0, 0]))
tub.apply_translation([0, 0, -tub.bounds[0][2]])  # drop the flipped mesh to z>=0
```

---

## Related Skills

- `verify-findings` — the verification ethos this workflow follows (numeric proof
  before handoff).
- `writing-plans` — for any modification touching structural load paths, plan
  before you boolean.
