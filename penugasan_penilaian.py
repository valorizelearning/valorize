# assign_with_links.py
# Usage:
#   python assign_with_links.py [input.xlsx] [output.xlsx] [seed]
# Defaults:
#   input.xlsx = data_mahasiswa.xlsx
#   output.xlsx = hasil_random.xlsx
#   seed = None (random each run) or integer for reproducible

import pandas as pd
import random
import os
import sys

# ----------------- konfigurasi via argumen -----------------
FILE_INPUT  = sys.argv[1] if len(sys.argv) > 1 else "data_mahasiswa.xlsx"
FILE_OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "hasil_random.xlsx"
SEED_ARG    = sys.argv[3] if len(sys.argv) > 3 else None
# ----------------------------------------------------------

def find_col(cols, keywords):
    """Cari nama kolom dari daftar keywords (case-insensitive contains)."""
    cols_map = {c.upper(): c for c in cols}
    for kw in keywords:
        for cu, orig in cols_map.items():
            if kw in cu:
                return orig
    return None

def is_missing_link(x):
    """Tentukan apakah sel link dianggap tidak submit."""
    if pd.isna(x):
        return True
    s = str(x).strip()
    if s == "":
        return True
    low = s.lower()
    for bad in ["belum", "not submit", "none", "n/a", "na", "tidak", "kosong"]:
        if bad in low:
            return True
    return False

def main():
    if not os.path.exists(FILE_INPUT):
        raise FileNotFoundError(f"Input file not found: {FILE_INPUT}")

    df = pd.read_excel(FILE_INPUT)
    if df.shape[0] == 0:
        raise ValueError("Input file is empty.")

    # Temukan kolom NAMA, NIM, LINK (tolerant)
    nama_col = find_col(df.columns, ["NAMA", "NAME"])
    nim_col  = find_col(df.columns, ["NIM", "ID", "NRP"])
    link_col = find_col(df.columns, ["LINK", "URL", "GITHUB", "HASIL", "SUBMIT"])

    if nama_col is None or nim_col is None or link_col is None:
        raise ValueError(
            "Tidak menemukan kolom yang diperlukan. Pastikan ada kolom NAMA, NIM, dan kolom Link/URL."
        )

    # Normalisasi data
    df = df.copy().reset_index(drop=True)
    df[nama_col] = df[nama_col].astype(str).str.strip()
    df[nim_col]  = df[nim_col].astype(str).str.strip()
    # link tidak diubah agar tetap persis apa yang diisi mahasiswa

    # Buat list index submitter (target pool)
    submit_mask = ~df[link_col].apply(is_missing_link)
    submit_indices = df[submit_mask].index.tolist()
    if len(submit_indices) < 2:
        raise ValueError(f"Terlalu sedikit submitter. Ditemukan {len(submit_indices)} submitter (butuh minimal 2).")

    # Seed handling
    if SEED_ARG is None or str(SEED_ARG).lower() == "none":
        seed = None
    else:
        try:
            seed = int(SEED_ARG)
        except:
            seed = None
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    # Untuk memastikan konsistensi pairing URL-NIM-NAMA kita bekerja menggunakan indeks df.
    # Reviewer = seluruh mahasiswa (df.index)
    # Target pool = submit_indices
    # Untuk setiap reviewer r:
    #   kandidat = submit_indices excluding r (if r also submit)
    #   jika kandidat >= 2: ambil random.sample tanpa replacement
    #   jika kandidat == 1: ambil 1 + ambil satu lagi secara random (boleh berulang)
    #   (kasus kandidat 0 sudah dihindari karena telah dicek submit_indices >=2)

    # Siapkan kolom output (tetap mempertahankan kolom input)
    out = df.copy()
    out["NIM_PENILAI_1"] = ""
    out["NAMA_PENILAI_1"] = ""
    out["URL_PENILAI_1"] = ""
    out["NIM_PENILAI_2"] = ""
    out["NAMA_PENILAI_2"] = ""
    out["URL_PENILAI_2"] = ""

    for r in df.index:
        # buat pool kandidat target (jangan target dirinya sendiri)
        candidates = [i for i in submit_indices if i != r]
        if len(candidates) >= 2:
            t1, t2 = random.sample(candidates, 2)
        elif len(candidates) == 1:
            t1 = candidates[0]
            # pilih t2 dari candidates (boleh sama t1 jika tidak ada pilihan lain)
            t2 = random.choice(candidates)
        else:
            # tidak mungkin karena kita cek submit_indices >=2, tapi jaga safety
            raise RuntimeError("Tidak ada kandidat target untuk reviewer index {}".format(r))

        # tulis hasil — jaga agar NIM/NAMA/URL tetap satu kesatuan diambil dari baris target
        out.at[r, "NIM_PENILAI_1"] = df.at[t1, nim_col]
        out.at[r, "NAMA_PENILAI_1"] = df.at[t1, nama_col]
        out.at[r, "URL_PENILAI_1"]  = df.at[t1, link_col]

        out.at[r, "NIM_PENILAI_2"] = df.at[t2, nim_col]
        out.at[r, "NAMA_PENILAI_2"] = df.at[t2, nama_col]
        out.at[r, "URL_PENILAI_2"]  = df.at[t2, link_col]

    # Simpan hasil
    out.to_excel(FILE_OUTPUT, index=False)
    print(f"✅ Penugasan selesai. File disimpan: {os.path.abspath(FILE_OUTPUT)}")
    # Ringkasan singkat: berapa kali tiap NIM jadi target
    assigned = out["NIM_PENILAI_1"].tolist() + out["NIM_PENILAI_2"].tolist()
    counts = pd.Series(assigned).value_counts().reset_index()
    counts.columns = ["NIM", "Count"]
    print("\nTop target (by assignment count):")
    print(counts.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
