import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import glob
from Pose2Sim import Pose2Sim

# ================= CONFIGURATION =================

# 1. Project directory path (resolved from this file's location)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = script_dir

# 2. Rotation angles [X, Y, Z] in degrees
# Since both people were recorded with the same cameras, 
# they share the same coordinate system and need the SAME rotation.
# - Use [180, 0, 0] if they are "upside down/head in ground".
# - Use [-90, 0, 0] if they are "lying on their backs".
rotation_angles = [180, 180, 0] 

# =================================================

def fix_trc_file(file_path, angles):
    """
    Reads a TRC file, applies a 3D rotation, and overwrites the file.
    """
    filename = os.path.basename(file_path)
    print(f"🔄 Processing file: {filename}")
    
    try:
        # 1. Read the header (First 5 lines contain metadata)
        with open(file_path, 'r') as f:
            header = [f.readline() for _ in range(5)]
        
        # 2. Read the data (Skip the first 5 lines)
        df = pd.read_csv(file_path, sep='\t', skiprows=5, header=None)
        
        # 3. Separate metadata and coordinates
        # Columns 0 and 1 are Frame# and Time
        meta_cols = df.iloc[:, :2] 
        # Columns 2 onwards are X, Y, Z coordinates
        coords = df.iloc[:, 2:].values
        
        # 4. Apply Rotation
        r = R.from_euler('xyz', angles, degrees=True)
        
        # Reshape to (N, 3) for matrix multiplication
        n_rows, n_cols = coords.shape
        flat_coords = coords.reshape(-1, 3)
        
        # Rotate
        rotated_coords = r.apply(flat_coords)
        
        # Reshape back to original dimensions
        rotated_data = pd.DataFrame(rotated_coords.reshape(n_rows, n_cols))
        
        # 5. Overwrite the file
        # Write header first
        with open(file_path, 'w') as f:
            f.writelines(header)
        
        # Append data
        final_df = pd.concat([meta_cols, rotated_data], axis=1)
        final_df.to_csv(file_path, sep='\t', mode='a', header=False, index=False, float_format='%.4f')
        
        print(f"✅ Successfully rotated: {filename}")
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

# === MAIN EXECUTION ===

def main():
    # 1. Define the directory containing 3D data
    pose3d_dir = os.path.join(project_dir, "pose-3d")
    
    # 2. Find all relevant TRC files
    # We look for files ending with 'filt_butterworth_LSTM.trc' 
    # as these are usually the highest quality files for all detected persons.
    search_pattern = os.path.join(pose3d_dir, "*filt_butterworth_LSTM.trc")
    trc_files = glob.glob(search_pattern)
    
    print(f"🔎 Found {len(trc_files)} TRC files to process in: {pose3d_dir}")
    
    if len(trc_files) == 0:
        print("⚠️ No files found! Please check the path or file naming.")
        return

    # 3. Loop through each file and apply rotation
    for trc_file in trc_files:
        fix_trc_file(trc_file, rotation_angles)
        
    # 4. Re-run Kinematics
    # Now that the TRC data is corrected, we generate the .mot files for OpenSim.
    print("\n🚀 All files rotated. Generating OpenSim motion files (.mot)...")
    
    # Note: Pose2Sim automatically processes all detected persons in the folder.
    Pose2Sim.kinematics()
    
    print("🎉 Done! You can now load the .mot files for both persons in OpenSim.")

if __name__ == "__main__":
    main()