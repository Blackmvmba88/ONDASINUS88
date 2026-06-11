from __future__ import annotations

import tempfile
from pathlib import Path

import librosa
import numpy as np
import plotly.graph_objects as go
import soundfile as sf
import streamlit as st

from sinesoothe.engine import export_hunter_report, process_audio
from sinesoothe.presets import get_preset, list_presets


APP_TITLE = "ONDASINUS88"
APP_SUBTITLE = "BlackMamba SineSoothe WebUI"
SUPPORTED_TYPES = ["wav", "mp3", "flac", "ogg", "m4a", "aiff", "aif"]


st.set_page_config(
    page_title=f"{APP_TITLE} WebUI",
    page_icon="🐍",
    layout="wide",
)


st.markdown(
    """
<style>
:root {
  --obsidian: #070812;
  --panel: #101421;
  --cyan: #00f2fe;
  --violet: #a855f7;
  --magenta: #f43f8f;
  --gold: #fbbf24;
  --green: #34d399;
}

.stApp {
  background:
    radial-gradient(circle at 15% 20%, rgba(168, 85, 247, 0.25), transparent 32%),
    radial-gradient(circle at 85% 5%, rgba(0, 242, 254, 0.18), transparent 26%),
    radial-gradient(circle at 55% 95%, rgba(52, 211, 153, 0.13), transparent 30%),
    var(--obsidian);
  color: #e5e7eb;
}

.block-container {
  padding-top: 2rem;
}

.bm-card {
  padding: 1rem 1.2rem;
  border: 1px solid rgba(0, 242, 254, 0.22);
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(16, 20, 33, 0.95), rgba(7, 8, 18, 0.86));
  box-shadow: 0 0 34px rgba(0, 242, 254, 0.08);
}

.bm-title {
  font-size: 2.4rem;
  line-height: 1;
  font-weight: 900;
  letter-spacing: -0.04em;
  margin: 0;
  background: linear-gradient(90deg, var(--cyan), var(--violet), var(--magenta), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.bm-subtitle {
  color: #94a3b8;
  margin-top: 0.25rem;
  font-size: 0.95rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.bm-pill {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  background: rgba(0, 242, 254, 0.08);
  border: 1px solid rgba(0, 242, 254, 0.35);
  color: var(--cyan);
  font-size: 0.8rem;
  margin-right: 0.4rem;
}

[data-testid="stFileUploader"] section {
  border: 2px dashed rgba(0, 242, 254, 0.5);
  background: rgba(16, 20, 33, 0.75);
  border-radius: 20px;
}

.stButton>button {
  border-radius: 14px;
  border: 1px solid rgba(0, 242, 254, 0.35);
  background: linear-gradient(90deg, rgba(0,242,254,.20), rgba(168,85,247,.25));
  color: white;
  font-weight: 800;
}

.stDownloadButton>button {
  border-radius: 14px;
  border: 1px solid rgba(251, 191, 36, 0.35);
  background: linear-gradient(90deg, rgba(251,191,36,.18), rgba(244,63,143,.20));
  color: white;
  font-weight: 800;
}
</style>
""",
    unsafe_allow_html=True,
)


def ensure_workspace() -> Path:
    root = Path(tempfile.gettempdir()) / "ondasinu88_webui"
    root.mkdir(parents=True, exist_ok=True)
    return root


def save_uploaded_file(uploaded_file, workspace: Path) -> Path:
    suffix = Path(uploaded_file.name).suffix.lower() or ".wav"
    target = workspace / f"uploaded{suffix}"
    target.write_bytes(uploaded_file.getbuffer())
    return target


def load_audio_any(path: Path) -> tuple[np.ndarray, int]:
    audio, sr = librosa.load(str(path), sr=None, mono=True)
    if audio.size == 0:
        raise ValueError("Audio vacio o no legible.")
    audio = audio.astype(np.float32)
    peak = float(np.max(np.abs(audio)))
    if peak > 1.0:
        audio = audio / peak * 0.98
    return audio, sr


def trim_audio(audio: np.ndarray, sr: int, start_s: float, end_s: float) -> np.ndarray:
    start_i = max(0, int(start_s * sr))
    end_i = min(len(audio), int(end_s * sr))
    if end_i <= start_i:
        raise ValueError("El final del corte debe ser mayor que el inicio.")
    return audio[start_i:end_i].astype(np.float32)


def downsample_for_plot(audio: np.ndarray, sr: int, max_points: int = 9000) -> tuple[np.ndarray, np.ndarray]:
    if len(audio) <= max_points:
        y = audio
        x = np.arange(len(audio)) / sr
        return x, y

    step = int(np.ceil(len(audio) / max_points))
    y = audio[::step]
    x = np.arange(len(y)) * step / sr
    return x, y


def make_waveform_figure(audio: np.ndarray, sr: int, style: str, title: str) -> go.Figure:
    x, y = downsample_for_plot(audio, sr)

    if style == "Neon Sine":
        glow = np.sin(np.linspace(0, 10 * np.pi, len(y))) * 0.04
        display_y = y + glow
        color = "#00f2fe"
        fill = "rgba(0, 242, 254, 0.12)"
    elif style == "Vocal Plasma":
        display_y = y
        color = "#f43f8f"
        fill = "rgba(244, 63, 143, 0.13)"
    elif style == "Golden Master":
        display_y = y
        color = "#fbbf24"
        fill = "rgba(251, 191, 36, 0.13)"
    elif style == "Emerald Jungle":
        display_y = y
        color = "#34d399"
        fill = "rgba(52, 211, 153, 0.13)"
    else:
        display_y = y
        color = "#a855f7"
        fill = "rgba(168, 85, 247, 0.13)"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=display_y,
            mode="lines",
            line=dict(color=color, width=1.8),
            fill="tozeroy",
            fillcolor=fill,
            name="waveform",
        )
    )
    fig.add_hline(y=0, line_width=1, line_color="rgba(255,255,255,0.18)")
    fig.update_layout(
        title=title,
        height=310,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7,8,18,0.45)",
        font=dict(color="#e5e7eb"),
        margin=dict(l=20, r=20, t=48, b=20),
        xaxis_title="seconds",
        yaxis_title="amplitude",
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", range=[-1.05, 1.05]),
    )
    return fig


