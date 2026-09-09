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

These names are hypotheses until validated by creating one isolated component at a time in CADe_SIMU and comparing the resulting files.

| Code | Provisional meaning |
|---:|---|
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
6. Only after the codes and field positions are confirmed, implement a generator.
7. Open a generated file in CADe_SIMU and simulate a minimal circuit.

The generator must not guess unknown fields. Until a component schema is validated, the MCP should inspect/preserve it rather than synthesize it.
