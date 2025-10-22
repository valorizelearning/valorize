```{python}
import pandas as pd
import random
from IPython.display import display, HTML

# Nama file input dan output
FILE_INPUT = "data_mahasiswa.xlsx"   # ganti sesuai nama file kamu
FILE_OUTPUT = "hasil_penugasan_random.xlsx"

# Baca file Excel
try:
    df = pd.read_excel(FILE_INPUT)
except FileNotFoundError:
    display(HTML(f"<p style='color:red;'>❌ File '{FILE_INPUT}' tidak ditemukan. Pastikan file ada di folder yang sama.</p>"))
    raise

# Pastikan kolom penting tersedia
required_cols = {"NIM", "NAMA"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"File Excel harus memiliki kolom: {', '.join(required_cols)}")

# Siapkan hasil baru
hasil = df.copy()
hasil["NIM_PENILAI_1"] = ""
hasil["NAMA_PENILAI_1"] = ""
hasil["NIM_PENILAI_2"] = ""
hasil["NAMA_PENILAI_2"] = ""

# Daftar mahasiswa
mahasiswa = df[["NIM", "NAMA"]].to_dict(orient="records")

# Random assignment
random.seed(42)
for idx, mhs in enumerate(mahasiswa):
    # kandidat penilai = semua mahasiswa kecuali dirinya sendiri
    kandidat = [x for x in mahasiswa if x["NIM"] != mhs["NIM"]]
    peni
