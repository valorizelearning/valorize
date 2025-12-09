Template LaTeX Dokumen Tugas Akhir/Tesis Teknik Biomedis ITB
========================================================
Templat asli oleh: Petra Novandi <me@petrabarus.net>  
Diperbarui oleh: [Dionesius Agung](https://github.com/dionesiusap)  
Diperbarui dan diadaptasi oleh: [Irfan Tito Kurniawan](https://github.com/titoirfan)

Dokumen ini merupakan templat LaTeX yang ditujukan untuk laporan tugas akhir atau tesis di program studi Teknik Biomedis ITB. Templat ini penulis gunakan dalam penulisan laporan tugas akhir penulis dan dengan semangat berbagi penulis memutuskan untuk mempublikasikan templat ini agar dapat digunakan oleh banyak orang.

Silakan mengunduh, menggunakan, memodifikasi, dan menyebarkan templat ini. :)

Kebutuhan
---------
Templat telah diuji dan berjalan dengan baik dalam OS Linux Ubuntu 20.04. Untuk melakukan instalasi perangkat lunak yang dibutuhkan, eksekusi perintah berikut.

```
sudo apt-get -qq update && sudo apt-get install -y --no-install-recommends \
    texlive-fonts-recommended texlive-latex-extra texlive-fonts-extra \
    dvipng texlive-latex-recommended texlive-lang-other \
    texlive-bibtex-extra texlive-plain-generic biber xzdec
```

Penggunaan (Linux)
----------

Templat ini telah dilengkapi oleh skrip untuk melakukan kompilasi Makefile. Untuk melakukan kompilasi cukup eksekusi perintah berikut

```
make
```

Hasil kompilasi akan berada pada berkas `output/tesis.pdf`.

Agar menulis dokumen lebih mudah bisa juga menggunakan aplikasi tex editor seperti
[TeXstudio](https://www.texstudio.org/).

Overleaf
----------

Templat ini dapat digunakan pada platform [Overleaf](https://www.overleaf.com) dan teruji per 1 Agustus 2021. Untuk menggunakan templat ini pada platform Overleaf, cukup *compress* isi folder `src` ke dalam sebuah file `*.zip` kemudian unggah file tersebut ke menu `New Project > Upload Project` pada laman utama Overleaf.  Kompilasi dapat dilakukan seperti biasa dengan menekan tombol *compile*.

Bila anda menggunakan daftar singkatan dan lambang, jangan lupa untuk menghapus *cache* kompilasi tiap anda menambahkan singkatan maupun lambang baru.

Kontribusi
----------

Templat ini dapat digunakan secara gratis, akan tetapi penulis sangat
berharap adanya kritik serta saran dari pengguna untuk meningkatkan
kualitas hasil dan penggunaan templat ini.

[comment]: <> (temporary change to link biar gk bingung)
Kritik dan saran tersebut dapat dikirim melalui URL
<https://github.com/titoirfan/eb-itb-latex/issues>.

Terima Kasih
-----------

* Steven Lolong atas pemberian templat LaTeX yang asli.
* Peb Ruswono Aryan atas bantuan pelengkapan struktur dokumen.
