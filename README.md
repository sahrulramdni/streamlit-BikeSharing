# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk menganalisis data peminjaman sepeda Capital Bikeshare Washington D.C. (2011-2012).

## Prasyarat

- Python 3.8 atau lebih baru
- Git (opsional, untuk clone repository)

## 🚀 Cara Menjalankan Dashboard

### 1. Clone Repository (Opsional)

```bash
git clone https://github.com/username/streamlit-bikesharing.git
cd streamlit-bikesharing
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Siapkan File Data
Pastikan struktur folder seperti berikut:

```bash
streamlit-bikesharing/
├── dashboard/
│   ├── data_1.csv          # Hourly data (data peminjaman per jam)
│   └── dashboard.py        # File dashboard utama
├── data/
│   ├── data_1.csv          # Hourly data (backup)
│   └── data_2.csv          # Daily data (data peminjaman per hari)
├── requirements.txt
└── README.md
```

Catatan:

- File data_1.csv adalah file hour.csv (data per jam)
- File data_2.csv adalah file day.csv (data per hari)

### 5. Jalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

### 6. Buka di Browser
Setelah menjalankan perintah di atas, akan muncul URL:

```bash
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Buka ```bash http://localhost:8501``` di browser Anda.

## 🛠️ Setup dengan Anaconda

```bash
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt
cd dashboard
streamlit run dashboard.py
```

## 🛠️ Setup dengan Pipenv

```bash
mkdir bike_sharing_dashboard
cd bike_sharing_dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
cd dashboard
streamlit run dashboard.py
```
