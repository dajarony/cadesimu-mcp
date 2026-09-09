# Annotation layout rules

For teaching-oriented CADe_SIMU files, explanatory labels should be spatially tied to the component they describe.

## Current rule

- Place each text label on the same Y row (or visual centerline) as its component.
- Keep power-side explanations beside the power component and control-side explanations beside the control component.
- When two components share one row (for example START S1 and the KM1 self-hold auxiliary contact), place one explanation on the left and the other on the right so ownership is unambiguous.
- Include terminal semantics in the label where useful, e.g. `S0 (11-12): PARO NC`, `S1 (13-14): MARCHA NO`, `KM1 aux (13-14): automantenimiento`, `KM1 A1-A2: bobina`.

## Leader lines

Do **not** use CADe_SIMU electrical wire records (`4000`) as visual leader/callout lines. They participate in the electrical network and could change simulation behaviour.

A true non-electrical leader line should only be generated after the graphical/drawing-line record type has been identified and validated from a controlled CADe_SIMU sample. Until then, coordinate-aligned text is the safe annotation method.