def write_wav(path: Path, audio: np.ndarray, sr: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), audio.astype(np.float32), sr)


st.markdown(
    f"""
<div class="bm-card">
  <h1 class="bm-title">{APP_TITLE}</h1>
  <div class="bm-subtitle">{APP_SUBTITLE} · drag, cut, process, export</div>
  <div style="margin-top: 0.8rem;">
    <span class="bm-pill">MP3 / WAV / FLAC</span>
    <span class="bm-pill">Trim Editor</span>
    <span class="bm-pill">Venom Engine</span>
    <span class="bm-pill">Multicolor Wave</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")
workspace = ensure_workspace()

left, right = st.columns([0.62, 0.38], gap="large")

with left:
    uploaded = st.file_uploader(
        "Arrastra cualquier archivo de audio aqui",
        type=SUPPORTED_TYPES,
        accept_multiple_files=False,
    )

with right:
    st.markdown("### Control Room")
    wave_style = st.selectbox(
        "Wave skin",
        ["Neon Sine", "Vocal Plasma", "Golden Master", "Emerald Jungle", "Cosmic Jaguar"],
    )
    preset_name = st.selectbox("Preset", list_presets(), index=0)

if uploaded is None:
    st.info("Suelta un WAV, MP3, FLAC, OGG, M4A o AIFF para abrir el editor.")
    st.stop()

try:
    input_path = save_uploaded_file(uploaded, workspace)
    audio, sr = load_audio_any(input_path)
except Exception as exc:
    st.error(f"No pude leer el audio: {exc}")
    st.stop()

duration = len(audio) / sr
st.success(f"Archivo cargado: {uploaded.name} · {sr} Hz · {duration:.2f}s")

st.plotly_chart(
    make_waveform_figure(audio, sr, wave_style, "Original Waveform"),
    use_container_width=True,
)

st.markdown("## Corte / Trim")
trim_col_1, trim_col_2 = st.columns(2)
with trim_col_1:
    start_s = st.number_input(
        "Inicio del corte (segundos)",
        min_value=0.0,
        max_value=max(0.0, duration - 0.01),
        value=0.0,
        step=0.1,
    )
with trim_col_2:
    end_s = st.number_input(
        "Final del corte (segundos)",
        min_value=0.01,
        max_value=max(0.01, duration),
        value=float(duration),
        step=0.1,
    )

try:
    trimmed = trim_audio(audio, sr, start_s, end_s)
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.plotly_chart(
    make_waveform_figure(trimmed, sr, wave_style, "Selected Region / Trim Preview"),
    use_container_width=True,
)

trimmed_path = workspace / "trimmed_input.wav"
write_wav(trimmed_path, trimmed, sr)

st.audio(str(trimmed_path))

st.markdown("## SineSoothe Engine")
selected_preset = get_preset(preset_name)

c1, c2, c3, c4 = st.columns(4)
with c1:
    depth = st.slider("Depth", 0.0, 1.0, float(selected_preset.depth), 0.01)
with c2:
    sharpness = st.slider("Sharpness", 0.0, 1.0, float(selected_preset.sharpness), 0.01)
with c3:
    mix = st.slider("Mix", 0.0, 1.0, float(selected_preset.mix), 0.01)
with c4:
    max_reduction_db = st.slider(
        "Max Reduction dB",
        0.0,
        18.0,
        float(selected_preset.max_reduction_db),
        0.5,
    )

process_now = st.button("Procesar con ONDASINUS88", use_container_width=True)

if process_now:
    output_path = workspace / "sinesoothe_output.wav"
    json_path = workspace / "sinesoothe_output.json"

    with st.spinner("Cazando resonancias..."):
        result = process_audio(
            input_path=trimmed_path,
            output_path=output_path,
            depth=depth,
            sharpness=sharpness,
            mix=mix,
            max_reduction_db=max_reduction_db,
        )
        export_hunter_report(result, json_path)
        processed_audio, _ = load_audio_any(output_path)

    st.markdown("## Resultado")
    st.audio(str(output_path))
    st.plotly_chart(
        make_waveform_figure(processed_audio, sr, wave_style, "Processed Waveform"),
        use_container_width=True,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Max GR", f"{result.max_reduction_db:.2f} dB")
    m2.metric("Avg GR", f"{result.avg_reduction_db:.2f} dB")
    m3.metric("Venom", f"{result.venom_level_score:.1f}/100")

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "Descargar WAV procesado",
            data=output_path.read_bytes(),
            file_name="ondasinu88_processed.wav",
            mime="audio/wav",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "Descargar JSON report",
            data=json_path.read_bytes(),
            file_name="ondasinu88_report.json",
            mime="application/json",
            use_container_width=True,
        )

    with st.expander("Ver analysis.json"):
        st.code(json_path.read_text(encoding="utf-8"), language="json")
else:
    st.download_button(
        "Descargar solo el corte WAV",
        data=trimmed_path.read_bytes(),
        file_name="ondasinu88_trimmed.wav",
        mime="audio/wav",
        use_container_width=True,
    )
