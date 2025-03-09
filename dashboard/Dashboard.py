import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# Filtering
day_df["dateday"] = pd.to_datetime(day_df["dateday"])
hour_df["dateday"] = pd.to_datetime(hour_df["dateday"])

min_date = hour_df["dateday"].min()
max_date = hour_df["dateday"].max()

selected_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

# Apply filtering
filtered_day_df = day_df[
    (day_df["dateday"] >= pd.Timestamp(selected_date[0]))
    & (day_df["dateday"] <= pd.Timestamp(selected_date[1]))
]
filtered_hour_df = hour_df[
    (hour_df["dateday"] >= pd.Timestamp(selected_date[0]))
    & (hour_df["dateday"] <= pd.Timestamp(selected_date[1]))
]


# Processing methods
def get_total_casual_vs_registered():
    return filtered_day_df.groupby("year")[["casual", "registered"]].sum().reset_index()


def get_pola_penyewaan():
    return filtered_hour_df.groupby(by=["hour", "year"]).count_cr.sum().reset_index()


def get_total_penyewaan_per_musim():
    return (
        filtered_day_df.groupby(by=["season", "year"])
        .agg({"count_cr": "sum"})
        .reset_index()
    )


# Visualization Methods
def plot_total_casual_vs_registered():
    data = get_total_casual_vs_registered()
    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.3
    index = np.arange(len(data["year"]))
    p1 = ax.bar(index, data["casual"], bar_width, label="Total Casual")
    p2 = ax.bar(
        index + bar_width, data["registered"], bar_width, label="Total Registered"
    )

    for bars in [p1, p2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
            )

    ax.set_title("Total Casual vs Registered Users by Year")
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(data["year"])
    ax.legend()
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    plt.tight_layout()
    return fig


def plot_pola_penyewaan():
    data = get_pola_penyewaan()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=data,
        x="hour",
        y="count_cr",
        hue="year",
        marker="o",
        palette="bright",
        ax=ax,
    )
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Jam dan Tahun")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.legend(title="Tahun", loc="upper right")
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    return fig


def plot_total_penyewaan_per_musim():
    data = get_total_penyewaan_per_musim()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=data, x="season", y="count_cr", hue="year", palette="deep", ax=ax)
    ax.set_title("Total Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.legend(title="Tahun", loc="upper right")
    plt.tight_layout()
    return fig


# Layout Berurutan Kebawah
st.title("Dashboard Insight Penyewaan Sepeda (2011-2012)")


st.header("Tren Pengguna Baru vs. Kasual")
st.pyplot(plot_total_casual_vs_registered())
st.subheader("Insight")
st.write("""
- Jumlah pengguna baru lebih tinggi dibandingkan pengguna casual di kedua tahun
- Tren tertinggi penyewaan sepeda terjadi pada pengguna baru di tahun 2012, yaitu 1.304.046 lebih banyak dari pengguna casual""")


st.header("Pola Penyewaan Sepeda tiap Jam")
st.pyplot(plot_pola_penyewaan())
st.subheader("Insight")
st.write("""
- Jumlah penyewaan pada tahun 2012 meningkat signifikan dari tahun sebelumnya
- Jam tengah malam hingga subuh (00.00 - 05.00) memiliki penyewaan paling rendah
- Terjadi lonjakan penyewaan yang signifikan pada pagi (06:00 - 08:00) dan sore (16:00 - 17:00)
- penyewaan sepada terbanyak terjadi pada jam 17.00 sedangkan terendah terjadi pada jam 04.00""")

st.header("Total Penyewaan Sepeda Berdasarkan Musim")

st.pyplot(plot_total_penyewaan_per_musim())
st.subheader("Insight")
st.write("""
- Jumlah penyewaan pada tahun 2012 mengalami kenaikan yang signifikan dibanding tahun sebelumnya
- Jumlah penyewaan yang tinggi terjadi di musim gugur dan panas, pada musim ini kondisi cuaca mendukung aktivitas luar ruangan dan bisa jadi banyak orang menggunakan sepeda untuk berangkat kerja atau bersenang-senang
- Pada musim dingin, tidak lebih tinggi dari musim gugur dan panas
- Jumlah penyewaan cukup rendah pada musim semi karena cuaca yang tidak menentu""")

# Kesimpulan
st.subheader("Kesimpulan")
st.write(
    "- Pengguna baru lebih banyak dibandingkan pengguna casual, dengan peningkatan signifikan pada tahun 2012."
    "\n- Penyewaan sepeda meningkat di pagi (06:00 - 08:00) dan sore (16:00 - 17:00), dengan puncak pada pukul 17:00."
    "\n- Musim gugur dan panas menjadi periode dengan jumlah penyewaan tertinggi, sedangkan musim semi lebih rendah karena cuaca yang tidak menentu."
)
