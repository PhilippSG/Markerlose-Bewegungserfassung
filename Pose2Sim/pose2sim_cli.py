import argparse
import glob
import os
import pandas as pd
from scipy.spatial.transform import Rotation as R
from Pose2Sim import Pose2Sim

# ================= CONFIGURATION =================
# Project directory path (resolved from this file's location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = SCRIPT_DIR

# Rotation angles [X, Y, Z] in degrees
# - Use [180, 0, 0] if subjects are upside down
# - Use [-90, 0, 0] if subjects are lying on their backs
ROTATION_ANGLES = [180, 180, 0]
# =================================================


def fix_trc_file(file_path, angles):
    """Reads a TRC file, applies a 3D rotation, and overwrites the file."""
    filename = os.path.basename(file_path)
    print(f"🔄 Processing file: {filename}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            header = [f.readline() for _ in range(5)]

        df = pd.read_csv(file_path, sep="\t", skiprows=5, header=None)

        meta_cols = df.iloc[:, :2]
        coords = df.iloc[:, 2:].values

        r = R.from_euler("xyz", angles, degrees=True)

        n_rows, n_cols = coords.shape
        flat_coords = coords.reshape(-1, 3)
        rotated_coords = r.apply(flat_coords)
        rotated_data = pd.DataFrame(rotated_coords.reshape(n_rows, n_cols))

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(header)

        final_df = pd.concat([meta_cols, rotated_data], axis=1)
        final_df.to_csv(
            file_path,
            sep="\t",
            mode="a",
            header=False,
            index=False,
            float_format="%.4f",
        )

        print(f"✅ Successfully rotated: {filename}")

    except Exception as e:  # noqa: BLE001
        print(f"❌ Error processing {filename}: {e}")


def rotate_trc_files():
    pose3d_dir = os.path.join(PROJECT_DIR, "pose-3d")
    search_pattern = os.path.join(pose3d_dir, "*filt_butterworth_LSTM.trc")
    trc_files = glob.glob(search_pattern)

    print(f"🔎 Found {len(trc_files)} TRC files to process in: {pose3d_dir}")
    if len(trc_files) == 0:
        print("⚠️ No files found! Please check the path or file naming.")
        return

    for trc_file in trc_files:
        fix_trc_file(trc_file, ROTATION_ANGLES)

    print("\n🚀 All files rotated. Generating OpenSim motion files (.mot)...")
    Pose2Sim.kinematics()
    print("🎉 Done! You can now load the .mot files for both persons in OpenSim.")


POSE2SIM_PIPELINE = [
    ("calibration", Pose2Sim.calibration),
    ("poseEstimation", Pose2Sim.poseEstimation),
    ("synchronization", Pose2Sim.synchronization),
    ("personAssociation", Pose2Sim.personAssociation),
    ("triangulation", Pose2Sim.triangulation),
    ("filtering", Pose2Sim.filtering),
    ("markerAugmentation", Pose2Sim.markerAugmentation),
    ("kinematics", Pose2Sim.kinematics),
]


def run_pose2sim_steps(step_names):
    for name, func in POSE2SIM_PIPELINE:
        if name in step_names:
            print(f"\n▶ Running {name} ...")
            func()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pose2Sim pipeline helper and TRC rotation"
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run the full Pose2Sim pipeline (default when no flags are given)",
    )
    parser.add_argument("-c", "--calibration", action="store_true", help="Run calibration")
    parser.add_argument("-p", "--pose", action="store_true", help="Run pose estimation")
    parser.add_argument("-s", "--sync", action="store_true", help="Run synchronization")
    parser.add_argument("-o", "--assoc", action="store_true", help="Run person association")
    parser.add_argument(
        "-t", "--triangulation", action="store_true", help="Run triangulation"
    )
    parser.add_argument("-f", "--filtering", action="store_true", help="Run filtering")
    parser.add_argument(
        "-m", "--marker", action="store_true", help="Run marker augmentation"
    )
    parser.add_argument(
        "-k", "--kinematics", action="store_true", help="Run kinematics"
    )
    parser.add_argument(
        "-r",
        "--rotate",
        action="store_true",
        help="Rotate TRC files in pose-3d and regenerate .mot files",
    )
    return parser.parse_args()


def selected_steps_from_args(args):
    step_flags = [
        (args.calibration, "calibration"),
        (args.pose, "poseEstimation"),
        (args.sync, "synchronization"),
        (args.assoc, "personAssociation"),
        (args.triangulation, "triangulation"),
        (args.filtering, "filtering"),
        (args.marker, "markerAugmentation"),
        (args.kinematics, "kinematics"),
    ]
    any_step_flag = any(flag for flag, _ in step_flags)
    if args.all or (not any_step_flag and not args.rotate):
        return [name for name, _ in POSE2SIM_PIPELINE]
    return [name for flag, name in step_flags if flag]


def main():
    args = parse_args()
    steps_to_run = selected_steps_from_args(args)

    if steps_to_run:
        run_pose2sim_steps(steps_to_run)

    if args.rotate:
        rotate_trc_files()


if __name__ == "__main__":
    main()
