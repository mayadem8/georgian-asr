from pathlib import Path
from tqdm import tqdm

# ====== CONFIG (edit only these) ======
INPUT_FILE  = "kawiki_clean.txt"   # your cleaned text
OUTPUT_FILE = "kawiki_final.txt"                      # output for KenLM
MIN_WORDS = 5                                            # drop short junk lines

# Remove lines that START with any of these (after stripping)
BAD_STARTS = (
    "ვიკიპედია", "დახმარება", "ფორუმი", "კატეგორია", "ფაილი", "სურათი",
    "შაბლონი", "თარგი", "სპეციალური", "პროექტი", "მედიავიკი",
    "იხილეთ", "გარე", "ბმული", "წყარო", "რედაქტირება",
)

# Remove lines that CONTAIN any of these phrases (anywhere in line)
BAD_CONTAINS = (
    "თუ თქვენ", "გთხოვთ", "დააჭირეთ", "განხილვის გვერდზე", "დაცვის ჟურნალ",
    "ლიცენზი", "ავტორ", "რედაქტორ", "შეიტანეთ ცვლილება", "შესწორება",
    "ვერსია", "ისტორია", "რეგისტრ", "ანგარიში", "შეტყობინება",
)
# ======================================

def normalize_spaces(s: str) -> str:
    return " ".join(s.split())

def is_bad_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True

    # too short (often meta)
    if len(s.split()) < MIN_WORDS:
        return True

    # start-based filtering
    for p in BAD_STARTS:
        if s.startswith(p):
            return True

    # contains-based filtering
    for x in BAD_CONTAINS:
        if x in s:
            return True

    return False

def main():
    in_path = Path(INPUT_FILE)
    out_path = Path(OUTPUT_FILE)

    if not in_path.exists():
        print(f"❌ Input not found: {in_path.resolve()}")
        return

    kept = 0
    dropped = 0

    with in_path.open("r", encoding="utf-8", errors="ignore") as fin, \
         out_path.open("w", encoding="utf-8") as fout:

        for line in tqdm(fin, desc="Filtering", unit=" lines"):
            line = normalize_spaces(line)
            if is_bad_line(line):
                dropped += 1
                continue
            fout.write(line + "\n")
            kept += 1

    print("\n✅ DONE")
    print(f"Kept:   {kept:,}")
    print(f"Dropped:{dropped:,}")
    print(f"Output: {out_path.resolve()}")

if __name__ == "__main__":
    main()
