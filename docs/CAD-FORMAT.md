# CADe_SIMU `.cad` format notes

> Status: reverse-engineering notes, not an official specification.

## What we know so far

Public CADe_SIMU examples show that `.cad` documents are plain text. A document begins with the literal header:

```text
CADe_SIMU
```

The object stream then consists of records whose observed shape is:

```text
*<record-index>*<type-code>#<hash-delimited labels>*<star-delimited numeric fields>
```

Adjacent records are separated by `#`, giving a transition like:

```text
...record-data#*12*4000#next-record-data...
```

A metadata/footer area begins with the marker:

```text
#$$$
```

The current codec intentionally preserves each record as raw text and only derives a small amount of metadata. This is important because many fields are not understood yet.

## Observed positional fields

Across the examples inspected so far, the first eight star-delimited numeric values after the label block appear to be state/terminal flags. The next values consistently behave as geometry:

```text
field[8]  -> x
field[9]  -> y
field[10] -> x2 (not meaningful for every component)
field[11] -> y2 (not meaningful for every component)
```

For a `4000` wire record, `(x, y)` and `(x2, y2)` correspond to the segment endpoints in the inspected examples.

## Provisional type-code observations

The direct-starter power-chain generator was opened successfully in the user's CADe_SIMU installation on 2026-09-09. Individual component schemas still need isolated-file validation before the map can be treated as a full specification.

| Code | Provisional meaning |
|---:|---|
| 8 | free text / annotation label |
| 1000 | three-phase motor |
| 2001 | three-pole contactor |
| 3004 | three-phase supply |
| 4000 | wire segment |
| 4001 | junction/node |
| 6003 | three-pole fuse block |
| 6007 | thermal overload, power path |
| 6009 | three-pole motor protection device |
| 7000 | NO auxiliary contact |
| 7001 | NC auxiliary contact |
| 8000 | NO pushbutton |
| 8001 | NC pushbutton |
| 8018 | overload auxiliary contact |
| 9000 | contactor coil |
| 9008 | indicator lamp |

Observed type `8` records end with a hash followed by display text, for example `#FUERZA` or `#MANDO`. The generator now supports optional explanatory labels using this record shape; rendering is awaiting the same manual CADe_SIMU validation used for the power layout.

## Evidence used for reconnaissance

The main public comparison files currently come from:

- https://github.com/GermanAriza/cadesimu-projects
- https://github.com/ruajelectric-dotcom/CURSO-CADE-SIMU
- https://github.com/ELECTROALL/CADE-SIMU

One especially useful file is `cadesimu-motor_arranque-indirecto.cad` in the first repository because it contains a compact power circuit plus a control circuit: protection, contactor, overload, motor, pushbuttons, coil, auxiliary contact, lamps, wires and nodes.

## Validation plan

1. Create a blank CADe_SIMU file and save it.
2. Add exactly one three-phase supply, save a second file, and diff them.
3. Repeat for fuse, breaker/guardamotor, contactor, thermal overload and motor.
4. Repeat for wire and junction geometry.
5. Verify parser round-trip against every captured file.
6. Validate generated explanatory text labels in CADe_SIMU.
7. Build and validate a complete direct-starter control circuit (STOP, START, seal-in auxiliary contact and KM1 coil).
8. Add PE/earth handling after its exact symbol/connection representation is confirmed.

Unknown fields are preserved rather than guessed. Components that have not been validated should remain inspect/preserve-first until their schema is confirmed.
