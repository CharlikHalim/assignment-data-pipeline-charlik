# Data Preparation & Pipeline Project

## 1. Project Overview

Project ini merupakan implementasi assignment Data Engineering: Pipeline & Preparation.

Tujuannya adalah membangun pipeline Python untuk membaca dataset otomotif mentah, memeriksa kualitas data, melakukan data cleaning dan transformation, serta menyimpan hasil pemrosesan sebagai dataset baru.

## 2. Dataset

Dataset utama:
- automobileEDA_dirty_training.csv

Dataset referensi:
- automobileEDA.csv
- automobile_processed.csv

Dataset mentah digunakan sebagai input pipeline. Dataset referensi hanya digunakan untuk memahami struktur data dan membandingkan hasil.

## 3. Project Structure
```text
data-pipeline-assignment/
├── data/
│   ├── raw/
│   │   └── automobileEDA_dirty_training.csv
│   └── processed/
│       └── automobileEDA_processed.csv
├── src/
│   └── pipeline.py
├── documentation/
│   └── data-flow-diagram.png
├── README.md
└── requirements.txt
```

## 4. Tools and Libraries

- Python
- Pandas
- NumPy
- scikit-learn
- VS Code
- Git
- GitHub

## 5. Initial Dataset Inspection

Berdasarkan pemeriksaan awal dataset:

- Jumlah baris: 205
- Jumlah kolom: 30
- Total missing values: 17
- Jumlah duplicate records: 4

Kolom dengan missing values:

| Kolom             | Missing values |
| ----------------  | -------------- |
| transaction_date  |              2 |
| make              |              2 |
| num-of-doors      |              2 |
| stroke            |              4 |
| horsepower        |              3 |
| price             |              3 |
| horsepower-binned |              1 |

Permasalahan lain yang ditemukan:

1. Penulisan kategori tidak konsisten, misalnya perbedaan kapitalisasi dan spasi pada kolom 'make'.
2. Kolom 'body-style', 'drive-wheels', dan 'fuel-system' memiliki penulisan kategori yang tidak konsisten.
3. Kolom 'transaction_date' menggunakan beberapa format tanggal.
4. Kolom 'transaction_date' merupakan kolom tambahan yang tidak terdapat pada dataset original.

## 6. Data Cleaning

Metode cleaning yang diterapkan:

1. Menghapus spasi yang tidak diperlukan.
2. Menyeragamkan huruf pada data kategorikal.
3. Menghapus duplicate records.
4. Menghapus kolom 'transaction_date' setelah pemeriksaan duplikat.
5. Mengisi missing values numerik dengan median.
6. Mengisi missing values kategorikal dengan modus jika sesuai.
7. Mengisi missing values pada 'make' dengan kategori 'unknown'.

Alasan pemilihan metode:

- Pembersihan teks membantu menyeragamkan kategori yang sama.
- Penghapusan duplikat menghindari penghitungan data berulang.
- Median digunakan untuk mengisi nilai numerik yang kosong.
- Modus digunakan untuk mengisi kategori yang kosong.
- Kategori 'unknown' digunakan untuk merek yang tidak diketahui agar tidak menebak merek mobil.
- 'transaction_date' dihapus karena merupakan metadata tambahan, bukan karakteristik teknis mobil, dan format tanggalnya tidak konsisten.

Ringkasan cleaning:

- Baris sebelum cleaning: 205
- Baris sesudah cleaning: 201
- Missing values sebelum: 17
- Missing values sesudah: 0
- Duplicate records dihapus: 4

## 7. Data Transformation

### 7.1 Min-Max Scaling

Kolom yang ditransformasi:
- engine-size

Metode:
- Min-Max Scaling

Kolom hasil:
- engine-size_minmax

Alasan:
Min-Max Scaling digunakan untuk mengubah rentang nilai numerik menjadi rentang 0 sampai 1.

Contoh perbandingan:

| engine-size | engine-size_minmax |
| ----------- | ------------------ |
| 130         | 0.260377           |
| 130         | 0.260377           |
| 152         | 0.343396           |
| 152         | 0.343396           |
| 109         | 0.181132           | 
| 136         | 0.283019           |
| 136         | 0.283019           |
| 136         | 0.283019           | 
| 136         | 0.283019           |
| 131         | 0.264151           |
| 108         | 0.177358           |

### 7.2 One-Hot Encoding

Kolom yang diencoding:
- body-style

Metode:
- One-Hot Encoding

Alasan:
Metode ini mengubah kategori berbentuk teks menjadi kolom numerik tanpa memberikan urutan yang tidak semestinya kepada kategori.

Kolom hasil:
- body-style_convertible
- body-style_hardtop
- body-style_hatchback
- body-style_sedan
- body-style_wagon

## 8. Final Dataset

Nama file:
- automobileEDA_processed.csv

Lokasi:
- data/processed/automobileEDA_processed.csv

Jumlah baris setelah pemrosesan:
- 201

Jumlah kolom setelah pemrosesan:
- 35

## 9. ETL Pipeline

Pipeline terdiri dari tiga tahapan utama:

1. Extract: membaca dataset CSV dari folder 'data/raw/'.
2. Transform: memeriksa kualitas data, melakukan cleaning, dan menerapkan transformation.
3. Load: menyimpan dataset hasil ke folder 'data/processed/'.

Seluruh proses dijalankan melalui 'src/pipeline.py'.

## 10. Installation

Instal dependency menggunakan:

python -m pip install -r requirements.txt


## 11. How to Run

Jalankan perintah berikut dari folder utama project:

python src/pipeline.py


Pipeline akan membaca dataset mentah, melakukan inspection, cleaning, transformation, dan menyimpan hasilnya sebagai 'automobileEDA_processed.csv'.

## 12. Data Flow Diagram

Diagram alur data tersedia di:

'documentation/data-flow-diagram.png'
