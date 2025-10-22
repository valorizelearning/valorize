# Introduction {.unnumbered}

::: {.callout-note appearance="simple"}
Kata "Valorize" berasal dari bahasa Prancis valoriser dan akar Latin valor (nilai). Dalam konteks pendidikan, Valorize berarti mengakui, mengembangkan, dan merealisasikan potensi yang ada menjadi nilai nyata yang dapat diukur.
:::

## VALORIZE LEARNING: Where Value is Realized!

Kerangka pembelajaran transformatif yang mengintegrasikan Value (nilai), Collaboration (kolaborasi), Artificial Intelligence (Kecerdasan Buatan), dan Personalized Learning (Pembelajaran yang dipersonalisasi) untuk menciptakan pembelajaran yang bermakna (Value Co-Creation) dalam konteks pendidikan berorientasi nilai (Value Oriented Education).

### VISI

Menjadi kerangka kerja pembelajaran transformatif yang mengakui, mengembangkan, dan merealisasikan potensi peserta didik menjadi kompetensi profesional yang autentik.

### MISI

Memfasilitasi transformasi peserta didik dari konsumen pengetahuan pasif menjadi produsen nilai aktif melalui: Kolaborasi bermakna dalam Knowledge Marketplace berbasis peer production Pembelajaran berbasis proyek autentik yang relevan dengan kebutuhan profesional Pengembangan identitas profesional yang kuat dan adaptif.

Komponen inti framework:

1. VALue (Nilai-nilai luhur sebagai fondasi)
2. Organized through CollaRation (Pembelajaran kolaboratif terorganisir)
3. Intelligence (Kecerdasan Buatan sebagai enabler)
4. Zones of PersonalIzed & Zenith Education (Zona pembelajaran personal menuju puncak potensi)

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

# Penugasan Penilaian — tampilkan hasil di halaman

Blok Python berikut akan **import** `penugasan_penilaian.py`, menjalankan `buat_penugasan`,
menampilkan tabel hasil, dan menambahkan link unduh `hasil_penilaian.xlsx`.

```{python}
# Konfigurasi
FILE_INPUT = "data_mahasiswa.xlsx"   # pastikan file ini ada di repo / folder yang sama
FILE_OUTPUT = "hasil_penilaian.xlsx"
SEED = 42        # set None jika ingin acak tiap render

# import fungsi dari script
import os
from IPython.display import display, HTML
import pandas as pd

# pastikan modul (file .py) ada di working dir
if not os.path.exists("penugasan_penilaian.py"):
    raise FileNotFoundError("File 'penugasan_penilaian.py' tidak ditemukan di folder proyek. Letakkan file di root repo.")

from penugasan_penilaian import buat_penugasan

# fallback kalau data ada di /mnt/data (sebagaimana di runner/CI)
if not os.path.exists(FILE_INPUT):
    alt = "/mnt/data/data_mahasiswa.xlsx"
    if os.path.exists(alt):
        FILE_INPUT = alt
    else:
        raise FileNotFoundError(f\"File '{FILE_INPUT}' tidak ditemukan. Letakkan 'data_mahasiswa.xlsx' di folder proyek atau di /mnt/data.\")
        
# panggil fungsi untuk membuat penugasan
hasil_df = buat_penugasan(file_input=FILE_INPUT, file_output=FILE_OUTPUT, seed=SEED)

# tampilkan hasil ringkasan
display(HTML("<h3>Contoh hasil (10 baris pertama)</h3>"))
display(hasil_df.head(10))

# tampilkan distribusi berapa kali tiap orang dinilai
all_targets = pd.concat([
    hasil_df[["Dinilai1_NAMA","Dinilai1_NIM"]].rename(columns={"Dinilai1_NAMA":"Nama","Dinilai1_NIM":"NIM"}),
    hasil_df[["Dinilai2_NAMA","Dinilai2_NIM"]].rename(columns={"Dinilai2_NAMA":"Nama","Dinilai2_NIM":"NIM"})
], ignore_index=True)
dist = all_targets.groupby("Nama").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
display(HTML("<h4>Distribusi target (berapa kali tiap orang dinilai)</h4>"))
display(dist)

# tambahkan link unduh (file output)
if os.path.exists(FILE_OUTPUT):
    display(HTML(f'<p><a href="{FILE_OUTPUT}" target="_blank">⬇️ Download hasil penilaian (Excel)</a></p>'))
else:
    display(HTML("<p><b>File output belum dibuat.</b></p>"))


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

# Penugasan Penilaian — tampilkan hasil di halaman

Blok Python berikut akan **import** `penugasan_penilaian.py`, menjalankan `buat_penugasan`,
menampilkan tabel hasil, dan menambahkan link unduh `hasil_penilaian.xlsx`.

```{python}
# Konfigurasi
FILE_INPUT = "data_mahasiswa.xlsx"   # pastikan file ini ada di repo / folder yang sama
FILE_OUTPUT = "hasil_penilaian.xlsx"
SEED = 42        # set None jika ingin acak tiap render

# import fungsi dari script
import os
from IPython.display import display, HTML
import pandas as pd

# pastikan modul (file .py) ada di working dir
if not os.path.exists("penugasan_penilaian.py"):
    raise FileNotFoundError("File 'penugasan_penilaian.py' tidak ditemukan di folder proyek. Letakkan file di root repo.")

from penugasan_penilaian import buat_penugasan

# fallback kalau data ada di /mnt/data (sebagaimana di runner/CI)
if not os.path.exists(FILE_INPUT):
    alt = "/mnt/data/data_mahasiswa.xlsx"
    if os.path.exists(alt):
        FILE_INPUT = alt
    else:
        raise FileNotFoundError(f\"File '{FILE_INPUT}' tidak ditemukan. Letakkan 'data_mahasiswa.xlsx' di folder proyek atau di /mnt/data.\")
        
# panggil fungsi untuk membuat penugasan
hasil_df = buat_penugasan(file_input=FILE_INPUT, file_output=FILE_OUTPUT, seed=SEED)

# tampilkan hasil ringkasan
display(HTML("<h3>Contoh hasil (10 baris pertama)</h3>"))
display(hasil_df.head(10))

# tampilkan distribusi berapa kali tiap orang dinilai
all_targets = pd.concat([
    hasil_df[["Dinilai1_NAMA","Dinilai1_NIM"]].rename(columns={"Dinilai1_NAMA":"Nama","Dinilai1_NIM":"NIM"}),
    hasil_df[["Dinilai2_NAMA","Dinilai2_NIM"]].rename(columns={"Dinilai2_NAMA":"Nama","Dinilai2_NIM":"NIM"})
], ignore_index=True)
dist = all_targets.groupby("Nama").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
display(HTML("<h4>Distribusi target (berapa kali tiap orang dinilai)</h4>"))
display(dist)

# tambahkan link unduh (file output)
if os.path.exists(FILE_OUTPUT):
    display(HTML(f'<p><a href="{FILE_OUTPUT}" target="_blank">⬇️ Download hasil penilaian (Excel)</a></p>'))
else:
    display(HTML("<p><b>File output belum dibuat.</b></p>"))
