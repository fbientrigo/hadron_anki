"""Tests for the qualitative + precise mass summary derivation."""
import pytest

from hadron_anki.domain.pedagogical_derivations import derive_mass_summary


def test_combines_bucket_rounded_and_precise():
    assert (
        derive_mass_summary("intermediate", "938 MeV", 938.272088)
        == "intermediate · ≈938 MeV (938.27 MeV)"
    )


def test_trims_trailing_zeros_on_precise_value():
    assert derive_mass_summary("light", "500 MeV", 493.677) == "light · ≈500 MeV (493.68 MeV)"


def test_rejects_non_positive_mass():
    with pytest.raises(ValueError):
        derive_mass_summary("light", "500 MeV", 0)


def test_rejects_empty_bucket_or_display():
    with pytest.raises(ValueError):
        derive_mass_summary("", "500 MeV", 100)
    with pytest.raises(ValueError):
        derive_mass_summary("light", "", 100)
