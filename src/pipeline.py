from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# =========================================================
# 1. KONFIGURASI
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "automobileEDA_dirty_training.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "automobileEDA_processed.csv"
)


# =========================================================
# 2. EXTRACT: MEMBACA DATASET
# =========================================================

def load_data(file_path):
    """Membaca dataset mentah dari file CSV."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_path}\n"
            "Periksa nama dan lokasi file dataset."
        )

    df = pd.read_csv(file_path)

    # Membersihkan spasi pada nama kolom.
    df.columns = df.columns.str.strip()

    print("\n" + "=" * 60)
    print("EXTRACT: DATASET BERHASIL DIMUAT")
    print("=" * 60)

    print(f"Jumlah baris : {df.shape[0]}")
    print(f"Jumlah kolom : {df.shape[1]}")

    return df


# =========================================================
# 3. INSPECTION: MEMERIKSA KONDISI AWAL
# =========================================================

def inspect_data(df):
    """Menampilkan kondisi awal dataset."""

    print("\n" + "=" * 60)
    print("DATA INSPECTION")
    print("=" * 60)

    print("\n1. Lima baris pertama:")
    print(df.head().to_string())

    print("\n2. Ukuran dataset:")
    print(f"Baris  : {df.shape[0]}")
    print(f"Kolom  : {df.shape[1]}")

    print("\n3. Nama kolom:")
    print(df.columns.tolist())

    print("\n4. Tipe data:")
    print(df.dtypes.to_string())

    print("\n5. Missing values per kolom:")
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("Tidak ada missing values.")
    else:
        print(missing.to_string())

    print("\nTotal missing values:")
    print(int(df.isna().sum().sum()))

    print("\n6. Jumlah duplicate records:")
    print(int(df.duplicated().sum()))

    print("\n7. Nilai unik kolom kategorikal:")

    categorical_columns = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns

    for column in categorical_columns:
        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False).to_dict())


# =========================================================
# 4. CLEANING: MEMBERSIHKAN DATA
# =========================================================

def clean_data(df):
    """Membersihkan dataset berdasarkan temuan awal."""

    print("\n" + "=" * 60)
    print("DATA CLEANING")
    print("=" * 60)

    # Bekerja pada salinan agar data mentah tetap utuh.
    cleaned = df.copy()

    rows_before = len(cleaned)
    missing_before = int(cleaned.isna().sum().sum())
    duplicates_before = int(cleaned.duplicated().sum())

    # -----------------------------------------------------
    # B. BERSIHKAN PENULISAN TEKS
    # -----------------------------------------------------

    text_columns = cleaned.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    for column in text_columns:
        cleaned[column] = cleaned[column].map(
            lambda value: (
                " ".join(value.split()).lower()
                if isinstance(value, str)
                else value
            )
        )

    # -----------------------------------------------------
    # C. HAPUS DUPLIKAT
    # -----------------------------------------------------

    duplicates_before_removal = int(
        cleaned.duplicated().sum()
    )

    cleaned = cleaned.drop_duplicates().copy()

    # -----------------------------------------------------
    # A. HAPUS KOLOM TRANSACTION_DATE
    # -----------------------------------------------------

    # Kolom ini merupakan metadata tambahan, bukan atribut
    # karakteristik mobil dalam dataset original.
    if "transaction_date" in cleaned.columns:
        cleaned = cleaned.drop(columns=["transaction_date"])

        print(
            "\nKolom transaction_date dihapus karena "
            "merupakan metadata tambahan dan format "
            "tanggalnya tidak konsisten."
        )
        
    duplicates_removed = (
        duplicates_before_removal
    )

    # -----------------------------------------------------
    # D. TANGANI MISSING VALUES NUMERIK
    # -----------------------------------------------------

    numeric_columns = cleaned.select_dtypes(
        include=[np.number]
    ).columns.tolist()

    for column in numeric_columns:
        if cleaned[column].isna().any():
            median_value = cleaned[column].median()

            if pd.notna(median_value):
                cleaned[column] = cleaned[column].fillna(
                    median_value
                )

    # -----------------------------------------------------
    # E. TANGANI MISSING VALUES KATEGORIKAL
    # -----------------------------------------------------

    # Merek yang tidak diketahui tidak boleh ditebak.
    if "make" in cleaned.columns:
        cleaned["make"] = cleaned["make"].fillna("unknown")

    # Untuk kolom kategorikal lain, gunakan modus.
    categorical_columns = cleaned.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    for column in categorical_columns:
        if cleaned[column].isna().any():
            mode_values = cleaned[column].mode(
                dropna=True
            )

            if not mode_values.empty:
                cleaned[column] = cleaned[column].fillna(
                    mode_values.iloc[0]
                )

    # -----------------------------------------------------
    # F. LAPORKAN HASIL CLEANING
    # -----------------------------------------------------

    rows_after = len(cleaned)
    missing_after = int(cleaned.isna().sum().sum())

    print("\nRingkasan cleaning:")
    print(f"Baris sebelum       : {rows_before}")
    print(f"Baris sesudah       : {rows_after}")
    print(f"Kolom sebelum       : {df.shape[1]}")
    print(f"Kolom sesudah       : {cleaned.shape[1]}")
    print(f"Missing sebelum     : {missing_before}")
    print(f"Missing sesudah     : {missing_after}")
    print(f"Duplikat dihapus    : {duplicates_removed}")

    print("\nMissing values setelah cleaning:")
    print(cleaned.isna().sum().to_string())

    if cleaned.isna().sum().sum() > 0:
        raise ValueError(
            "Masih terdapat missing values. "
            "Periksa kembali proses cleaning."
        )

    print("\nCleaning berhasil.")

    return cleaned


# =========================================================
# 5. TRANSFORMATION: MIN-MAX SCALING DAN ENCODING
# =========================================================

def transform_data(df):
    """Melakukan scaling dan encoding."""

    print("\n" + "=" * 60)
    print("DATA TRANSFORMATION")
    print("=" * 60)

    transformed = df.copy()

    # -----------------------------------------------------
    # A. MIN-MAX SCALING PADA ENGINE-SIZE
    # -----------------------------------------------------

    scaling_column = "engine-size"

    if scaling_column not in transformed.columns:
        raise ValueError(
            f"Kolom {scaling_column} tidak ditemukan."
        )

    scaler = MinMaxScaler()

    scaled_column = f"{scaling_column}_minmax"

    transformed[scaled_column] = scaler.fit_transform(
        transformed[[scaling_column]]
    ).ravel()

    print("\nMin-Max Scaling:")
    print(f"Kolom asli  : {scaling_column}")
    print(f"Kolom baru  : {scaled_column}")

    print(
        transformed[
            [scaling_column, scaled_column]
        ].head(10).to_string(index=False)
    )

    # -----------------------------------------------------
    # B. ONE-HOT ENCODING PADA BODY-STYLE
    # -----------------------------------------------------

    encoding_column = "body-style"

    if encoding_column not in transformed.columns:
        raise ValueError(
            f"Kolom {encoding_column} tidak ditemukan."
        )

    encoded = pd.get_dummies(
        transformed[encoding_column],
        prefix=encoding_column,
        dtype=int
    )

    # Mempertahankan kolom body-style asli.
    transformed = pd.concat(
        [transformed, encoded],
        axis=1
    )

    print("\nOne-Hot Encoding:")
    print(f"Kolom asli: {encoding_column}")
    print("Kolom baru:")
    print(encoded.columns.tolist())

    print("\nContoh hasil encoding:")
    print(encoded.head(10).to_string(index=False))

    print("\nUkuran setelah transformation:")
    print(f"Baris : {transformed.shape[0]}")
    print(f"Kolom : {transformed.shape[1]}")

    return transformed


# =========================================================
# 6. LOAD: MENYIMPAN HASIL
# =========================================================

def save_data(df, output_path):
    """Menyimpan dataset hasil ke CSV."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 60)
    print("LOAD: DATASET BERHASIL DISIMPAN")
    print("=" * 60)

    print(f"File   : {output_path}")
    print(f"Baris  : {df.shape[0]}")
    print(f"Kolom  : {df.shape[1]}")


# =========================================================
# 7. MENJALANKAN SELURUH PIPELINE
# =========================================================

def main():
    """Menjalankan pipeline dari awal sampai akhir."""

    # EXTRACT
    raw_data = load_data(RAW_FILE)

    # INSPECTION
    inspect_data(raw_data)

    # CLEANING
    cleaned_data = clean_data(raw_data)

    # TRANSFORMATION
    processed_data = transform_data(cleaned_data)

    # LOAD
    save_data(processed_data, OUTPUT_FILE)

    print("\n" + "=" * 60)
    print("PIPELINE SELESAI")
    print("=" * 60)

    print("Dataset mentah tetap dipertahankan.")
    print("Processed dataset telah dibuat.")


if __name__ == "__main__":
    main()