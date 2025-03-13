import streamlit as slt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO


st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df_hour = pd.read_csv("dashboard/hour_clean.csv")
    df_day = pd.read_csv("dashboard/day_clean.csv")
    df_hour['yr'] = df_hour['yr'] + 2011 
    return df_hour, df_day

df_hour, df_day = load_data()

st.title("📊 Bike Sharing Dashboard")

min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

# --- SIDEBAR --- #
with st.sidebar:
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    
df_day = df_day[(df_day["dteday"] >= str(start_date)) & 
                (df_day["dteday"] <= str(end_date))]

df_hour = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                (df_hour["dteday"] <= str(end_date))]


# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📌 Overview", "🌡️ Pengaruh Suhu", "📅 Trend Bulanan & Tahunan", "⏰ Trend Per Jam", "🌦️ Tren Berdasarkan Musim"])

# 📌 **TAB 1: Overview**
with tab1:
    st.subheader("🔍 Ringkasan Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_rentals = df_hour['cnt'].sum()
    avg_rentals = df_day['cnt'].mean()
    peak_hour = df_hour.groupby('hr')['cnt'].mean().idxmax()
    peak_day = df_day.groupby('dteday')['cnt'].mean().idxmax()

    
    col1.metric("Total Penyewaan", f"{total_rentals:,}")
    col2.metric("Rata-rata Penyewaan (Daily)", f"{avg_rentals:.2f}")
    col3.metric("Jam Tersibuk", f"{peak_hour}:00")
    col4.metric("Hari Tersibuk", f"{peak_day}")

# 🌡️ **TAB 2: Pengaruh Suhu, Kelembapan, dan Kecepatan Angin**
with tab2:
    st.subheader("🌡️ Pengaruh Suhu dengan Jumlah Penyewaan")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.regplot(data=df_day, x='temp', y='cnt', line_kws={'color':'red'})
    ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda")
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Total Jumlah Penyewaan Sepeda")
    ax.grid()
    # st.pyplot(fig)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.write("Tes korelasi menunjukkan bahwa suhu memiliki korelasi yang cukup kuat dengan jumlah penyewaan sepeda per-harinya.")
    st.write("""**Insight:**
- Korelasi antara suhu dengan jumlah penyewaan sepeda menunjukkan bahwa semakin hangat suhu pada suatu hari, maka ada kecenderungan bahwa akan lebih banyak orang yang menyewa sepeda pada hari itu.""")
   

# 📅 **TAB 3: Trend Bulanan & Tahunan**
with tab3:
    st.subheader("📅 Tren Penyewaan Sepeda per Tahun & Bulan")

    # 📈 **Yearly Trend**
    yearly_trend = df_day.groupby('yr')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=yearly_trend['yr']+2011, y=yearly_trend['cnt'], palette="coolwarm", ax=ax)
    ax.set_title("Tren Penyewaan Sepeda per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Total Penyewaan")
    # st.pyplot(fig)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    # 📆 **Monthly Trend**
    monthly_trend = df_hour.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=monthly_trend, marker="o", ax=ax)
    ax.set_xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    ax.set_title("Rata-rata Penyewaan Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend(title="Tahun")
    ax.grid()
    # st.pyplot(fig)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.write("""Visualisasi data penyewaan sepeda per jam menunjukkan adanya pola dimana:
- Penyewaan sepeda lebih rendah di bulan Januari dan Desember.
- Penyewaan meningkat mulai Maret, mencapai puncaknya antara Mei hingga September, kemudian turun lagi menjelang akhir tahun.
- Pada tahun 2012, jumlah penyewaan sepeda meningkat dibandingkan tahun 2011 di setiap bulan.""")
    
    st.write("""**Insight:**

- Dapat disimpulkan adanya tren peningkatan penggunaan sepeda dari tahun 2011 ke 2012, serta pola musiman di mana jumlah penyewaan lebih tinggi pada musim panas dan gugur, dan lebih rendah pada musim dingin dan semi. """)

# ⏰ **TAB 4: Trend Per Jam**
with tab4:
    st.subheader("Tren Penyewaan Sepeda per Jam")
    
    hourly_trend = df_hour.groupby('hr')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(x=hourly_trend['hr'], y=hourly_trend['cnt'], marker="o")
    ax.set_xticks(range(0, 24))
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    ax.grid()
    # st.pyplot(fig)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.write("""Visualisasi tren per jam menunjukkan adanya pola dimana:
- Penyewaan sangat rendah antara jam 00:00 - 05:00, dengan titik terendah sekitar jam 04:00 dengan 6.35 penyewaan.
- Terjadi peningkatan pada pukul 06.00 - 09.00, dengan lonjakan signifikan pada 08.00 - 09.00.
- Pada pukul 10.00 - 16.00 jumlah penyewaan relatif stabil dengan sedikit peningkatan.
- Terjadi peningkatan signifikan kedua pada 17.00 - 18.00, dengan titik tertinggi pada jam 18.00 dengan 461.45 penyewaan.
- Setelah pukul 19.00 penyewaan mulai turun drastis hingga mencapai titik terendah pada 23.00 dengan 87.83 penyewaan.""")
    
    st.write("""**Insight:**\n
Dapat disimpulkan adanya tren per jam dimana:
- Dua puncak utama penyewaan sepeda terjadi pada jam 08:00 (berangkat kerja/sekolah) dan 17:00 - 18:00 (pulang kerja/sekolah).
- Malam hingga dini hari memiliki penyewaan yang rendah, kemungkinan karena kurangnya aktivitas.
- Jumlah penyewaan antara 10:00 - 16:00 relatif stabil, kemungkinan digunakan untuk aktivitas seperti rekreasi atau keperluan bisnis.
             
             """)

# 🌦️ **TAB 5: Tren Berdasarkan Musim (Binning)**
with tab5:
    st.subheader("🌦️ Tren Penyewaan Berdasarkan Musim (Binning)")

    seasonal_trend = df_hour.groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=seasonal_trend, x='season', y='cnt', palette='coolwarm', ax=ax)

    ax.set_xlabel('Musim')  
    ax.set_xticks(range(0, 4), ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
    ax.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax.set_title('Tren Penyewaan Sepeda Berdasarkan Musim')
    # st.pyplot(fig)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.write("""Dari hasil binning, diketahui bahwa musim semi memiliki jumlah paling sedikit penyewaan sepeda, sedangkan jumlah penyewaan tertinggi ada pada musim gugur.""")

