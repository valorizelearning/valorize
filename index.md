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

# file: penugasan_penilaian.py
import pandas as pd
import random
import os

def baca_daftar(file_input="data_mahasiswa.xlsx", kolom_nama_expected="NAMA"):
    """Baca excel dan kembalikan DataFrame. Cari kolom nama (case-insensitive)."""
    df = pd.read_excel(file_input)
    # cari kolom NAMA case-insensitive
    cols_upper = {c.upper(): c for c in df.columns}
    if kolom_nama_expected.upper() in cols_upper:
        nama_col = cols_upper[kolom_nama_expected.upper()]
    else:
        raise ValueError(f"Kolom untuk nama ('{kolom_nama_expected}') tidak ditemukan di {file_input}. "
                         f"Kolom yang ada: {list(df.columns)}")
    # hapus baris nama kosong
    df[nama_col] = df[nama_col].astype(str).str.strip()
    df = df[df[nama_col] != ""].reset_index(drop=True)
    return df, nama_col

def buat_penugasan(
    file_input="data_mahasiswa.xlsx",
    file_output="hasil_penilaian.xlsx",
    seed=None,
    max_attempts=1000
):
    """
    Membuat penugasan: setiap mahasiswa menilai 2 orang lain, tanpa self-assignment
    dan tanpa pasangan timbal-balik. Hasil disimpan ke file_output.
    """
    df, nama_col = baca_daftar(file_input)
    # Buat list nama (unik)
    # Jika ada duplikasi nama, kita tetap gunakan baris (pakai index unik) - namun algoritma mengacu pada index
    df = df.reset_index(drop=False)  # simpan original index di kolom 'index'
    df.rename(columns={"index": "_orig_index"}, inplace=True)
    # Buat list of records
    records = df.to_dict(orient="records")
    n = len(records)
    if n < 3:
        raise ValueError("Diperlukan minimal 3 mahasiswa agar setiap orang bisa menilai 2 orang lain.")
    if seed is not None:
        random.seed(seed)

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        order = list(range(n))  # indices into records
        random.shuffle(order)

        # buat penugasan rotasi (i -> i+1, i -> i+2)
        edges = []
        hasil_list = []
        valid = True
        for pos, idx in enumerate(order):
            penilai = records[idx]
            idx1 = order[(pos + 1) % n]
            idx2 = order[(pos + 2) % n]
            target1 = records[idx1]
            target2 = records[idx2]

            # safety checks: tidak self (seharusnya tidak) dan dua target berbeda
            if penilai["_orig_index"] == target1["_orig_index"] or penilai["_orig_index"] == target2["_orig_index"]:
                valid = False
                break
            if target1["_orig_index"] == target2["_orig_index"]:
                valid = False
                break

            hasil_list.append({
                "_penilai_idx": penilai["_orig_index"],
                "Penilai_NO": penilai.get("NO", None),
                "Penilai_NIM": penilai.get("NIM", None),
                "Penilai_NAMA": penilai.get(nama_col, None),
                "Penilai_FAKULTAS": penilai.get("FAKULTAS", None),
                "Penilai_PRODI": penilai.get("PRODI", None),
                "Penilai_KETERANGAN": penilai.get("KETERANGAN", None),

                "_din1_idx": target1["_orig_index"],
                "Dinilai1_NO": target1.get("NO", None),
                "Dinilai1_NIM": target1.get("NIM", None),
                "Dinilai1_NAMA": target1.get(nama_col, None),
                "Dinilai1_PRODI": target1.get("PRODI", None),

                "_din2_idx": target2["_orig_index"],
                "Dinilai2_NO": target2.get("NO", None),
                "Dinilai2_NIM": target2.get("NIM", None),
                "Dinilai2_NAMA": target2.get(nama_col, None),
                "Dinilai2_PRODI": target2.get("PRODI", None),
            })
            edges.append((penilai["_orig_index"], target1["_orig_index"]))
            edges.append((penilai["_orig_index"], target2["_orig_index"]))

        if not valid:
            continue

        # cek apakah ada pasangan timbal-balik (a->b dan b->a)
        edge_set = set(edges)
        has_reciprocal = any(((b, a) in edge_set) for (a, b) in edge_set)
        if has_reciprocal:
            continue

        # jika valid -> simpan DataFrame hasil
        hasil_df = pd.DataFrame(hasil_list)
        # agar rapi, gabungkan Penilai_NAMA sebagai kolom utama
        hasil_df = hasil_df[[
            "Penilai_NAMA", "Penilai_NIM", "Penilai_NO", "Penilai_FAKULTAS", "Penilai_PRODI",
            "Dinilai1_NAMA", "Dinilai1_NIM", "Dinilai1_NO", "Dinilai1_PRODI",
            "Dinilai2_NAMA", "Dinilai2_NIM", "Dinilai2_NO", "Dinilai2_PRODI"
        ]]
        hasil_df.to_excel(file_output, index=False)
        print(f"✅ Penugasan dibuat (attempt {attempt}). File disimpan: {os.path.abspath(file_output)}")
        return hasil_df

    raise RuntimeError(f"Gagal membuat penugasan valid setelah {max_attempts} percobaan.")

# --- fungsi lookup ---
def siapa_dinilai(hasil_df, nama):
    """Kembalikan tuple (dinilai1, dinilai2) berdasarkan kolom Penilai_NAMA atau Penilai_NIM/NO jika perlu."""
    row = hasil_df[hasil_df["Penilai_NAMA"] == nama]
    if row.empty:
        return None
    r = row.iloc[0]
    return (r["Dinilai1_NAMA"], r["Dinilai2_NAMA"])

def siapa_menilai(hasil_df, nama):
    """Kembalikan list penilai yang menilai 'nama' (cari di Dinilai1_NAMA atau Dinilai2_NAMA)."""
    penilai = hasil_df[(hasil_df["Dinilai1_NAMA"] == nama) | (hasil_df["Dinilai2_NAMA"] == nama)]
    return penilai["Penilai_NAMA"].tolist()

# --- contoh pemakaian ---
if __name__ == "__main__":
    # ganti file_input bila perlu. Letakkan data_mahasiswa.xlsx di folder yang sama dengan file .py atau .qmd
    try:
        hasil = buat_penugasan("data_mahasiswa.xlsx", file_output="hasil_penilaian.xlsx", seed=42)
        # tampilkan beberapa baris
        print(hasil.head(10))
        # contoh lookup: siapa yang dinilai oleh mahasiswa pertama di hasil
        contoh_penilai = hasil.iloc[0]["Penilai_NAMA"]
        print("Contoh penilai:", contoh_penilai)
        print("Yang dinilai oleh", contoh_penilai, ":", siapa_dinilai(hasil, contoh_penilai))
        print("Yang menilai", contoh_penilai, ":", siapa_menilai(hasil, contoh_penilai))
    except Exception as e:
        print("ERROR:", e)
