# ONDASINUS88 - BlackMamba SineSoothe

Dynamic resonance suppressor, spectral de-harshing engine and multicolor audio visual lab.

> No matamos frecuencias. Domesticamos resonancias.

ONDASINUS88 / BlackMamba SineSoothe es un motor DSP para detectar, medir y reducir resonancias agresivas en voces, mezclas y masters usando analisis espectral dinamico.

## Que hace

Pipeline minimo:

```txt
input.wav
  -> STFT analysis
  -> resonance detection
  -> dynamic gain reduction
  -> output.wav
  -> before_after.png
  -> analysis.json
```

## Casos de uso

- Tame sharp vocals
- Reducir sibilancia
- Suavizar voces filosas
- Controlar nasalidad
- Quitar boxiness / cuarto feo
- Reducir harshness digital
- Pulir mixes
- Limpieza suave en mastering
- Reportes tecnicos de procesamiento
- Visualizaciones espectrales antes/despues

## Estado

```txt
Status: Prototype / Phase 1
Version: 0.1.0
Core: Python DSP
Interface: CLI + static visual reports
Future: Visual Lab / realtime / plugin
```

## Instalacion

```bash
git clone https://github.com/Blackmvmba88/ONDASINUS88.git
cd ONDASINUS88

python3 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -e .
```

## Uso rapido

```bash
sinesoothe process input.wav -o output.wav
sinesoothe process input.wav -o output.wav --plot
sinesoothe process input.wav -o output.wav --json-report
```

Con preset vocal:

```bash
sinesoothe process vocal_raw.wav \
  -o vocal_clean.wav \
  --preset tame-sharp-vocal \
  --json-report \
  --plot
```

Mastering suave:

```bash
sinesoothe process mix_bus.wav \
  -o mix_polished.wav \
  --preset master-gentle-polish \
  --json-report \
  --plot
```

## Parametros

### depth

Cantidad de reduccion aplicada.

```txt
0.20 = suave
0.40 = natural
0.70 = agresivo
1.00 = extremo
```

### sharpness

Que tan quirurgico es el detector.

```txt
0.30 = zonas amplias
0.60 = balanceado
0.90 = picos especificos
```

### mix

Blend entre original y procesado.

```txt
0.00 = original
0.50 = paralelo
1.00 = procesado completo
```

### max-reduction-db

Limite maximo de reduccion.

```txt
4 dB  = mastering suave
9 dB  = vocal control
12 dB = rescue mode
```

## Presets incluidos

```txt
tame-sharp-vocal
sibilance-hunter
boxy-room-fix
master-gentle-polish
```

## Reporte JSON

Cada proceso puede generar un reporte tecnico:

```bash
sinesoothe process input.wav -o output.wav --json-report
```

Salida esperada:

```txt
output.wav
output.json
```

## Sistema visual futuro

Paleta base:

```txt
Obsidian black
Neon cyan
Emerald green
Plasma violet
Liquid gold
Hot magenta
Deep blue
```

Skins futuros:

```txt
Obsidian
Neon Jungle
Cosmic Jaguar
Golden Master
Vocal Plasma
Studio Dark
```

## Onda sinusoidal viva

La interfaz futura incluira una onda sinusoidal reactiva:

```txt
Amplitude  -> volumen RMS
Color      -> intensidad de resonancia
Glow       -> reduccion aplicada
Frequency  -> centro espectral dominante
Motion     -> energia dinamica
```

## Tests

```bash
pytest -q
```

## Motor DSP

```txt
audio
  -> librosa.stft
  -> magnitude + phase
  -> local peak detection
  -> resonance score
  -> gain reduction map
  -> istft reconstruction
```

## Resonance Score

El score considera:

```txt
peak height
local contrast
temporal persistence
frequency zone weighting
sharpness
```

Zonas criticas:

```txt
200 Hz - 500 Hz     boxiness / mud
700 Hz - 1.2 kHz    nasalidad
2 kHz - 5 kHz       filo / agresividad vocal
5 kHz - 9 kHz       sibilancia
10 kHz - 14 kHz     brillo aspero
```

## Venom Meter

Metrica experimental:

```txt
0 - 20    clean
20 - 50   spicy
50 - 75   harsh
75 - 100  venom critical
```

## Desarrollo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ruff check .
pytest -q
```

## Milestone sagrado

```txt
input.wav
  -> deteccion de picos
  -> reduccion dinamica
  -> output.wav
  -> before_after.png
  -> analysis.json
```

## Licencia

MIT License.

## Autor

BlackMamba Records & Labs

Grado 33: audio, codigo, ritual y caceria espectral.
