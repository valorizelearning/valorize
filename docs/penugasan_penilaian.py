# penugasan_penilaian.py
# Usage:
#   python penugasan_penilaian.py [input.xlsx] [output.xlsx] [seed]
# Defaults:
#   input.xlsx = data_mahasiswa.xlsx
#   output.xlsx = hasil_random.xlsx
#   seed = 42

import pandas as pd
import random
import sys
import os
from collections import Counter

# --------- args / defaults ----------
INPUT = sys.argv[1] if len(sys.argv) > 1 else "data_mahasiswa.xlsx"
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "hasil_random.xlsx"
SEED_ARG = sys.argv[3] if len(sys.argv) > 3 else "42"
# ------------------------------------

def find_col(cols, keywords):
    cmap = {c.upper(): c for c in cols}
    for kw in keywords:
        for cu, orig in cmap.items():
            if kw in cu:
                return orig
    return None

def looks_like_url(s):
    if pd.isna(s):
        return False
    st = str(s).strip()
    if st == "":
        return False
    low = st.lower()
    # positive cues
    if "http" in low or "github" in low or ".io" in low or "gitlab" in low:
        return True
    # negative cues
    for bad in ["belum", "not submit", "none", "n/a", "na", "tidak", "kosong"]:
        if bad in low:
            return False
    # fallback: contains dot and no spaces
    if "." in st and " " not in st:
        return True
    return False

def main():
    # cek file input
    if not os.path.exists(INPUT):
        raise FileNotFoundError(f"Input file not found: {INPUT}")

    df_raw = pd.read_excel(INPUT)
    if df_raw.shape[0] == 0:
        raise ValueError("Input file is empty.")

    # deteksi kolom penting (tolerant)
    nama_col = find_col(df_raw.columns, ["NAMA", "NAME"])
    nim_col  = find_col(df_raw.columns, ["NIM", "ID", "NRP"])
    link_col = find_col(df_raw.columns, ["LINK", "URL", "GITHUB", "HASIL", "SUBMIT", "KETERANGAN"])

    if nama_col is None or nim_col is None or link_col is None:
        raise ValueError(
            "Required columns not found. Pastikan file memiliki kolom Nama, NIM, dan Link/URL Hasil Tugas.\n"
            f"Columns found: {list(df_raw.columns)}"
        )

    # seed handling
    if SEED_ARG is None or str(SEED_ARG).lower() == "none":
        seed = None
    else:
        try:
            seed = int(SEED_ARG)
        except:
            seed = 42

    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    # buat salinan output (pertahankan kolom asli)
    out = df_raw.copy().reset_index(drop=True)

    # tambahkan kolom hasil (hindari bentrok nama)
    triples = [
        ("NIM_PENILAI_1", "NAMA_PENILAI_1", "URL_PENILAI_1"),
        ("NIM_PENILAI_2", "NAMA_PENILAI_2", "URL_PENILAI_2"),
    ]
    for a,b,c in triples:
        for col in (a,b,c):
            if col in out.columns:
                i = 1
                newcol = f"{col}_{i}"
                while newcol in out.columns:
                    i += 1
                    newcol = f"{col}_{i}"
                out[newcol] = ""
            else:
                out[col] = ""

    # deteksi submitters (pool target)
    submit_mask = out[link_col].apply(looks_like_url)
    submit_indices = out.index[submit_mask].tolist()
    num_submit = len(submit_indices)

    # pool target: prefer submitters, fallback seluruh kelas jika <2
    if num_submit >= 2:
        pool_indices = submit_indices
    else:
        pool_indices = out.index.tolist()

    # reviewers = SEMUA mahasiswa (termasuk yang belum submit)
    reviewer_indices = out.index.tolist()

    # lakukan assignment: untuk setiap reviewer pilih dua target (tidak self)
    for r in reviewer_indices:
        candidates = [i for i in pool_indices if i != r]
        if len(candidates) >= 2:
            t1, t2 = random.sample(candidates, 2)
        elif len(candidates) == 1:
            t1 = candidates[0]
            t2 = random.choice(candidates)
        else:
            # fallback: seluruh kelas excluding self
            pool_full = [i for i in out.index.tolist() if i != r]
            if len(pool_full) >= 2:
                t1, t2 = random.sample(pool_full, 2)
            elif len(pool_full) == 1:
                t1 = pool_full[0]; t2 = pool_full[0]
            else:
                raise RuntimeError(f"No possible targets for reviewer {r}")

        # temukan nama kolom hasil (untuk jaga jika ada suffix)
        col1_nim  = [c for c in out.columns if c.upper().startswith("NIM_PENILAI_1")][0]
        col1_nama = [c for c in out.columns if c.upper().startswith("NAMA_PENILAI_1")][0]
        col1_url  = [c for c in out.columns if c.upper().startswith("URL_PENILAI_1")][0]
        col2_nim  = [c for c in out.columns if c.upper().startswith("NIM_PENILAI_2")][0]
        col2_nama = [c for c in out.columns if c.upper().startswith("NAMA_PENILAI_2")][0]
        col2_url  = [c for c in out.columns if c.upper().startswith("URL_PENILAI_2")][0]

        # tulis target (ambil NIM/NAMA/URL dari baris target)
        out.at[r, col1_nim]  = out.at[t1, nim_col]
        out.at[r, col1_nama] = out.at[t1, nama_col]
        out.at[r, col1_url]  = out.at[t1, link_col]

        out.at[r, col2_nim]  = out.at[t2, nim_col]
        out.at[r, col2_nama] = out.at[t2, nama_col]
        out.at[r, col2_url]  = out.at[t2, link_col]

    # simpan hasil
    out.to_excel(OUTPUT, index=False)

    # ringkasan
    assigned = []
    for c in out.columns:
        if c.upper().startswith("NIM_PENILAI_"):
            assigned.extend(out[c].dropna().astype(str).tolist())
    counts = Counter([x for x in assigned if str(x).strip() != ""])
    print(f"✅ Saved: {os.path.abspath(OUTPUT)}")
    print(f"Detected submitters (valid URLs): {num_submit} / {len(out)}")
    print("Top assigned targets (NIM -> count):")
    for nim, cnt in counts.most_common(10):
        print(f"  {nim} -> {cnt}")

if __name__ == "__main__":
    main()
