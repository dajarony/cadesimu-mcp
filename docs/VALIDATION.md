# Validation flow

Unit tests can prove that the generator is internally consistent, but CADe_SIMU itself is the final compatibility oracle.

## Automated gates

- lossless parser round-trip
- record type and reference checks
- coordinate checks
- self-hold topology record checks
- CADe_SIMU control-device scan-order check
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

### Gate D — control simulation — FIX CANDIDATE PENDING MANUAL RETEST

Observed on 2026-09-09 with the previous generator:

- QF1 closes correctly.
- Holding START S1 energizes KM1, closes the KM1 auxiliary contact, closes the three power contacts and runs M1.
- A normal momentary START pulse does **not** remain latched; the motor stops when START returns to rest.
- Therefore the previous build does not pass Gate D.

Root-cause hypothesis from comparison with a known-working CADe_SIMU direct-starter file: CADe_SIMU is sensitive to the order in which control records are emitted/evaluated. The previous generator emitted the KM1 auxiliary contact before the KM1 coil. The reference file emits the coil first and the self-hold auxiliary later, after the main control wiring.

Fix candidate:

- emit QF1 aux -> FR1 aux -> STOP -> START -> KM1 coil -> control supply/return;
- emit the main path wiring;
- emit KM1 auxiliary contact;
- emit the self-hold branch wiring;
- keep a regression test requiring the KM1 coil record to precede the KM1 auxiliary record.

Retest procedure:

1. Run simulation and close QF1.
2. Give START S1 one normal momentary press; do not drag-lock it.
3. After S1 returns to rest, KM1 must remain energized through KM1 aux 13-14 and M1 must keep running.
4. Give STOP S0 one normal momentary press; after S0 returns to rest, KM1 and M1 must remain off.
5. Triggering the overload contact must also interrupt the control path.

Do not mark the direct-starter generator fully validated until this retest passes in CADe_SIMU.

### Gate E — PE/earth — PENDING

Generate and validate the protective-earth connection to the motor PE terminal without altering the simulation network incorrectly.

### Gate F — graphical leader lines — PENDING

Identify CADe_SIMU's non-electrical drawing-line record from a controlled sample before generating callout lines. Never use electrical wire record `4000` for this purpose.

### Gate G — protected single-phase lighting — PENDING MANUAL TEST

Candidate generator implemented for the classroom circuit:

`L/N/PE -> Q1 IGA -> F differential -> Q2 branch breaker -> S1 NO -> H1 lamp`.

The implementation uses observed CADe_SIMU records from known lighting examples: type `3011` for L/N/PE supply, `6005` for the two-pole differential, `6008` for a two-pole magnetothermic breaker, `8008` for a maintained NO switch, `9008` for the lamp, and conductor variants `4018` phase, `4009` neutral and `4010` PE.

Manual test:

1. Open `circuito_monofasico_iga_id_luz.cad` in CADe_SIMU.
2. Confirm the supply and all five devices render in the intended vertical order.
3. Start simulation and close Q1, F and Q2.
4. Toggle S1 closed: H1 must illuminate.
5. Toggle S1 open: H1 must turn off.
6. Opening Q1, F or Q2 must remove power from H1.

Do not mark Gate G as passed until all six checks succeed in the target CADe_SIMU version.
