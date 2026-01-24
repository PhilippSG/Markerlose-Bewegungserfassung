# Markerlose Bewegungserfassung

Dieses Projekt vergleicht zwei Verfahren der markerlosen Bewegungserfassung: **MediaPipe** und **Pose2Sim**, und evaluiert deren Genauigkeit und Leistung für die Analyse menschlicher Bewegungen.

## Projektübersicht

**Markerlose Bewegungserfassung** ist ein akademisches Praktikumsprojekt, das zwei open-source Computervision-Ansätze zur Erfassung menschlicher Bewegungen ohne physische Marker analysiert und vergleicht:

- **MediaPipe**: Googles Echtzeit-Multi-Body-Pose-Schätzungs-Framework
- **Pose2Sim**: Ein Toolkit zur 2D-zu-3D-Pose-Schätzung und biomechanischen Analyse mit OpenSim

Das Projekt beinhaltet eine detaillierte Vergleichsanalyse, biomechanische Modellierung und Validierung gegen Referenzdaten.

## Projektstruktur

### `/Bericht/`

Umfassender LaTeX-basierter technischer Bericht dokumentiert:

- Einleitung und Literaturübersicht
- Methodik für beide Pipelines
- Vergleichsanalyse und Ergebnisse
- Schlussfolgerungen

### `/MediaPipe/`

MediaPipe-Implementierung und Analyse:

- **`scripts/`**: Jupyter Notebooks und Workflow-Skripte
- **`docs/`**: Dokumentation und temporäre Dateien
- **`Vergleich_2D-3D/`**: 2D-zu-3D-Konvertierungsanalyse

### `/Pose2Sim/`

Pose2Sim-Pipeline und Hilfsprogramme:

- **`pose2sim_cli.py`**: CLI-Wrapper für die vollständige Pose2Sim-Pipeline
- **`demo/`**: Demo-Projekt mit Kalibrierungs- und Konfigurationsdateien
- **`requirements.txt`**: Python-Abhängigkeiten für Pose2Sim CLI-Helper

### `/OpenSim/`

Biomechanische Modelle und Markerdefinitionen:

- **`models/`**: OpenSim-kompatible muskuloskeletale Modelle (skaliert und unskaliert)
- **`Markers_BlazePose.xml`**: Markersatzdefinition gemappt auf BlazePose-Keypoints

### `/Vergleich_MP-P2S/`

Vergleichsanalyse und Validierung:

- **`Angles.ipynb`**: Gelenkwinkel-Vergleich zwischen Methoden
- **`extract_markers.ipynb`**: Markerextraktion und -verarbeitung
- **`marker_errors.ipynb`**: Fehleranalyse und Validierung
- **`MediaPipe/`**: Ergebnisse aus der MediaPipe-Pipeline (IK-Ergebnisse, TRC-Dateien, Fehlermetriken)
- **`Pose2Sim/`**: Ergebnisse aus der Pose2Sim-Pipeline (IK-Ergebnisse, TRC-Dateien, Fehlermetriken)
- **`Vergleichsvideos/`**: Vergleichsmaterialien

## Schnelleinstieg

### Ausführung der Pose2Sim-Pipeline

Navigieren Sie in das Verzeichnis `Pose2Sim/demo/` und führen Sie aus:

```bash
# Aktivieren Sie die Pose2Sim-Umgebung
conda activate pose2sim

# Vollständige Pipeline ausführen
python pose2sim_cli.py

# Spezifische Schritte ausführen
python pose2sim_cli.py -f -k -r  # Filterung, Kinematik, TRC-Rotation
```

Detaillierte Anweisungen finden Sie in [Pose2Sim/readme.md](Pose2Sim/readme.md) und [Pose2Sim/demo/readme.md](Pose2Sim/demo/readme.md).

### Vergleichsanalyse

Führen Sie die Jupyter Notebooks in `Vergleich_MP-P2S/` aus, um:

1. Markerpositionen zu extrahieren und zu vergleichen
2. Gelenkwinkelunterschiede zu analysieren
3. Markierungsrekonstruktionsfehler zu evaluieren

## Hauptmerkmale

- **Duale Pipeline-Implementierung**: Komplette Setups für MediaPipe und Pose2Sim
- **Biomechanische Integration**: OpenSim-Modelle mit anatomisch genauen Marker-Zuordnungen
- **Umfassende Analyse**: Jupyter Notebooks zur methodenübergreifenden Validierung
- **Kalibrierungsdatenbank**: Kamerakalibrierungsdaten für Multi-Kamera-Setups
- **Fehlermetriken**: Quantitativer Genauigkeitsvergleich zwischen den Methoden

## Anforderungen

- Python 3.8+
- OpenSim (für muskuloskeletale Modellierung)
- Pose2Sim (installiert und konfiguriert)
- MediaPipe
- Jupyter Notebook
- Gängige wissenschaftliche Pakete (pandas, scipy, numpy)

Siehe die individuellen `requirements.txt`-Dateien der Komponenten für spezifische Abhängigkeiten.

## Kontakt & Zuschreibung

Dieses Projekt ist Teil eines Praktikumsstudiums an der **FH Aachen** (5. Semester Praktika).

---

**Hinweis**: Dieses Repository enthält deutsche Dokumentation und Berichtsdateien. Der Hauptcode ist in Python mit englischen Kommentaren verfasst.
