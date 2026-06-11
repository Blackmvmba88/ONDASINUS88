from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SineSoothePreset:
    name: str
    depth: float
    sharpness: float
    max_reduction_db: float
    mix: float
    mode: str


PRESETS: dict[str, SineSoothePreset] = {
    "tame-sharp-vocal": SineSoothePreset(
        name="Tame Sharp Vocal",
        depth=0.55,
        sharpness=0.75,
        max_reduction_db=9.0,
        mix=1.0,
        mode="vocal",
    ),
    "sibilance-hunter": SineSoothePreset(
        name="Sibilance Hunter",
        depth=0.65,
        sharpness=0.85,
        max_reduction_db=12.0,
        mix=1.0,
        mode="sibilance",
    ),
    "boxy-room-fix": SineSoothePreset(
        name="Boxy Room Fix",
        depth=0.45,
        sharpness=0.50,
        max_reduction_db=8.0,
        mix=0.90,
        mode="low-mud",
    ),
    "master-gentle-polish": SineSoothePreset(
        name="Master Gentle Polish",
        depth=0.20,
        sharpness=0.40,
        max_reduction_db=4.0,
        mix=0.85,
        mode="master",
    ),
}


def normalize_preset_name(name: str) -> str:
    return name.strip().lower().replace(" ", "-").replace("_", "-")


def get_preset(name: str) -> SineSoothePreset:
    key = normalize_preset_name(name)
    if key not in PRESETS:
        available = ", ".join(sorted(PRESETS))
        raise KeyError(f"Unknown preset '{name}'. Available presets: {available}")
    return PRESETS[key]


def list_presets() -> list[str]:
    return sorted(PRESETS)
