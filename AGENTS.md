# AGENTS.md — read this first

This file is the entry point for any coding agent working on `cadesimu-mcp`.
Read it before modifying code, generated `.cad` output, tests, or documentation.

## Mission

Build a small, testable CADe_SIMU `.cad` parser/generator/MCP bridge that produces files which are not only visually correct, but also simulate correctly in the target CADe_SIMU installation.

## Critical discovery

A `.cad` file can open and look electrically connected while still failing during CADe_SIMU simulation.

Do **not** assume that visible touching lines imply valid electrical connectivity. CADe_SIMU records contain simulation-relevant structure such as terminal relationships, network identifiers, nodes, record variants, orientation/state fields and possibly other metadata that the synthetic generator does not yet fully model.

Therefore there are two generation paths:

1. **Synthetic generation** — useful for reverse engineering, rendering and controlled experiments.
2. **Reference-preserving generation** — starts from a known-working CADe_SIMU file and makes only narrowly scoped safe changes while preserving connectivity-sensitive data.

For simulation-critical work, prefer the reference-preserving path until the synthetic connectivity model has been proven equivalent.

## Current project state

Manual CADe_SIMU validation truth:

- Gate A — three-phase power render: **PASS**
- Gate B — teaching annotations: **PASS**
- Gate C — direct-starter control render: **PASS**
- Gate D — direct-starter simulation: **IN PROGRESS**
- Gate E — PE / protective earth: **PENDING**
- Gate F — non-electrical leader/callout graphics: **PENDING**
- Gate G — protected single-phase lighting simulation: **PENDING**
- Gate H — final QA / v1 release: **PENDING**

See `docs/VALIDATION.md` for the detailed manual protocol.

## Gate D: current blocker

Previous synthetic direct-starter builds render correctly and behave correctly while START is held, but a normal momentary START press does not reliably remain latched after START returns to rest.

Changing record order alone did not solve the problem.

The current fallback/diagnostic path is a **known-working direct-starter reference clone**. It preserves the canonical `.cad` connectivity and changes only safe references such as:

- `K1 -> KM1`
- `Q1 -> QF1`
- `F1 -> FR1`
- `M -> M1`

Do not rewrite its wires, node records, network ids, coordinates or other connectivity-sensitive fields during the Gate D diagnostic.

If the reference-preserving clone passes START/self-hold/STOP/overload simulation, treat that as evidence that the synthetic connectivity model is incomplete rather than a CADe_SIMU runtime problem.

## Gate G: single-phase lighting

Target classroom circuit:

`L/N/PE -> IGA -> differential -> branch breaker -> switch -> lamp`

The synthetic generator already produces the visual structure, but it is **not yet manually validated as simulation-correct**. Do not mark it PASS merely because it opens or renders.

Known observed CADe_SIMU record families used in public lighting examples include:

- `3011` supply/terminal variant
- `6005` two-pole residual-current device / differential
- `6008` two-pole breaker
- `8008` maintained NO switch
- `9008` indicator/lamp
- `4018` phase conductor variant
- `4009` neutral conductor variant
- `4010` PE conductor variant
- `4001` junction

## Architecture rules

Keep responsibilities separated:

- `codec.py` — parse/dump existing CADe_SIMU text losslessly
- `components.py` — observed type-code catalogue only
- `model.py` — immutable user-facing specs
- `layout.py` — coordinates only
- `records.py` — low-level record factories
- `circuits/*` — circuit topology/composition
- `reference_templates.py` — opaque known-working reference data
- reference adapters — narrowly scoped safe transformations only
- `annotations.py` — teaching-label content/placement
- `writer.py` — serialization/trailer
- `server.py` — thin MCP wrappers only

Never put MCP concerns inside circuit generation. Never put raw record construction inside layout code.

Preserve unknown fields instead of guessing them.

Never use an electrical wire record as a decorative callout/leader line.

## Validation rules

CADe_SIMU itself is the final compatibility oracle.

Automated tests prove internal consistency only. Manual CADe_SIMU validation is required before changing a manual gate from PENDING/IN PROGRESS to PASS.

For Gate D, the required sequence is:

1. Start simulation.
2. Close the protection.
3. Press START once normally, without drag-locking it.
4. START returns to rest and KM1 must remain energized through its auxiliary self-hold contact.
5. Motor must remain running.
6. Press STOP once normally.
7. STOP returns to rest and KM1/motor must remain off.
8. Trigger overload; it must interrupt the control path.

## Scope decision

Do **not** connect this project to the user's Universal MCP yet.
Finish standalone CADe_SIMU validation first.

## Before committing

Run or ensure CI runs:

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python -m compileall src tests
```

Opaque one-line CADe_SIMU fixtures may need narrowly scoped lint exemptions. Do not relax lint globally just to accommodate reference data.

## What to do next

Priority order:

1. Finish Gate D with the reference-preserving direct-starter clone.
2. Once Gate D passes, use the same evidence-driven method for the single-phase lighting circuit (Gate G).
3. Validate PE handling (Gate E).
4. Identify a true non-electrical graphics record for callout lines (Gate F).
5. Run final QA and cut v1 only after all required manual gates pass.
