# Architecture and separation of responsibilities

The project is intentionally split so that CADe_SIMU format parsing, record creation, layout, circuit topology and MCP transport do not leak into each other.

## Module boundaries

| Module | One responsibility |
|---|---|
| `codec.py` | Lossless parsing and dumping of existing `.cad` text |
| `components.py` | Observed CADe_SIMU type-code catalogue |
| `model.py` | Immutable user-facing circuit specifications and annotations |
| `layout.py` | Coordinates only; no file-format strings and no circuit logic |
| `records.py` | Low-level raw CADe_SIMU record factories |
| `writer.py` | Document trailer and record serialization |
| `annotations.py` | Teaching-label content and placement |
| `circuits/power.py` | Three-phase power topology |
| `circuits/control.py` | STOP/START and KM1 self-hold topology |
| `circuits/direct_starter.py` | Composition of power + control + optional annotations |
| `generator.py` | Compatibility imports only; no generation logic |
| `validation.py` | Manual CADe_SIMU validation state |
| `server.py` | MCP-facing adapters only |

## Dependency direction

```text
model / layout / components
          |
          v
       records
          |
          v
  circuits + annotations
          |
          v
        writer

codec is independent and is used as a lossless verification guard.
server depends on the public generation/parsing APIs, never the reverse.
```

## Rules

1. A record factory must create one CADe_SIMU record and nothing else.
2. Layout modules never emit CADe_SIMU text.
3. Circuit modules describe electrical topology; they do not know about MCP.
4. MCP tools never hard-code CADe_SIMU record strings.
5. Unknown format fields are preserved when parsing and are not guessed when generating.
6. Electrical `4000` wire records must never be reused as decorative leader lines.
7. Every generated document must pass parser round-trip before it is returned.
8. Manual CADe_SIMU validation is tracked separately from unit-test success.

## Why `generator.py` still exists

Early versions exposed imports from `cadesimu_mcp.generator`. Removing the module would break callers. It is now a tiny facade that re-exports the real implementations from `circuits/`, keeping compatibility without duplicating logic.
