import os
import csv
from tqdm import tqdm

ROOT_DIR = r"D:\Maya\asr_geo\CommonVoice"
OUT_CSV = r"D:\Maya\asr_geo\dataset.csv"

rows = []

for root, _, files in os.walk(ROOT_DIR):
    wav_files = [f for f in files if f.lower().endswith(".wav")]

    for wav in wav_files:
        wav_path = os.path.join(root, wav)
        txt_path = wav_path.replace(".wav", ".txt")

        if not os.path.exists(txt_path):
            continue

        with open(txt_path, "r", encoding="utf-8-sig") as f:
            transcript = f.read().strip()

        if not transcript:
            continue

        rows.append({
            "path": wav_path.replace("\\", "/"),
            "transcript": transcript
        })

print(f"Collected {len(rows)} valid samples")

with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["path", "transcript"])
    writer.writeheader()
    writer.writerows(
        tqdm(rows, desc="Writing CSV", unit="sample")
    )

print(f"✅ CSV written to: {OUT_CSV}")
