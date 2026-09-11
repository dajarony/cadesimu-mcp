from __future__ import annotations

from .codec import CadDocument
from .model import DirectStarterSpec
from .reference_templates import DIRECT_STARTER_REFERENCE


def _normalize_reference(value: str) -> str:
    value = value.strip().lstrip("-")
    if not value or any(char in value for char in "#*"):
        raise ValueError("invalid CADe_SIMU reference")
    return value


def _replace_reference(cad_text: str, old: str, new: str) -> str:
    old_ref = _normalize_reference(old)
    new_ref = _normalize_reference(new)
    marker = f"#-{old_ref}#"
    if marker not in cad_text:
        raise ValueError(f"reference {old_ref!r} is not present in the canonical template")
    return cad_text.replace(marker, f"#-{new_ref}#")


def build_direct_starter_reference_clone(spec: DirectStarterSpec | None = None) -> str:
    """Clone the canonical working starter while preserving all network metadata.

    This path intentionally does not regenerate wires, coordinates, network ids or
    device internals. It only renames component references. That makes it useful
    as the compatibility baseline while the fully synthetic generator continues
    to be reverse-engineered.
    """
    spec = spec or DirectStarterSpec(include_explanations=False)
    cad_text = DIRECT_STARTER_REFERENCE
    replacements = (
        ("Q1", spec.protection),
        ("K1", spec.contactor),
        ("F1", spec.overload),
        ("M", spec.motor),
        ("S0", spec.stop_button),
        ("S1", spec.start_button),
    )
    for old, new in replacements:
        cad_text = _replace_reference(cad_text, old, new)

    # A clone must stay structurally parseable after all narrow substitutions.
    doc = CadDocument.parse(cad_text)
    if doc.dumps() != cad_text:
        raise RuntimeError("reference clone failed CADe_SIMU round-trip")
    return cad_text
