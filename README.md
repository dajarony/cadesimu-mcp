# cadesimu-mcp

A small, testable **CADe_SIMU `.cad` parser, circuit generator and MCP server**.

The project reverse-engineers only the parts of the CADe_SIMU text format that have been observed and validated. Unknown fields are preserved instead of guessed.

## Current status

Validated manually in the target CADe_SIMU installation:

- [x] Generated three-phase power circuit opens correctly
- [x] `L1/L2/L3 -> QF1 -> KM1 -> FR1 -> M1` renders correctly
- [x] Free-text teaching annotations render correctly
- [x] Combined power + control file opens and renders
- [x] STOP, START, KM1 auxiliary contact and KM1 coil render
- [ ] START/STOP simulation behaviour validated end-to-end
- [ ] PE/earth connection generated and validated
- [ ] Non-electrical leader/callout line record identified
- [ ] Broader component catalogue validated with controlled CADe_SIMU saves

The next manual gate is **simulation**: START must energize KM1, the KM1 NO auxiliary contact must self-hold the coil, STOP must de-energize it, and the motor power contacts must follow KM1.

## MCP tools

- `inspect_cad_text` — parse records, references, terminals and coordinates
- `roundtrip_cad_text` — prove lossless reconstruction of a `.cad` text document
- `known_type_codes` — list the observed CADe_SIMU record codes
- `validation_status` — report what has been manually validated in CADe_SIMU
- `generate_three_phase_power_circuit` — generate the power side of a direct starter
- `generate_direct_starter_with_control` — generate power + STOP/START + KM1 self-hold

The MCP server is implemented and testable, but it does **not** need to be connected to Universal MCP yet. The generator can be developed and validated independently first.

## Architecture

```text
CADe_SIMU text
      |
      v
+-------------+       +----------------+
| codec.py    |       | components.py  |
| parse/dump  |       | type catalogue |
+-------------+       +----------------+

Generation path

model.py -> layout.py -> records.py -> circuits/* -> writer.py -> *.cad
                 \          /
                  annotations.py

MCP boundary

server.py -> thin wrappers only
```

The prototype `generator.py` remains only as a compatibility facade. Circuit-building logic is split by responsibility under `circuits/`.

See `docs/ARCHITECTURE.md` for module boundaries and `docs/CAD-FORMAT.md` for format notes.

## Development

```bash
python -m pip install -e ".[dev]"
pytest -q
ruff check .
python -m compileall src tests
```

## Safety / scope

This project generates and inspects **schematics and simulation files**. It is not a substitute for electrical design review, protection calculations, applicable standards, or safe work procedures on real energized installations.

## Research sources

Format behaviour has been inferred from publicly available CADe_SIMU project files, including:

- `GermanAriza/cadesimu-projects`
- `ruajelectric-dotcom/CURSO-CADE-SIMU`
- `ELECTROALL/CADE-SIMU`

Third-party sample files are not copied into this repository unless their licence explicitly permits it.
