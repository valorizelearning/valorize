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

```{python}
import pandas as pd
import random

def buat_penugasan_tanpa_timball_balik(file_input="data_mahasiswa.xlsx",
                                        kolom_nama="Nama",
                                        file_output="hasil_penilaian_tanpa_timball_balik.xlsx",
                                        seed=None,
                                        max_attempts=1000):
    df = pd.read_excel(file_input)
    nama_asli = df[kolom_nama].astype(str).tolist()
    n = len(nama_asli)
    if n < 3:
        raise ValueError("Minimal 3 mahasiswa diperlukan.")
    if seed is not None:
        random.seed(seed)

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        nama = nama_asli[:]
        random.shuffle(nama)
        edges = []
        hasil = []
        for i, penilai in enumerate(nama):
            din1 = nama[(i + 1) % n]
            din2 = nama[(i + 2) % n]
            if din1 == penilai or din2 == penilai:
                break
            hasil.append({"Penilai": penilai, "Dinilai_1": din1, "Dinilai_2": din2})
            edges.append((penilai, din1))
            edges.append((penilai, din2))
        else:
            edge_set = set(edges)
            has_reciprocal = any((b, a) in edge_set for a, b in edges)
            if not has_reciprocal:
                hasil_df = pd.DataFrame(hasil)
                hasil_df.to_excel(file_output, index=False)
                hasil_df.head()  # tampilkan sebagian hasil di web
                break
    else:
        raise RuntimeError("Gagal membuat penugasan valid setelah banyak percobaan.")