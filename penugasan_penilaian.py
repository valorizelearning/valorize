---
title: "Penugasan Penilaian Mahasiswa"
format:
  html:
    toc: true
execute:
  echo: true
  warning: false
  error: true
---

# Penugasan Otomatis — setiap mahasiswa menilai 2 orang lain

Dokumen ini membaca file Excel `data_mahasiswa.xlsx` (kolom minimal: `NAMA` — case insensitive) dan membuat penugasan:
- setiap mahasiswa menilai 2 mahasiswa lain,
- tidak ada self-assignment,
- tidak ada pasangan timbal-balik (A→B dan B→A),
- hasil disimpan ke `hasil_penilaian.xlsx` dan ditampilkan.

```{python}
# ------------------ KONFIGURASI ------------------
FILE_INPUT = "data_mahasiswa.xlsx"   # ganti path jika file berada di tempat lain
FILE_OUTPUT = "hasil_penilaian.xlsx"
SEED = 42            # None = acak berbeda tiap render
MAX_ATTEMPTS = 2000
# -------------------------------------------------

import pandas as pd
import random
import os
from IPython.display import display, HTML

# fallback: jika tidak ditemukan di working dir, coba /mnt/data (upload UI)
if not os.path.exists(FILE_INPUT):
    alt = "/mnt/data/data_mahasiswa.xlsx"
    if os.path.exists(alt):
        FILE_INPUT = alt
    else:
        raise FileNotFoundError(
            f"File '{FILE_INPUT}' tidak ditemukan. Letakkan 'data_mahasiswa.xlsx' di folder proyek (sama dengan index.qmd) "
            f"atau di '/mnt/data/'. Current dir: {os.getcwd()}, files: {os.listdir('.')}"
        )

# baca excel
df_raw = pd.read_excel(FILE_INPUT)

# cari kolom NAMA case-insensitive
cols_upper = {c.upper(): c for c in df_raw.columns}
if "NAMA" not in cols_upper:
    raise ValueError(f"Kolom 'NAMA' tidak ditemukan di file. Kolom yang ada: {list(df_raw.columns)}")

nama_col = cols_upper["NAMA"]

# bersihkan baris kosong pada kolom nama dan simpan original index
df = df_raw.copy()
df[nama_col] = df[nama_col].astype(str).str.strip()
df = df[df[nama_col] != ""].reset_index(drop=False)
df.rename(columns={"index": "_orig_index"}, inplace=True)

n = len(df)
if n < 3:
    raise ValueError(f"Diperlukan minimal 3 mahasiswa. Saat ini jumlah baris valid: {n}")

# set seed (opsional)
if SEED is not None:
    random.seed(SEED)

attempt = 0
hasil_list = None

while attempt < MAX_ATTEMPTS:
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

        # safety checks
        if pen["_orig_index"] == t1["_orig_index"] or pen["_orig_index"] == t2["_orig_index"]:
            ok = False
            break
        if t1["_orig_index"] == t2["_orig_index"]:
            ok = False
            break

        temp.append({
            "Penilai_NAMA": pen.get(nama_col),
            "Penilai_NIM": pen.get(cols_upper.get('NIM')),
            "Penilai_NO": pen.get(cols_upper.get('NO')),
            "Penilai_FAKULTAS": pen.get(cols_upper.get('FAKULTAS')),
            "Penilai_PRODI": pen.get(cols_upper.get('PRODI')),

            "Dinilai1_NAMA": t1.get(nama_col),
            "Dinilai1_NIM": t1.get(cols_upper.get('NIM')),
            "Dinilai1_NO": t1.get(cols_upper.get('NO')),
            "Dinilai1_PRODI": t1.get(cols_upper.get('PRODI')),

            "Dinilai2_NAMA": t2.get(nama_col),
            "Dinilai2_NIM": t2.get(cols_upper.get('NIM')),
            "Dinilai2_NO": t2.get(cols_upper.get('NO')),
            "Dinilai2_PRODI": t2.get(cols_upper.get('PRODI')),
        })
        edges.append((pen["_orig_index"], t1["_orig_index"]))
        edges.append((pen["_orig_index"], t2["_orig_index"]))

    if not ok:
        continue

    # cek reciprocals
    edge_set = set(edges)
    has_recip = any(((b, a) in edge_set) for (a, b) in edge_set)
    if has_recip:
        continue

    hasil_list = temp
    break

if hasil_list is None:
    raise RuntimeError(f"Gagal membuat penugasan valid setelah {MAX_ATTEMPTS} percobaan.")

# buat DataFrame hasil dan simpan
hasil_df = pd.DataFrame(hasil_list)

# Pilih kolom rapi kalau tersedia
cols_order = [
    "Penilai_NAMA","Penilai_NIM","Penilai_NO","Penilai_FAKULTAS","Penilai_PRODI",
    "Dinilai1_NAMA","Dinilai1_NIM","Dinilai1_NO","Dinilai1_PRODI",
    "Dinilai2_NAMA","Dinilai2_NIM","Dinilai2_NO","Dinilai2_PRODI"
]
cols_present = [c for c in cols_order if c in hasil_df.columns]
hasil_df = hasil_df[cols_present]

hasil_df.to_excel(FILE_OUTPUT, index=False)
print(f"✅ Penugasan dibuat (attempt {attempt}). File disimpan: {os.path.abspath(FILE_OUTPUT)}")

# tampilkan contoh hasil di halaman
display(HTML("<h4>Contoh hasil (10 baris pertama)</h4>"))
display(hasil_df.head(10))

# ringkasan distribusi target
all_targets = pd.concat([
    hasil_df[["Dinilai1_NAMA","Dinilai1_NIM"]].rename(columns={"Dinilai1_NAMA":"Nama","Dinilai1_NIM":"NIM"}),
    hasil_df[["Dinilai2_NAMA","Dinilai2_NIM"]].rename(columns={"Dinilai2_NAMA":"Nama","Dinilai2_NIM":"NIM"})
], ignore_index=True)

display(HTML("<h4>Distribusi: berapa kali tiap orang dinilai</h4>"))
dist = all_targets.groupby("Nama").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
display(dist)
