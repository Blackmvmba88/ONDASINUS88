from __future__ import annotations

import datetime as dt
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.ndimage import maximum_filter, uniform_filter1d


@dataclass(frozen=True)
class ProcessResult:
    input_path: str
    output_path: str
    sample_rate: int
    duration_seconds: float
    depth: float
    sharpness: float
    mix: float
    max_reduction_db: float
    avg_reduction_db: float
    venom_level_score: float


def load_audio(path: str | Path, mono: bool = True) -> tuple[np.ndarray, int]:
    audio, sr = librosa.load(str(path), sr=None, mono=mono)

    if audio.size == 0:
        raise ValueError("Audio file is empty.")

    if not np.isfinite(audio).all():
        raise ValueError("Audio contains NaN or infinite values.")

    return audio.astype(np.float32), sr


def build_resonance_score(
    magnitude: np.ndarray,
    sharpness: float = 0.7,
    freq_window: int = 9,
    time_window: int = 3,
) -> tuple[np.ndarray, np.ndarray]:
    """Build a normalized resonance score and a detected peak mask."""

    sharpness = float(np.clip(sharpness, 0.0, 1.0))

    local_max = maximum_filter(
        magnitude,
        size=(freq_window, time_window),
        mode="nearest",
    )

    local_floor = maximum_filter(
        magnitude,
        size=(freq_window * 2 + 1, time_window * 2 + 1),
        mode="nearest",
    )

    eps = 1e-8
    contrast = magnitude / (local_floor + eps)
    peak_strength = magnitude / (local_max + eps)

    threshold = 0.82 + sharpness * 0.13
    peak_mask = peak_strength >= threshold

    raw_score = contrast * peak_mask

    persistence = uniform_filter1d(
        peak_mask.astype(np.float32),
        size=5,
        axis=1,
        mode="nearest",
    )

    score = raw_score * (0.5 + persistence)

    positive = score[score > 0]
    if positive.size:
        score = score / (np.percentile(positive, 95) + eps)

    score = np.clip(score, 0.0, 1.0)
    return score.astype(np.float32), peak_mask


def make_reduction_map(
    score: np.ndarray,
    depth: float = 0.4,
    max_reduction_db: float = 9.0,
) -> np.ndarray:
    """Convert a resonance score into a linear gain-reduction map."""

    depth = float(np.clip(depth, 0.0, 1.0))
    max_reduction_db = float(max(0.0, max_reduction_db))

    reduction_db = -max_reduction_db * depth * score
    reduction_linear = librosa.db_to_amplitude(reduction_db)

    return reduction_linear.astype(np.float32)


def process_audio(
    input_path: str | Path,
    output_path: str | Path,
    depth: float = 0.4,
    sharpness: float = 0.7,
    mix: float = 1.0,
    n_fft: int = 2048,
    hop_length: int = 512,
    max_reduction_db: float = 9.0,
) -> ProcessResult:
    input_path = Path(input_path)
    output_path = Path(output_path)

    audio, sr = load_audio(input_path)
    mix = float(np.clip(mix, 0.0, 1.0))

    stft = librosa.stft(
        audio,
        n_fft=n_fft,
        hop_length=hop_length,
        window="hann",
    )

    magnitude = np.abs(stft).astype(np.float32)
    phase = np.angle(stft).astype(np.float32)

    score, _peak_mask = build_resonance_score(
        magnitude,
        sharpness=sharpness,
    )

    reduction_map = make_reduction_map(
        score,
        depth=depth,
        max_reduction_db=max_reduction_db,
    )

    processed_magnitude = magnitude * reduction_map
    processed_stft = processed_magnitude * np.exp(1j * phase)

    processed_audio = librosa.istft(
        processed_stft,
        hop_length=hop_length,
        length=len(audio),
    ).astype(np.float32)

    final_audio = (1.0 - mix) * audio + mix * processed_audio

    peak = float(np.max(np.abs(final_audio)))
    if peak > 1.0:
        final_audio = final_audio / peak * 0.98

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), final_audio, sr)

    reduction_db = librosa.amplitude_to_db(reduction_map, ref=1.0)
    min_reduction = float(np.min(reduction_db))
    avg_reduction = float(np.mean(reduction_db))
    venom_level_score = float(np.clip(abs(min_reduction) * 10.0, 0.0, 100.0))

    return ProcessResult(
        input_path=str(input_path),
        output_path=str(output_path),
        sample_rate=sr,
        duration_seconds=len(audio) / sr,
        depth=float(depth),
        sharpness=float(sharpness),
        mix=mix,
        max_reduction_db=min_reduction,
        avg_reduction_db=avg_reduction,
        venom_level_score=venom_level_score,
    )


def export_hunter_report(result: ProcessResult, output_json_path: str | Path) -> None:
    """Export a JSON report for the processing run."""

    output_json_path = Path(output_json_path)
    output_json_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "engine_version": "0.1.0",
        "timestamp": dt.datetime.now(dt.UTC).isoformat(),
        "audio_properties": {
            "sample_rate": result.sample_rate,
            "duration_seconds": round(result.duration_seconds, 2),
        },
        "applied_configuration": {
            "depth": result.depth,
            "sharpness": result.sharpness,
            "mix": result.mix,
        },
        "attenuation_metrics": {
            "max_reduction_db": round(result.max_reduction_db, 2),
            "avg_reduction_db": round(result.avg_reduction_db, 2),
            "venom_level_score": round(result.venom_level_score, 1),
        },
        "raw_result": asdict(result),
    }

    with output_json_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)


def plot_before_after(
    input_path: str | Path,
    output_path: str | Path,
    plot_path: str | Path,
    n_fft: int = 2048,
    hop_length: int = 512,
) -> None:
    input_audio, sr = load_audio(input_path)
    output_audio, _ = load_audio(output_path)

    before = librosa.amplitude_to_db(
        np.abs(librosa.stft(input_audio, n_fft=n_fft, hop_length=hop_length)),
        ref=np.max,
    )

    after = librosa.amplitude_to_db(
        np.abs(librosa.stft(output_audio, n_fft=n_fft, hop_length=hop_length)),
        ref=np.max,
    )

    plot_path = Path(plot_path)
    plot_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    librosa.display.specshow(
        before,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="log",
        ax=axes[0],
    )
    axes[0].set_title("Before - Venom Map")

    img = librosa.display.specshow(
        after,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="log",
        ax=axes[1],
    )
    axes[1].set_title("After - Domesticated Signal")

    fig.colorbar(img, ax=axes, format="%+2.0f dB")
    fig.suptitle("ONDASINUS88 / BlackMamba SineSoothe - Before / After", fontsize=16)
    fig.tight_layout()
    fig.savefig(str(plot_path), dpi=160)
    plt.close(fig)
