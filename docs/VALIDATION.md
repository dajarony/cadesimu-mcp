# Validation flow

Unit tests can prove that the generator is internally consistent, but CADe_SIMU itself is the final compatibility oracle.

## Automated gates

- lossless parser round-trip
- record type and reference checks
- coordinate checks
- self-hold topology record checks
- CADe_SIMU control-device scan-order check
- reference-preserving clone checks
- annotation placement checks
- single-phase L/N/PE component and conductor checks
- `compileall`
- Ruff in CI

## Manual CADe_SIMU gates

### Gate A — power render — PASS

Generated `L1/L2/L3 -> QF1 -> KM1 -> FR1 -> M1` opened correctly in CADe_SIMU.

### Gate B — annotations — PASS

Free-text labels rendered in CADe_SIMU. The generator now aligns labels with the component they explain.

### Gate C — control render — PASS

The combined direct-starter file opened and rendered QF1 auxiliary, FR1 auxiliary, STOP S0, START S1, KM1 auxiliary self-hold contact and KM1 coil.

### Gate D — control simulation — REFERENCE-PRESERVING RETEST PENDING

Observed with the fully synthetic generator:

- QF1 closes correctly.
- Holding START S1 energizes KM1, closes the KM1 auxiliary contact, closes the three power contacts and runs M1.
- A normal momentary START pulse does **not** remain latched; the motor stops when START returns to rest.
- Reordering the coil and auxiliary records was not sufficient to fix the behavior.

The working hypothesis is now broader: CADe_SIMU stores simulation-relevant metadata that is not yet completely modeled by the synthetic writer. Visual continuity is not enough to prove electrical/simulation continuity.

A second generation path now exists: `build_direct_starter_reference_clone()`. It starts from a canonical known-working CADe_SIMU direct-starter document and performs only narrowly scoped component-reference renames. It does **not** regenerate coordinates, wire records, junction records, network ids or device internals. Automated tests require the record-type sequence to remain identical to the canonical template.

Reference-preserving retest procedure:

1. Generate a reference clone with QF1 / KM1 / FR1 / M1 / S0 / S1 names.
2. Open it in the target CADe_SIMU version.
3. Run simulation and close QF1.
4. Give START S1 one normal momentary press; do not drag-lock it.
5. After S1 returns to rest, KM1 must remain energized through KM1 aux 13-14 and M1 must keep running.
6. Give STOP S0 one normal momentary press; after S0 returns to rest, KM1 and M1 must remain off.
7. Trigger the overload contact; it must interrupt the control path.

If this reference-preserving clone passes, it becomes the compatibility baseline for Gate D while the fully synthetic generator remains experimental for simulation-critical circuits.

### Gate E — PE/earth — PENDING

Generate and validate the protective-earth connection to the motor PE terminal without altering the simulation network incorrectly.

### Gate F — graphical leader lines — PENDING

Identify CADe_SIMU's non-electrical drawing-line record from a controlled sample before generating callout lines. Never use electrical wire record `4000` for this purpose.

### Gate G — protected single-phase lighting — PENDING MANUAL TEST

Candidate generator implemented for the classroom circuit:

`L/N/PE -> Q1 IGA -> F differential -> Q2 branch breaker -> S1 NO -> H1 lamp`.

The implementation uses observed CADe_SIMU records from known lighting examples: type `3011` for L/N/PE supply, `6005` for the two-pole differential, `6008` for a two-pole magnetothermic breaker, `8008` for a maintained NO switch, `9008` for the lamp, and conductor variants `4018` phase, `4009` neutral and `4010` PE.

The first synthetic version rendered but did not simulate reliably. Gate G therefore follows the same rule as Gate D: establish a reference-preserving functional baseline first, then generalize only after the simulation metadata is understood.

Do not mark Gate G as passed until switching and protection behavior succeeds in the target CADe_SIMU version.
