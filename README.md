# cadesimu-mcp

Experimental MCP bridge and file-tooling for **CADe_SIMU**.

The first milestone is deliberately small: understand the CADe_SIMU `.cad` text format well enough to parse it without losing data, inspect components/wires, and round-trip a document byte-for-byte. Once that is stable we can add safe generators for common industrial-control circuits and expose them as MCP tools.

## Status

**Phase 1 — format reconnaissance / parser bootstrap**

- [x] Repository created
- [x] Public `.cad` examples identified for format study
- [ ] Round-trip parser verified against several independent CADe_SIMU files
- [ ] Component type-code catalogue validated
- [ ] Minimal generated `.cad` opened successfully in CADe_SIMU
- [ ] MCP tools for circuit generation

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
