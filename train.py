import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

# --- CONFIGURATION ---
# RAM SAFETY: Keep this low (50k) initially. 
# If your Mac has >16GB RAM, you can try 100k.
SAMPLE_LIMIT_PER_FILE = 100000 

# Define your devices and the path to their folders
DEVICES = {
    'Doorbell': '../data/Doorbell',
    'Thermostat': '../data/Thermostat',
    'BabyMonitor': '../data/BabyMonitor',
    'Camera': '../data/Camera'
}

# Define the files we want to load and their labels
# Label Mapping: 0=Benign, 1=Mirai Flood, 2=Bashlite Flood, 3=Port Scan
FILES_TO_LOAD = {
    'benign_traffic.csv': 0,
    'mirai_attacks/udp.csv': 1,
    'gafgyt_attacks/udp.csv': 2,
    'gafgyt_attacks/scan.csv': 3 
}

combined_df = pd.DataFrame()

print("Starting Multi-Device Data Ingestion...")

# --- LOAD DATA LOOP ---
for device_name, folder_path in DEVICES.items():
    print(f"\nProcessing Device: {device_name}...")
    
    for filename, label in FILES_TO_LOAD.items():
        full_path = os.path.join(folder_path, filename)
        
        # Check if file exists (some devices might miss specific attack files)
        if os.path.exists(full_path):
            try:
                print(f"   - Loading {filename} (Label: {label})...")
                df_temp = pd.read_csv(full_path, nrows=SAMPLE_LIMIT_PER_FILE)
                
                # Add the label
                df_temp['label'] = label
                
                # Optional: Add column so we know which device this came from
                # (Useful if you want to debug later)
                # df_temp['device_source'] = device_name 
                
                combined_df = pd.concat([combined_df, df_temp], ignore_index=True)
            except Exception as e:
                print(f"   ⚠️ Error loading {filename}: {e}")
        else:
            print(f"   ⚠️ File not found: {full_path} (Skipping)")

print(f"\n Total Combined Samples: {len(combined_df)}")
print(f"   - Benign: {len(combined_df[combined_df['label']==0])}")
print(f"   - Mirai Flood: {len(combined_df[combined_df['label']==1])}")
print(f"   - Bashlite Flood: {len(combined_df[combined_df['label']==2])}")
print(f"   - Port Scans: {len(combined_df[combined_df['label']==3])}")

# --- TRAIN ---
print("\n Training Universal Random Forest...")
X = combined_df.drop(['label'], axis=1)
# If you added 'device_source' column, drop it here too:
# X = combined_df.drop(['label', 'device_source'], axis=1)
y = combined_df['label']

clf = RandomForestClassifier(n_estimators=50, n_jobs=-1, random_state=42) # n_jobs=-1 uses all CPU cores
clf.fit(X, y)

# --- SAVE ---
print(" Saving 'universal_model.pkl'...")
joblib.dump(clf, 'universal_model.pkl')
print("Done! This model now understands Cameras, BabyMonitor, Thermostat AND Doorbells.")