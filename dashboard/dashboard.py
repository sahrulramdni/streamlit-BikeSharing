import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_hourly_data():
    """Load hourly data dari dashboard/data_1.csv"""
    # Cek beberapa kemungkinan lokasi file
    possible_paths = [
        'dashboard/data_1.csv',      # Lokasi utama
        'data_1.csv',                 # Dalam folder dashboard
        '../dashboard/data_1.csv',    # Relative path
        'data/data_1.csv',            # Backup di folder data
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            st.success(f"✅ Load hourly data dari: {path}")
            df = pd.read_csv(path)
            df['dteday'] = pd.to_datetime(df['dteday'])
            
            # Tambahkan kolom waktu
            df['year'] = df['dteday'].dt.year
            df['month'] = df['dteday'].dt.month
            df['month_name'] = df['dteday'].dt.month_name()
            df['day'] = df['dteday'].dt.day
            df['day_name'] = df['dteday'].dt.day_name()
            
            # Mapping label
            season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
            weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
            day_type_map = {1: 'Working Day', 0: 'Weekend/Holiday'}
            
            df['season_label'] = df['season'].map(season_map)
            df['weather_label'] = df['weathersit'].map(weather_map)
            df['day_type'] = df['workingday'].map(day_type_map)
            
            return df
    
    st.error("❌ File data_1.csv (hourly data) tidak ditemukan!")
    st.info("Pastikan file 'data_1.csv' ada di folder 'dashboard/'")
    return pd.DataFrame()

@st.cache_data
def load_daily_data():
    """Load daily data dari data/data_2.csv"""
    possible_paths = [
        'data/data_2.csv',           # Lokasi utama
        'dashboard/data_2.csv',      # Backup di dashboard
        '../data/data_2.csv',        # Relative path
        'data_2.csv',                # Dalam folder yang sama
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            st.success(f"✅ Load daily data dari: {path}")
            df = pd.read_csv(path)
            df['dteday'] = pd.to_datetime(df['dteday'])
            df['year'] = df['dteday'].dt.year
            df['month_name'] = df['dteday'].dt.month_name()
            
            # Mapping label
            season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
            weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
            day_type_map = {1: 'Working Day', 0: 'Weekend/Holiday'}
            
            df['season_label'] = df['season'].map(season_map)
            df['weather_label'] = df['weathersit'].map(weather_map)
            df['day_type'] = df['workingday'].map(day_type_map)
            
            return df
    
    st.warning("⚠️ File data_2.csv (daily data) tidak ditemukan, beberapa fitur mungkin terbatas.")
    return pd.DataFrame()

# Load data
hourly_df = load_hourly_data()
daily_df = load_daily_data()

# Stop jika data tidak ditemukan
if hourly_df.empty:
    st.stop()

# ============================================
# SIDEBAR FILTER
# ============================================
st.sidebar.title("🚲 Bike Sharing Dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filter Data")

# Filter Tahun
years = sorted(hourly_df['year'].unique())
selected_year = st.sidebar.multiselect(
    "📅 Tahun",
    options=years,
    default=years
)

# Filter Musim
seasons = sorted(hourly_df['season_label'].dropna().unique())
selected_season = st.sidebar.multiselect(
    "🍂 Musim",
    options=seasons,
    default=seasons
)

# Filter Kondisi Cuaca
weathers = sorted(hourly_df['weather_label'].dropna().unique())
selected_weather = st.sidebar.multiselect(
    "🌤️ Kondisi Cuaca",
    options=weathers,
    default=weathers
)

# Filter Tipe Hari
day_types = sorted(hourly_df['day_type'].dropna().unique())
selected_day_type = st.sidebar.multiselect(
    "📆 Tipe Hari",
    options=day_types,
    default=day_types
)

# Apply Filters
filtered_df = hourly_df[
    (hourly_df['year'].isin(selected_year)) &
    (hourly_df['season_label'].isin(selected_season)) &
    (hourly_df['weather_label'].isin(selected_weather)) &
    (hourly_df['day_type'].isin(selected_day_type))
]

# Filter untuk daily data jika ada
if not daily_df.empty:
    filtered_daily = daily_df[
        (daily_df['year'].isin(selected_year)) &
        (daily_df['season_label'].isin(selected_season)) &
        (daily_df['weather_label'].isin(selected_weather)) &
        (daily_df['day_type'].isin(selected_day_type))
    ]
else:
    filtered_daily = pd.DataFrame()

# ============================================
# METRIK UTAMA
# ============================================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis Peminjaman Sepeda Capital Bikeshare Washington D.C. (2011-2012)")
st.markdown("---")

# Hitung metrik
total_rentals = filtered_df['cnt'].sum()
avg_rentals = filtered_df['cnt'].mean()
max_rentals = filtered_df['cnt'].max()
total_hours = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Peminjaman", f"{total_rentals:,.0f}")
with col2:
    st.metric("⏱️ Rata-rata per Jam", f"{avg_rentals:.0f}")
with col3:
    st.metric("🔥 Peminjaman Tertinggi", f"{max_rentals:,.0f}")
with col4:
    st.metric("🕐 Total Data (Jam)", f"{total_hours:,}")

st.markdown("---")

# ============================================
# PREVIEW DATA (Opsional)
# ============================================
with st.expander("📋 Preview Data (10 baris pertama)"):
    st.dataframe(filtered_df.head(10))

st.markdown("---")

# ============================================
# VISUALISASI 1: PEAK HOUR ANALYSIS
# ============================================
st.header("⏰ Analisis Peak Hour pada Hari Kerja")
st.markdown("Visualisasi ini menjawab pertanyaan: *Jam berapa peak hour yang menyumbang 70% peminjaman?*")

# Filter untuk hari kerja
workingday_df = filtered_df[filtered_df['day_type'] == 'Working Day']

if len(workingday_df) > 0:
    # Hitung total per jam
    hourly_total = workingday_df.groupby('hr')['cnt'].sum().reset_index()
    hourly_total.columns = ['hour', 'total_cnt']
    hourly_total['percentage'] = (hourly_total['total_cnt'] / hourly_total['total_cnt'].sum()) * 100
    hourly_total['cumulative_pct'] = hourly_total['percentage'].cumsum()
    hourly_total['is_peak'] = hourly_total['cumulative_pct'] <= 70
    
    peak_hours = hourly_total[hourly_total['is_peak']]['hour'].tolist()
    peak_contribution = hourly_total[hourly_total['is_peak']]['percentage'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Jumlah Peak Hours", f"{len(peak_hours)} jam", 
                  help=f"Jam: {', '.join([f'{h:02d}:00' for h in peak_hours])}")
    with col2:
        st.metric("Kontribusi Peak Hours", f"{peak_contribution:.1f}%")
    
    # Bar Chart dengan Plotly
    colors = ['coral' if is_peak else 'steelblue' for is_peak in hourly_total['is_peak']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=hourly_total['hour'],
        y=hourly_total['total_cnt'],
        marker_color=colors,
        text=hourly_total['total_cnt'],
        textposition='outside',
        name='Total Peminjaman'
    ))
    fig.add_hline(y=hourly_total['total_cnt'].mean(), line_dash="dash", line_color="green",
                  annotation_text=f"Rata-rata: {hourly_total['total_cnt'].mean():.0f}")
    fig.update_layout(
        title='Total Peminjaman per Jam pada Hari Kerja',
        xaxis_title='Jam',
        yaxis_title='Total Peminjaman (2 Tahun)',
        xaxis=dict(tickmode='linear', tick0=0, dtick=2),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Info insight
    st.info(f"💡 **Insight**: {len(peak_hours)} jam pertama (jam {peak_hours[0]:02d}:00 - {peak_hours[-1]:02d}:00) "
            f"menyumbang {peak_contribution:.1f}% dari total peminjaman pada hari kerja. "
            f"Puncak tertinggi terjadi pada jam 08:00 pagi dan jam 17:00-18:00 sore.")
else:
    st.warning("Tidak ada data untuk hari kerja dengan filter yang dipilih.")

st.markdown("---")

# ============================================
# VISUALISASI 2: DAMPAK CUACA
# ============================================
st.header("🌤️ Dampak Cuaca pada Akhir Pekan di Musim Gugur")
st.markdown("Visualisasi ini menjawab pertanyaan: *Faktor cuaca apa yang menyebabkan penurunan >50%?*")

# Filter untuk akhir pekan di musim gugur
weekend_fall = filtered_df[(filtered_df['day_type'] == 'Weekend/Holiday') & 
                           (filtered_df['season_label'] == 'Fall')]

if len(weekend_fall) > 0:
    # Analisis per kondisi cuaca
    weather_impact = weekend_fall.groupby('weather_label')['cnt'].agg(['mean', 'count']).reset_index()
    weather_impact.columns = ['weather_label', 'mean_cnt', 'count']
    
    # Hitung baseline dan penurunan
    baseline = weather_impact[weather_impact['weather_label'] == 'Clear']['mean_cnt'].values[0]
    weather_impact['decline_pct'] = ((baseline - weather_impact['mean_cnt']) / baseline) * 100
    weather_impact['decline_pct'] = weather_impact['decline_pct'].clip(lower=0)
    
    # Bar Chart
    fig = px.bar(
        weather_impact,
        x='weather_label',
        y='mean_cnt',
        color='mean_cnt',
        color_continuous_scale='RdYlGn_r',
        title='Rata-rata Peminjaman per Kondisi Cuaca',
        labels={'weather_label': 'Kondisi Cuaca', 'mean_cnt': 'Rata-rata Peminjaman'}
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot humidity vs count
    fig2 = px.scatter(
        weekend_fall,
        x='hum',
        y='cnt',
        color='weather_label',
        title='Hubungan Kelembaban vs Jumlah Peminjaman',
        labels={'hum': 'Kelembaban', 'cnt': 'Jumlah Peminjaman'},
        color_discrete_map={'Clear': '#2ecc71', 'Mist': '#f39c12', 'Light Rain/Snow': '#e74c3c'}
    )
    fig2.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Batas Kritis 100")
    fig2.add_vline(x=0.75, line_dash="dash", line_color="purple", annotation_text="Kelembaban Kritis 0.75")
    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Info insight
    rain_data = weather_impact[weather_impact['weather_label'] == 'Light Rain/Snow']
    if len(rain_data) > 0:
        st.info(f"💡 **Insight**: Pada akhir pekan di musim gugur, cuaca hujan ringan menurunkan peminjaman "
                f"hingga {rain_data['decline_pct'].values[0]:.1f}% dibandingkan cuaca cerah. "
                f"Kelembaban tinggi (>0.75) menjadi indikator kritis penurunan permintaan.")
else:
    st.warning("Tidak ada data untuk akhir pekan di musim gugur dengan filter yang dipilih.")

st.markdown("---")

# ============================================
# VISUALISASI 3: PERBANDINGAN HARI KERJA VS AKHIR PEKAN
# ============================================
st.header("📆 Perbandingan Pola: Hari Kerja vs Akhir Pekan")

# Prepare data
hourly_pattern = filtered_df.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()

fig = px.line(
    hourly_pattern,
    x='hr',
    y='cnt',
    color='day_type',
    title='Perbandingan Pola Peminjaman: Hari Kerja vs Akhir Pekan/Libur',
    labels={'hr': 'Jam', 'cnt': 'Rata-rata Jumlah Peminjaman'},
    markers=True
)
fig.add_vrect(x0=7, x1=9, line_width=0, fillcolor="blue", opacity=0.1, annotation_text="Morning Peak")
fig.add_vrect(x0=17, x1=19, line_width=0, fillcolor="orange", opacity=0.1, annotation_text="Evening Peak")
fig.add_vrect(x0=12, x1=14, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Afternoon Peak")
fig.update_layout(height=500, xaxis=dict(tickmode='linear', tick0=0, dtick=2))
st.plotly_chart(fig, use_container_width=True)

st.info("💡 **Insight**: Hari kerja memiliki dua puncak (pagi dan sore) mencerminkan perilaku komuter, "
        "sedangkan akhir pekan memiliki puncak di siang hari mencerminkan penggunaan rekreasi.")

st.markdown("---")

# ============================================
# REKOMENDASI
# ============================================
st.header("💡 Rekomendasi Strategis")

tab1, tab2, tab3 = st.tabs(["📌 Operasional Rebalancing", "📌 Mitigasi Cuaca", "📌 Program Loyalitas"])

with tab1:
    st.markdown("""
    ### Optimalisasi Operasional Berdasarkan Peak Hour
    
    | Jam | Aksi yang Direkomendasikan |
    |-----|---------------------------|
    | **06.00 - 07.00** | Mulai rebalancing sepeda dari pusat kota ke pemukiman |
    | **07.00 - 09.00** | Tambah staf di stasiun tersibuk, pastikan ketersediaan sepeda |
    | **15.00 - 16.00** | Mulai rebalancing sepeda dari pemukiman ke pusat kota |
    | **17.00 - 19.00** | Tambah staf, pastikan stasiun pusat kota memiliki cukup sepeda |
    
    **Target**: Mengurangi keluhan "sepeda habis" di jam sibuk hingga 50%
    """)

with tab2:
    st.markdown("""
    ### Strategi Mitigasi Dampak Cuaca
    
    | Kondisi Cuaca | Action Item |
    |---------------|-------------|
    | **☀️ Cerah** | Fokus pada promosi "Day Pass" dan rute wisata |
    | **🌫️ Berkabut** | Kirim notifikasi "Foggy Ride - Double Points!" diskon 10% |
    | **🌧️ Hujan Ringan** | Promo "Rainy Day Special" diskon 20% + jas hujan gratis |
    | **⛈️ Hujan Lebat** | Alihkan promosi ke layanan ride-hailing partner |
    
    **Target**: Meningkatkan peminjaman pada cuaca buruk hingga 30%
    """)

with tab3:
    st.markdown("""
    ### Program Loyalitas Pengguna
    
    1. **Weather Guarantee Program**
       - Refund 100% jika hujan dalam 30 menit setelah peminjaman
       - Membangun kepercayaan pengguna
    
    2. **Peak Hour Member Discount**
       - Diskon khusus untuk peminjaman di jam non-peak (10:00-16:00)
       - Mendistribusikan beban operasional
    
    3. **Seasonal Pass**
       - Paket berlangganan musiman dengan harga lebih murah
       - Khusus untuk musim gugur (peminjaman tertinggi)
    
    **Target**: Meningkatkan retensi pelanggan hingga 40%
    """)

st.markdown("---")
st.caption("Dashboard ini dibuat untuk proyek akhir analisis data | Dataset: Capital Bikeshare (2011-2012)")
st.caption(f"Terakhir diupdate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
