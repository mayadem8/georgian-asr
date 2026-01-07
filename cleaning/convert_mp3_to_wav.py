import os
import subprocess
from tqdm import tqdm

ROOT_DIR = r"D:\Maya\asr_geo\CommonVoice"


mp3_files = []
for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith(".mp3"):
            mp3_files.append(os.path.join(root, file))

print(f"Found {len(mp3_files)} mp3 files")


for mp3_path in tqdm(mp3_files, desc="MP3 → WAV (deleting MP3)"):
    wav_path = mp3_path.replace(".mp3", ".wav")

    if os.path.exists(wav_path):

        try:
            os.remove(mp3_path)
        except Exception:
            pass
        continue

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", mp3_path,
            "-ar", "16000",
            "-ac", "1",
            wav_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


    if result.returncode == 0 and os.path.exists(wav_path):
        try:
            os.remove(mp3_path)
        except Exception as e:
            print(f"\n⚠️ Failed to delete {mp3_path}: {e}")

print("✅ Conversion + cleanup finished")
