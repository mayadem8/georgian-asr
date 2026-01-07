import os
from tqdm import tqdm

ROOT_DIR = r"D:\Maya\asr_geo\CommonVoice"
MAKE_BACKUP = False 

def fix_one_txt(path: str) -> bool:

    b = open(path, "rb").read()


    b2 = b.replace(b"\x00", b"")


    s = b2.decode("utf-8-sig", errors="ignore")

    fixed = s.lstrip()


    if fixed == s and b2 == b:
        return False


    if MAKE_BACKUP:
        bak_path = path + ".bak"
        if not os.path.exists(bak_path):
            with open(bak_path, "wb") as f:
                f.write(b)


    with open(path, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write(fixed)

    return True

def main():
    txt_files = []
    for root, _, files in os.walk(ROOT_DIR):
        for name in files:
            if name.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, name))

    changed = 0
    for p in tqdm(txt_files, desc="Fixing .txt (UTF-8 BOM + trim start)", unit="file"):
        if fix_one_txt(p):
            changed += 1

    print(f"\n✅ Done. Total txt: {len(txt_files)} | Rewritten: {changed}")

if __name__ == "__main__":
    main()
