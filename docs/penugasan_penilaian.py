#!/usr/bin/env python3
"""
penugasan_penilaian.py

Usage:
  python penugasan_penilaian.py [input_excel] [output_excel] [seed]

Default:
  input_excel = data_mahasiswa.xlsx
  output_excel = hasil_penugasan_random.xlsx
  seed = 42 (use 'None' to disable reproducible seed)
"""
import sys
import os
import pandas as pd
import random

def baca_daftar(file_input="data_mahasiswa.xlsx", nama_field="NAMA"):
    if not os.path.exists(file_input):
        raise FileNotFoundError(f"File '{file_input}' tidak ditemukan.")
    df = pd.read_excel(file_input)
    cols_upper = {c.upper(): c for c in df.columns}
    if nama_field.upper() not in cols_upper:
        raise ValueError(f"Kolom '{nama_field}' tidak ditemukan. Kolom yang ada: {list(df.columns)}")
    nama_col = cols_upper[nama_field.upper()]
    df[nama_col] = df[nama_col].astype(str).str.strip()
    df = df[df[nama_col] != ""].reset_index(drop=False)
    df.rename(columns={"index": "_orig_index"}, inplace=True)
    return df, nama_col

def buat_penugasan(file_input="data_mahasiswa.xlsx",
                   file_output="hasil_penugasan_random.xlsx",
                   seed=42):
    df, nama_col = baca_daftar(file_input)
    # cari kolom NIM aktual
    nim_col = None
    for c in df.columns:
        if c.upper() == "NIM":
            nim_col = c
            break
    if nim_col is None:
        raise ValueError("Kolom 'NIM' tidak ditemukan pada file input.")

    n = len(df)
    if n < 3:
        raise ValueError("Diperlukan minimal 3 peserta di file input.")

    # list peserta (with orig idx)
    peserta = df[[nim_col, nama_col, "_orig_index"]].to_dict(orient="records")

    # seed handling
    if seed is None or str(seed).lower() == "none":
        random.seed()
    else:
        random.seed(int(seed))

    rows = []
    for rec in peserta:
        kandidat = [r for r in peserta if r["_orig_index"] != rec["_orig_index"]]
        penilai = random.sample(kandidat, 2)
        rows.append({
            "NO": rec.get("NO") if "NO" in df.columns else None,
            "NIM": rec.get(nim_col),
            "NAMA": rec.get(nama_col),
            "NIM_PENILAI_1": penilai[0].get(nim_col),
            "NAMA_PENILAI_1": penilai[0].get(nama_col),
            "NIM_PENILAI_2": penilai[1].get(nim_col),
            "NAMA_PENILAI_2": penilai[1].get(nama_col),
        })

    hasil_df = pd.DataFrame(rows)
    hasil_df.to_excel(file_output, index=False)
    return hasil_df

def main(argv):
    inp = argv[1] if len(argv) > 1 else "data_mahasiswa.xlsx"
    out = argv[2] if len(argv) > 2 else "hasil_penugasan_random.xlsx"
    seed = argv[3] if len(argv) > 3 else 42

    try:
        df_out = buat_penugasan(file_input=inp, file_output=out, seed=seed)
        print(f"✅ Hasil disimpan: {os.path.abspath(out)} (baris: {len(df_out)})")
    except Exception as e:
        print("ERROR:", e)
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv)
