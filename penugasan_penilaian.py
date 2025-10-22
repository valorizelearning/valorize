# penugasan_penilaian.py
import pandas as pd
import random
import os

def baca_daftar(file_input="data_mahasiswa.xlsx", nama_field="NAMA"):
    df = pd.read_excel(file_input)
    cols_upper = {c.upper(): c for c in df.columns}
    if nama_field.upper() not in cols_upper:
        raise ValueError(f"Kolom '{nama_field}' tidak ditemukan. Kolom yang ada: {list(df.columns)}")
    nama_col = cols_upper[nama_field.upper()]
    df[nama_col] = df[nama_col].astype(str).str.strip()
    df = df[df[nama_col] != ""].reset_index(drop=False)
    df.rename(columns={"index": "_orig_index"}, inplace=True)
    return df, nama_col

def buat_penugasan(file_input="data_mahasiswa.xlsx", file_output="hasil_penilaian.xlsx", seed=None, max_attempts=2000):
    """
    Membuat penugasan dan menyimpan file_output.
    Mengembalikan DataFrame hasil.
    """
    df, nama_col = baca_daftar(file_input)
    n = len(df)
    if n < 3:
        raise ValueError("Diperlukan minimal 3 mahasiswa.")
    if seed is not None:
        random.seed(seed)

    attempt = 0
    hasil_list = None
    while attempt < max_attempts:
        attempt += 1
        order = list(range(n))
        random.shuffle(order)
        edges = []
        temp = []
        ok = True
        for pos, idx in enumerate(order):
            pen = df.loc[idx]
            idx1 = order[(pos + 1) % n]
            idx2 = order[(pos + 2) % n]
            t1 = df.loc[idx1]
            t2 = df.loc[idx2]
            if pen["_orig_index"] in (t1["_orig_index"], t2["_orig_index"]):
                ok = False
                break
            if t1["_orig_index"] == t2["_orig_index"]:
                ok = False
                break
            temp.append({
                "Penilai_NAMA": pen.get(nama_col),
                "Penilai_NIM": pen.get("NIM") if "NIM" in df.columns else None,
                "Penilai_NO": pen.get("NO") if "NO" in df.columns else None,

                "Dinilai1_NAMA": t1.get(nama_col),
                "Dinilai1_NIM": t1.get("NIM") if "NIM" in df.columns else None,
                "Dinilai2_NAMA": t2.get(nama_col),
                "Dinilai2_NIM": t2.get("NIM") if "NIM" in df.columns else None,
            })
            edges.append((pen["_orig_index"], t1["_orig_index"]))
            edges.append((pen["_orig_index"], t2["_orig_index"]))
        if not ok:
            continue
        edge_set = set(edges)
        # cek reciprocals
        has_recip = any(((b, a) in edge_set) for (a, b) in edge_set)
        if has_recip:
            continue
        hasil_list = temp
        break

    if hasil_list is None:
        raise RuntimeError(f"Gagal membuat penugasan valid setelah {max_attempts} percobaan.")

    hasil_df = pd.DataFrame(hasil_list)
    hasil_df.to_excel(file_output, index=False)
    return hasil_df
