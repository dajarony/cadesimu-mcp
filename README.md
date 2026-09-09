# cadesimu-mcp

Experimental MCP bridge and file-tooling for **CADe_SIMU**.

The first milestone is deliberately small: understand the CADe_SIMU `.cad` text format well enough to parse it without losing data, inspect components/wires, and round-trip a document byte-for-byte. Once that is stable we can add safe generators for common industrial-control circuits and expose them as MCP tools.

## Status

**Phase 1 — format reconnaissance / parser bootstrap**

- [x] Repository created
- [x] Public `.cad` examples identified for format study
- [x] Lossless parser/inspector bootstrap
- [x] Experimental power-only generator exposed as an MCP tool
- [ ] Round-trip parser verified against several independent CADe_SIMU files
- [ ] Component type-code catalogue validated with controlled saves
- [ ] Generated `.cad` opened and re-saved successfully in the target CADe_SIMU version
- [ ] Promote generation from experimental to validated

The current generator produces this candidate power chain:

```text
L1/L2/L3 -> QF1 -> KM1 -> FR1 -> M1 (3~)
```

It intentionally omits the control circuit and contactor coil until the first generated file has been opened successfully in CADe_SIMU. The MCP response reports `validated_in_cadesimu: false` until that happens.

## Current MCP tools

- `inspect_cad_text` — inspect components, terminals and coordinates
- `roundtrip_cad_text` — verify lossless parser reconstruction
- `known_type_codes` — show provisional CADe_SIMU type codes
- `generate_three_phase_power_circuit` — experimental power-circuit `.cad` generation

## Target architecture

```text
ChatGPT / Auralis
        |
        v
   CADe_SIMU MCP
        |
   +----+--------------------+
   |                         |
inspect / parse          generate / edit
   |                         |
   +-----------+-------------+
               v
          *.cad files
               |
               v
           CADe_SIMU
```

## Safety / scope

This project generates and inspects **schematics/simulation files**. It is not a substitute for electrical design review, protection calculations, applicable standards, or safe work procedures on real energized installations.

## Research sources

Format behaviour is being inferred from publicly available CADe_SIMU project files, including:

- `GermanAriza/cadesimu-projects`
- `ruajelectric-dotcom/CURSO-CADE-SIMU`
- `ELECTROALL/CADE-SIMU`

Third-party sample files are not copied into this repository unless their licence explicitly permits it; tests should prefer small original fixtures produced by this project.
