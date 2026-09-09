# Validation flow

Unit tests can prove that the generator is internally consistent, but CADe_SIMU itself is the final compatibility oracle.

## Automated gates

- lossless parser round-trip
- record type and reference checks
- coordinate checks
- self-hold topology record checks
- annotation placement checks
- `compileall`
- Ruff in CI

## Manual CADe_SIMU gates

### Gate A — power render — PASS

Generated `L1/L2/L3 -> QF1 -> KM1 -> FR1 -> M1` opened correctly in CADe_SIMU.

### Gate B — annotations — PASS

Free-text labels rendered in CADe_SIMU. The generator now aligns labels with the component they explain.

### Gate C — control render — PASS

The combined direct-starter file opened and rendered QF1 auxiliary, FR1 auxiliary, STOP S0, START S1, KM1 auxiliary self-hold contact and KM1 coil.

### Gate D — control simulation — PENDING

Expected behaviour:

1. Press START S1.
2. KM1 coil energizes.
3. KM1 main power contacts close and M1 is supplied.
4. KM1 auxiliary 13-14 closes and maintains the coil after START is released.
5. Press STOP S0.
6. KM1 coil de-energizes, the self-hold opens and the motor power contacts open.
7. Triggering the overload contact must also interrupt the control path.

Do not mark the direct-starter generator fully validated until Gate D passes in CADe_SIMU.

### Gate E — PE/earth — PENDING

Generate and validate the protective-earth connection to the motor PE terminal without altering the simulation network incorrectly.

### Gate F — graphical leader lines — PENDING

Identify CADe_SIMU's non-electrical drawing-line record from a controlled sample before generating callout lines. Never use electrical wire record `4000` for this purpose.
