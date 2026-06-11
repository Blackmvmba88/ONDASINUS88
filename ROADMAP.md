# ONDASINUS88 / BlackMamba SineSoothe Roadmap

Roadmap oficial para convertir ONDASINUS88 en un motor DSP real, visual, medible y eventualmente usable como plugin.

## Principio rector

```txt
Primero que funcione.
Luego que se vea brutal.
Despues que sea realtime.
Al final que sea plugin.
```

---

## Phase 0 - Foundation

### Objetivo

Crear la base del repo, entorno, estructura y primer motor funcional offline.

### Entregables

```txt
README.md
ROADMAP.md
requirements.txt
pyproject.toml
sinesoothe/engine.py
sinesoothe/cli.py
tests/test_engine.py
```

### Checklist

```txt
[x] Definir concepto
[x] Definir arquitectura
[x] Crear README base
[x] Crear roadmap base
[x] Crear repo GitHub
[x] Crear requirements.txt
[x] Crear pyproject.toml
[x] Crear engine.py
[x] Crear cli.py
[x] Crear preset engine
[x] Crear tests base
[ ] Probar con input.wav real
[ ] Exportar output.wav
[ ] Generar before_after.png
[ ] Generar analysis.json
```

### Comando objetivo

```bash
sinesoothe process input.wav -o output.wav --plot
```

### Criterio de exito

```txt
El archivo output.wav existe.
No tiene NaN.
No esta en silencio.
Mantiene duracion aproximada.
La grafica before_after.png se genera.
El audio suena menos filoso sin morir.
```

---

## Phase 1 - Spectral Engine

### Objetivo

Convertir el demo en un motor analitico medible.

### Entregables

```txt
analysis.json
resonance score
reduction metrics
venom level score
preset engine inicial
```

### Checklist

```txt
[x] Separar funciones DSP limpias
[x] Implementar resonance score basico
[x] Implementar persistencia temporal
[x] Calcular reduccion maxima
[x] Calcular reduccion promedio
[x] Exportar analysis.json
[x] Crear sinesoothe/presets.py
[x] Agregar --preset a CLI
[x] Agregar --json-report a CLI
[x] Agregar tests para presets
[ ] Probar reportes con audio real
[ ] Mejorar frequency zone metrics
```

### Comando objetivo

```bash
sinesoothe process vocal_raw.wav \
  -o vocal_clean.wav \
  --preset tame-sharp-vocal \
  --json-report \
  --plot
```

### Salida esperada

```txt
vocal_clean.wav
vocal_clean.png
vocal_clean.json
```

---

## Phase 2 - Dynamic Reduction Upgrade

### Objetivo

Hacer que la reduccion sea mas musical y menos destructiva.

### Mejoras DSP

```txt
attack smoothing
release smoothing
max reduction clamp
frequency weighting
band focus modes
parallel mix preservation
```

### Checklist

```txt
[ ] Attack configurable
[ ] Release configurable
[ ] Smoothing temporal real
[ ] Reduccion maxima por banda
[ ] Frequency weighting por modo
[ ] Control de sibilancia separado
[ ] Control de nasalidad separado
[ ] Control de boxiness separado
[ ] Comparacion objetiva before/after
```

---

## Phase 3 - Static Visual Lab

### Objetivo

Generar visuales utiles sin construir todavia una app pesada.

### Entregables

```txt
before_after.png
reduction_map.png
resonance_heatmap.png
venom_meter.png
```

### Checklist

```txt
[ ] Espectrograma before/after
[ ] Mapa de reduccion
[ ] Heatmap de resonancias
[ ] Metrica Venom Score visual
[ ] Exportar bundle de reporte
```

---

## Phase 4 - Preset Engine Pro

### Objetivo

Convertir los presets en sistema editable y exportable.

### Presets objetivo

```txt
tame-sharp-vocal
soft-rap-vocal
reggaeton-vocal-clean
sibilance-hunter
boxy-room-fix
female-vocal-silk
male-vocal-warm
podcast-smooth
digital-harshness-control
mix-glue-smooth
master-gentle-polish
extreme-rescue
```

### Checklist

```txt
[ ] Migrar presets a JSON
[ ] Validar schema
[ ] Cargar preset externo
[ ] Guardar preset desde CLI
[ ] Listar presets
[ ] Mostrar detalles de preset
```

---

## Phase 5 - Multicolor Skin System

### Objetivo

Disenar identidad visual completa.

### Skins

```txt
Obsidian
Neon Jungle
Cosmic Jaguar
Golden Master
Vocal Plasma
Studio Dark
```

### Elementos visuales

```txt
multicolor waveform
animated sine wave
glow reduction meter
venom meter
snake reduction curve
spectral heat map
```

---

## Phase 6 - Streamlit Visual Lab

### Objetivo

Crear una app interactiva rapida para experimentar.

### Entregables

```txt
apps/visual_lab.py
audio uploader
parameter sliders
preset selector
before/after player
spectrogram viewer
json report viewer
```

### Comando objetivo

```bash
streamlit run apps/visual_lab.py
```

---

## Phase 7 - Intelligence Layer

### Objetivo

Agregar analisis automatico y sugerencias inteligentes sin depender todavia de modelos pesados.

### Features

```txt
auto harshness score
auto mode suggestion
top resonance bands
before/after comparison
recommended preset
danger zones
```

---

## Phase 8 - Batch Processor

### Objetivo

Procesar carpetas completas de audio.

### Comando objetivo

```bash
sinesoothe batch ./raw_vocals \
  --output-dir ./clean_vocals \
  --preset tame-sharp-vocal \
  --json-report \
  --plot
```

---

## Phase 9 - Realtime Prototype

### Objetivo

Explorar procesamiento en tiempo real.

### Riesgos

```txt
latencia alta
clicks
dropouts
CPU spikes
artefactos por ventanas pequenas
```

---

## Phase 10 - Native Engine Path

### Objetivo

Preparar migracion del nucleo DSP a tecnologia mas eficiente.

### Opciones

```txt
Rust DSP core
C++ JUCE core
WebAssembly
Python bindings
```

---

## Phase 11 - Plugin Path

### Objetivo

Convertir SineSoothe en producto tipo plugin.

### Targets

```txt
VST3
AU
Standalone
CLAP opcional
```

---

## Phase 12 - Product Release

### Objetivo

Preparar una version publica instalable.

### Entregables

```txt
landing page
demo video
example audios
before/after comparisons
technical PDF
GitHub release
installer/build artifacts
```

---

## Prioridad inmediata

```txt
1. Clonar repo
2. Crear venv
3. pip install -e .
4. pytest -q
5. Probar con input.wav real
6. Generar output.wav
7. Generar output.png
8. Generar output.json
```

## Regla de oro

```txt
Si suena mas limpio pero perdio alma, fallo.
Si suena igual pero duele menos, gano.
```

**ONDASINUS88 - Spectral Venom Hunter.**
