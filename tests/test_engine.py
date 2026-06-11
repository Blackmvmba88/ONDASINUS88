import numpy as np

from sinesoothe.engine import build_resonance_score, make_reduction_map
from sinesoothe.presets import get_preset, list_presets


def test_resonance_score_shape():
    magnitude = np.ones((1025, 20), dtype=np.float32)
    magnitude[300, 10] = 100.0

    score, peak_mask = build_resonance_score(magnitude)

    assert score.shape == magnitude.shape
    assert peak_mask.shape == magnitude.shape
    assert score[300, 10] > 0


def test_reduction_map_has_no_nan():
    score = np.random.rand(1025, 20).astype(np.float32)

    reduction = make_reduction_map(score, depth=0.5)

    assert reduction.shape == score.shape
    assert np.isfinite(reduction).all()
    assert reduction.min() > 0
    assert reduction.max() <= 1.0


def test_presets_load():
    presets = list_presets()
    assert "tame-sharp-vocal" in presets

    preset = get_preset("tame sharp vocal")
    assert preset.depth > 0
    assert preset.max_reduction_db > 0
