# Case Study: Destaco clamp rack v8 — bolt-on enclosure (Sep 2026)

Concrete walk-through of the SKILL.md workflow on a real job. Original model:
MakerWorld model 1824384, "small clip-on cargo rack saddle bag for bike"
(Destaco-style toggle-clamp rack, personal-use license). Goal: enclose the rack
with a rigid tub + lid mounting, without touching the validated clamp mechanism.

## What the original looked like (measured)

- Rack envelope 261 × 120 × 154 mm; deck plane tilted — normal `(0.460, 0, 0.888)`
  (62.6° from horizontal in the file's frame), NOT axis-aligned.
- Side rails: inner face |y| = 56.0 (straight section), outer face 60.0 wall
  thickness 4, top plane w = 97.8 above deck; straight until u ≈ +40, then the
  rail **bulges inboard** toward the tower (|y| → 51.4 at u=50, 43.2 at 55,
  31.1 at 60) and ends at u=64.6.
- Clamp tower + toggle-latch linkage at u > 40 with a handle sweep keepout.
- Fastener hardware: Ø5 mm dowel pins (6× 40 mm, 2× 30 mm) in the latch.
- Mesh: watertight 2-manifold + ~23 stray shells (logo dots floating 0.35 mm off
  the interior faces).

## The chosen strategy (option 2 of 3 ranked)

Drop-over **tub that bolts down onto flange beads added to the rail tops**:

1. Reprint the rack with 4 mm tall × 7 mm wide beads on each rail top
   (spanning the straight section u −114…+36), each bead drilled with
   Ø2.6 × 5 mm-deep pilots at 4 stations 44 mm apart (y = ±58, through bead +
   rail land into solid material).
2. Tub straddles the rails: floor plate 3 mm riding ON TOP of the beads
   (w 101.8), Ø3.2 bores + Ø6.2 × 1.8 counterbores matching the pilots →
   M3 × 10 fasteners. Side walls hug the rail outer faces (0.6 mm clearance);
   a 48 mm skirt descends inside the rail channel (outer face |y| = 52.6,
   clearing the bead overhang edge |y| = 53.0).
3. Rear wall stops at u = 40 — the bulge/tower/latch-sweep zone stays open.
4. Ø3.5 mm weep holes low in the skirt walls both sides (PETG, outdoor, water
   pools in any pocket that cannot drain).
5. Tub prints open-face-down (161.5 × 127.2 × 163 mm envelope — fits A1 bed);
   rack reprint prints deck-down as oriented in the delivered STL.

Ranking rationale (kept in the reply to the user):
1. **Drop-over tub, no rack edits** — zero risk to the validated mechanism, but
   the tub can only hang on the rails, no bolt-down.
2. **Flange bead mod (chosen)** — small, non-structural addition to surfaces
   that exist only as the flat rail lands; bolt-down rigidity; reprint of the
   rack is one extra print, not a redesign.
3. **Full structural enclosure printing in one piece** — rejected: over-budget
   for the build volume and forces printing the tower unsupported.

## Iteration log (what actually happened)

Three full build passes were needed. Each pass is instructive:

- **Pass 1**: Tub walls placed assuming rail inner face |y| = 56 constant.
  Result: 7087 mm³ clash — the **bulge** at u > 40 was unaccounted. Lesson:
  walls are not constant-prismatic; measure at N stations.
- **Pass 2**: Fixed the bulge by terminating the tub before it (rear wall at
  u = 40). New clash: ring floor plate assumed at rail-top plane (97.8)
  intersected the flange beads (97.8–101.8). 7923 mm³. Lesson: mating planes
  STACK; compute the mating offset from the top of the previous layer.
- **Pass 3**: Ring raised onto the beads. Residual 2650 mm³ clash: the bead
  overhangs the rail inner face by 3 mm (to |y| = 53) and the skirt ran at
  |y| = 55.4. Shrank the skirt outer face to 52.6. Zero clash. Lesson: bolt
  features move effective wall faces; re-check clearances against *modified*
  geometry, not the original.

(A fourth micro-fix before final: re-cut weep holes to match the moved skirt
outer face — the holes drilled relative to the old face.)

## Verification delivered

```text
A. rack_with_flanges.stl  tris 173364  wt True
B. enclosure_tub.stl      tris  2266  wt True  vol 329.7 cm3
C. tub vs plain rack:      0.0 mm3
   tub vs flanged rack:    0.0 mm3
```

Plus: reload-after-export check, cross-section band checks at
u = −110/−60/−20/30/39, 3-view overlay render (grey original / blue beads /
orange tub) attached for visual confirmation, and load bearings reported.

## Artifacts

- `rack_with_flanges.stl` — reprint (deck-down orientation).
- `enclosure_tub.stl` + `enclosure_tub_print_upside_down.stl`.
- Preview PNG (3 orthographic overlays).
- NOT shipped: lid with hinge knuckles (reuses the Ø5 pin system; future job),
  rear panel with latch-sweep cutout (asked user; not requested yet),
  tether-strap lug (style pending user choice).
