---
name: rack-enclosure-geometry
description: >
  Reference for the Destaco clamp rack v8 (MakerWorld 1824384) geometry —
  design-frame coordinates, rail/deck/latch measurements, and the enclosure
  mating interface (beads, bolt grid, skirt clearances). Use when revisiting
  this project to add the lid, rear panel, or tether lugs, or to mount
  anything else onto this rack.
---

# Destaco clamp rack v8 — measured geometry reference

All numbers in the derived **cargo frame**: origin at deck-center, `u` along the
deck's upslope axis (−120.9 = rear open edge, +64.6 = rail ends), `y` across the
deck, `w` = distance above the deck cargo plane. Coordinates in `cargo_frame`
were produced by rotating the raw mesh so the deck's dominant plane (normal
`(0.460, 0, 0.888)`, offset −48.9) is horizontal; scripts live in
`/tmp/destaco_3mf/` (session-artifacts — regenerate via `SKILL.md` workflow if
the tmp dir is gone).

## Rack structure

| Feature | Value (cargo frame) |
|---|---|
| Deck bbox | u −128.7…+38.4 (deck face plane regions), overall part 261 × 120 × 154 mm raw |
| Deck cargo surface | plane offset −48.9 along normal (0.460, 0, 0.888); top face w = 0 |
| Deck thickness | ~2.8 mm (deck top 12.58 → 15.37 raw z) |
| Side rails | walls at \|y\| 56.0 (inner) / 60.0 (outer); **top plane w = 97.8** |
| Rail straight section | u −120.9 … +40 (inner face constant \|y\| = 56.0) |
| Rail bulge zone | u 40 → 64.6: inner face \|y\| 56 → 51.4 (u=50) → 43.2 (u=55) → 31.1 (u=60) |
| Tower / latch zone | u > 40; clamp tower + toggle-latch linkage + handle sweep |
| Floor plane (deck underside) | w ≈ −2.2 (raw z 12.58) |
| Pin hardware | Ø5 mm: 6 × 40 mm, 2 × 30 mm (latch knuckles; keep reusable) |
| Mesh | watertight 2-manifold + ~23 stray logo shells floating 0.35 mm off interior |

Latch link dims (raw, mm): v8_1 = 29.5 × 47.4 × 20; v8_2 = 50.4 × 24.6 × 40;
"v9 20.5 spacer" = 26.4 × 11.2 × 20; test link v8.step_B = 25 × 52 × 37.

## Enclosure mating interface (as built Sep 2026)

| Feature | Value |
|---|---|
| Flange beads | on rail tops, 4 tall × 7 wide (y 53.0…60.0, i.e. 3 mm overhang inboard of rail inner face) |
| Bead span | u −114.45 … +35.55 (straight section only) |
| Bolt grid | 4 per rail, 44 mm apart, at u = −105, −61, −17, +27 offsets (absolute −105+…), y = ±58 |
| Pilot (rack side) | Ø2.6 × 5 mm deep, into bead + rail land (solid column) |
| Fastener spec | M3 × 10 pan head + Ø4 heat-set insert (or M3 nyloc from below if preferred) |
| Tub floor plate | 3 mm, rides on bead top: w 101.8…104.8 |
| Tub clearance bores | Ø3.2 through + Ø6.2 × 1.8 counterbore (cavity side), matching bolt grid |
| Tub side walls | outside rails: y 60.6…63.6, 0.6 mm clearance to rails |
| Tub skirt | inside channel: outer face \|y\| = 52.6 (clears bead edge 53.0), wall 3 mm, descends 48 mm |
| Tub height above plate | 115 mm cavity |
| Tub rear wall | u = 40.0 (stops before bulge/tower) |
| Weep holes | Ø3.5 low in skirt walls both sides, every 24 mm |
| Tub envelope (print orient) | 161.5 × 127.2 × 163 mm (open-face-down fits A1 256³) |

Clash verification: tub∩(plain rack) = 0.0 mm³; tub∩(rack+beads) = 0.0 mm³.

## Constraints carried forward (NOT to violate)

1. Clamp/latch geometry and handle sweep keepout — untouched; rear panel would
   need a sweep-clearance cutout.
2. Ø5 pin system stays reusable for a future hinge (rear-hinged lid knuckles).
3. No hermetic seal — weeps mandatory in any added pocket.
4. License: MakerWorld 1824384 personal-use only. Mods OK for own use; no
   publishing derivative files or selling prints.
5. Materials: PETG on Bambu A1; PLA warped in hot-car testing by original
   designer.

## Open follow-ups (not requested yet)

- Rear-hinged lid (Ø5 pin knuckles along tub rear wall).
- Rear panel with latch-sweep cutout.
- Tether-strap lugs (design pending strap style choice).
