# Pose2Sim CLI Helper

## Pose2Sim CLI Helper (Deutsch)

`pose2sim_cli.py` fuehrt Pose2Sim-Schritte und optional die TRC-Rotation aus einem einzigen Kommando aus. Standardmaessig laeuft die komplette Pose2Sim-Pipeline vom Verzeichnis der Datei aus (Projektwurzel = Skriptordner).

### Voraussetzungen

- Pose2Sim ist fuer das Projekt installiert und konfiguriert.
- TRC-Dateien (fuer Rotation) liegen unter `pose-3d` neben dem Skript.

### Nutzung

Im Ordner mit `pose2sim_cli.py` ausfuehren:

- Gesamte Pipeline (Standard):
  - `python pose2sim_cli.py`
  - `python pose2sim_cli.py -a`
- Einzelne Schritte:
  - Calibration: `python pose2sim_cli.py -c`
  - Pose Estimation: `python pose2sim_cli.py -p`
  - Synchronization: `python pose2sim_cli.py -s`
  - Person Association: `python pose2sim_cli.py -o`
  - Triangulation: `python pose2sim_cli.py -t`
  - Filtering: `python pose2sim_cli.py -f`
  - Marker Augmentation: `python pose2sim_cli.py -m`
  - Kinematics: `python pose2sim_cli.py -k`
- TRC-Dateien rotieren und `.mot` neu erzeugen: `python pose2sim_cli.py -r`
- Flags kombinieren, z. B. `python pose2sim_cli.py -f -k -r`.

Ohne Flags laeuft die gesamte Pose2Sim-Pipeline. `-r` betrifft nur TRC-Rotation und `.mot`-Erzeugung und kann mit anderen Flags kombiniert werden.

---

## Pose2Sim CLI Helper (English)

`pose2sim_cli.py` lets you run Pose2Sim stages and optional TRC rotation from one command-line tool. By default it runs the full Pose2Sim pipeline from the script's folder, assuming the project root is the same directory as the script.

### Prerequisites

- Pose2Sim installed and configured for the project.
- TRC files (if rotating) under `pose-3d` next to the script.

### Usage

From the directory containing `pose2sim_cli.py`:

- Full pipeline (default):
  - `python pose2sim_cli.py`
  - `python pose2sim_cli.py -a`
- Individual stages:
  - Calibration: `python pose2sim_cli.py -c`
  - Pose estimation: `python pose2sim_cli.py -p`
  - Synchronization: `python pose2sim_cli.py -s`
  - Person association: `python pose2sim_cli.py -o`
  - Triangulation: `python pose2sim_cli.py -t`
  - Filtering: `python pose2sim_cli.py -f`
  - Marker augmentation: `python pose2sim_cli.py -m`
  - Kinematics: `python pose2sim_cli.py -k`
- Rotate TRC files and regenerate `.mot`: `python pose2sim_cli.py -r`
- Combine flags to chain steps, e.g. `python pose2sim_cli.py -f -k -r`.

If no flags are provided, the full Pose2Sim pipeline runs. `-r` only affects TRC rotation and `.mot` regeneration and can be combined with other flags.
