import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

#update
# Set page configuration
st.set_page_config(
    page_title="Dashboard Visualisasi Data Barang Keluar",
    page_icon="l.web.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
file_path = 'okee_dummy_data permintaan pelanggan dari gudang.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Rename columns
data.rename(columns={
    'nama divisi': 'nm div',
    'divisi': 'anm_div',
    'sub divisi': 'subdivisi'
}, inplace=True)

# Convert 'tanggal' to datetime
data['tanggal'] = pd.to_datetime(data['tanggal'], format='%d/%m/%Y').dt.date

# Sidebar
st.sidebar.image("654db0b264142 (1).webp", width=120)
st.sidebar.title("📊 PT Bakrie Pipe Industries")
st.sidebar.subheader("Dashboard Visualisasi Data Barang Keluar")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Fungsi untuk mendapatkan tanggal terakhir suatu bulan
def get_last_day_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)  # Lompat ke bulan berikutnya
    return next_month - timedelta(days=next_month.day)    # Mundur ke hari terakhir bulan sebelumnya

# Default mode and date range
mode = "Dark"
# Simulasikan tahun 2024
current_date = datetime(2024, datetime.now().month, datetime.now().day).date()

# Hari pertama bulan ini
default_start_date = current_date.replace(day=1)

# Tambahkan 2 bulan untuk mencapai akhir bulan ke-3 (termasuk bulan saat ini)
last_month = default_start_date + relativedelta(months=2)
default_end_date = get_last_day_of_month(last_month)

# Output hasil
print("Mode:", mode)
print("Current Date:", current_date)
print("Default Start Date:", default_start_date)
print("Default End Date:", default_end_date)


# Mode selector
mode = st.sidebar.radio(
    "Pilih Mode Tampilan:",
    options=["Light", "Dark"],
    index=1
)

# Set template based on mode
template = "plotly_white" if mode == "Light" else "plotly_dark"
background_color = "#ffffff" if mode == "Light" else "#222222"
font_color = "#000000" if mode == "Light" else "#ffffff"

# Date range filters
start_date = st.sidebar.date_input(
    "Tanggal Mulai:",
    default_start_date
)
end_date = st.sidebar.date_input(
    "Tanggal Akhir:",
    default_end_date
)

# nm div filter
nm_div_options = ['Semua Divisi'] + list(data['nm div'].unique())
selected_nm_div = st.sidebar.selectbox(
    "Pilih Nama Divisi:",
    options=nm_div_options
)

# anm_div and subdivisi filters (depend on selected nm div)
if selected_nm_div == 'Semua Divisi':
    filtered_nm_div_data = data
else:
    filtered_nm_div_data = data[data['nm div'] == selected_nm_div]

anm_div_options = filtered_nm_div_data['anm_div'].unique()
selected_anm_div = st.sidebar.multiselect(
    "Alokasi Nama Divisi {anm_div}",
    options=anm_div_options,
    default=anm_div_options
)

subdivisi_options = filtered_nm_div_data[filtered_nm_div_data['anm_div'].isin(selected_anm_div)]['subdivisi'].unique()
selected_subdivisi = st.sidebar.multiselect(
    "Pilih Sub Divisi:",
    options=subdivisi_options,
    default=subdivisi_options
)

# Default view if search has not been clicked
if 'search_clicked' not in st.session_state:
    st.session_state['search_clicked'] = False

if 'top_items_limit' not in st.session_state:
    st.session_state['top_items_limit'] = 3

# Search button
if st.sidebar.button("Search"):
    st.session_state['search_clicked'] = True
    st.session_state['top_items_limit'] = 3  # Reset to initial limit on new search

if not st.session_state['search_clicked']:
    st.markdown(
        f"""
        <div style="background-color:{background_color}; padding:15px; border-radius:10px;">
        <h1 style="color:{font_color};">🌟 Selamat Datang di Dashboard Visualisasi Data Barang Keluar</h1>
        <p style="color:{font_color};"> <b> Hari ini = </b> {datetime.now().strftime('%A, %d %B %Y')}</p>
        <p style="color:{font_color};"><b>Cara Penggunaan</b></p>
        <ul>
            <li style="color:{font_color};">Gunakan filter di sebelah kiri.</li>
            <li style="color:{font_color};">Klik tombol <b>'Search'</b> untuk melihat hasil visualisasi data.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(f"<h2 style='color:{font_color};'>🎯 Berikut hasil visualisasi data berdasarkan pencarian Anda!</h2>", unsafe_allow_html=True)

    # Apply filters
    filtered_data = data[
        (data['tanggal'] >= start_date) &
        (data['tanggal'] <= end_date) &
        ((selected_nm_div == 'Semua Divisi') | (data['nm div'] == selected_nm_div)) &
        (data['anm_div'].isin(selected_anm_div)) &
        (data['subdivisi'].isin(selected_subdivisi))
    ]

    # Search by nomor barang
    selected_nomor_barang = st.text_input("(Jika ingin mencari Berdasarkan Nomor Barang):", key="nomor_barang_filter")
    filtered_data = filtered_data[filtered_data['nomor barang'].str.contains(selected_nomor_barang, case=False, na=False)]

# Line chart: Tren permintaan berdasarkan tanggal
    st.markdown(f"<h3 style='color:{font_color};'>✨ Tren Permintaan Barang</h3>", unsafe_allow_html=True)
    line_chart = px.line(
        filtered_data.groupby('tanggal')['jumlah'].sum().reset_index(),
        x='tanggal',
        y='jumlah',
        title=None,
        labels={'jumlah': 'Jumlah Permintaan', 'tanggal': 'Tanggal'},
        template=template,
        markers=True
    )
    st.plotly_chart(line_chart, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Grafik ini menunjukkan perubahan jumlah permintaan barang berdasarkan waktu. Naik turunnya garis mencerminkan tingkat permintaan pada tanggal tertentu.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)


    # Display all filtered data
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>📋 Data Terfilter</h2>", unsafe_allow_html=True)
    columns_to_display = ['tanggal', 'nomor barang', 'nama barang', 'jumlah', 'satuan', 'nm div', 'anm_div', 'subdivisi']
    filtered_data.reset_index(drop=True, inplace=True)
    filtered_data.index += 1
    st.dataframe(filtered_data[columns_to_display])

    # Display top items summary with dynamic limit
    st.markdown("<h2 style='text-align: center;'>📋 Ringkasan Data</h2>", unsafe_allow_html=True)
    top_items = filtered_data.groupby('nomor barang').agg({'jumlah': 'sum'}).reset_index().sort_values(by='jumlah', ascending=False).head(st.session_state['top_items_limit'])
    top_items.reset_index(drop=True, inplace=True)
    top_items.index += 1
    st.table(top_items)

    if len(filtered_data.groupby('nomor barang')) > st.session_state['top_items_limit']:
        if st.button("Lihat lebih banyak"):
            st.session_state['top_items_limit'] += 3
            top_items = filtered_data.groupby('nomor barang').agg({'jumlah': 'sum'}).reset_index().sort_values(by='jumlah', ascending=False).head(st.session_state['top_items_limit'])
            top_items.reset_index(drop=True, inplace=True)
            top_items.index += 1
            st.table(top_items)

    # Visualization
    st.markdown("<h2 style='text-align: center;'>📈 Visualisasi Data</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""<div style='text-align: justify; margin-top: 10px; margin-bottom: 20px; font-size: 16px;'>
        Bagian ini menyajikan berbagai visualisasi data yang dirancang untuk memberikan pemahaman mendalam tentang pola, tren, dan distribusi data barang keluar. Dengan memanfaatkan grafik ini, Anda dapat menganalisis informasi penting, seperti tren permintaan, distribusi jumlah barang, hingga kontribusi setiap divisi atau sub divisi. Tujuannya adalah membantu Anda dalam pengambilan keputusan berbasis data secara lebih efektif dan efisien.
        </div>""",
        unsafe_allow_html=True
    )


    # Bar chart: Jumlah barang per anm_div dan subdivisi
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>📊 Jumlah Barang per Tanggal dan Alokasi Nama Divisi</h3>", unsafe_allow_html=True)
    bar_chart = px.bar(
        filtered_data.groupby(['tanggal', 'anm_div'])['jumlah'].sum().reset_index(),
        x='tanggal',
        y='jumlah',
        color='anm_div',
        title=None,
        labels={'jumlah': 'Total Jumlah', 'anm_div': 'Alokasi Nama Divisi', 'tanggal': 'Tanggal'},
        template=template
    )
    st.plotly_chart(bar_chart, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Grafik batang untuk membandingkan jumlah barang yang digunakan oleh divisi pada tanggal tertentu.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Pie chart: Contribution of anm_div
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>🍰 Persentase Jumlah per Tanggal</h3>", unsafe_allow_html=True)
    pie_chart = px.pie(
        filtered_data.groupby('tanggal')['jumlah'].sum().reset_index(),
        names='tanggal',
        values='jumlah',
        title=None,
        labels={'jumlah': 'Jumlah', 'tanggal': 'Tanggal'},
        template=template
    )
    st.plotly_chart(pie_chart, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Diagram lingkaran untuk melihat kontribusi setiap tanggal terhadap total permintaan barang.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Heatmap: Penggunaan Barang per Tanggal dan Sub Divisi
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>🌡️ Heatmap Penggunaan Barang per Tanggal dan Sub Divisi</h3>", unsafe_allow_html=True)
    heatmap_data = filtered_data.groupby(['tanggal', 'subdivisi'])['jumlah'].sum().reset_index()
    heatmap = px.density_heatmap(
        heatmap_data,
        x='tanggal',
        y='subdivisi',
        z='jumlah',
        title=None,
        labels={'jumlah': 'Jumlah', 'tanggal': 'Tanggal', 'subdivisi': 'Sub Divisi'},
        color_continuous_scale='Viridis',
        template=template
    )
    st.plotly_chart(heatmap, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Menunjukkan intensitas jumlah barang yang digunakan pada tanggal tertentu oleh subdivisi.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Scatterplot: Tanggal vs Jumlah Permintaan
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>🔹 Scatterplot Tanggal vs Jumlah Permintaan</h3>", unsafe_allow_html=True)
    scatter_plot = px.scatter(
        filtered_data,
        x='tanggal',
        y='jumlah',
        title=None,
        labels={'tanggal': 'Tanggal', 'jumlah': 'Jumlah Permintaan'},
        color='anm_div',
        hover_data=['subdivisi'],
        template=template
    )
    st.plotly_chart(scatter_plot, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Menampilkan hubungan antara tanggal dan jumlah permintaan barang, membantu mendeteksi pola dan anomali.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Boxplot: Distribusi Jumlah per Tanggal
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>📦 Distribusi Jumlah per Tanggal</h3>", unsafe_allow_html=True)
    box_plot = px.box(
        filtered_data,
        x='tanggal',
        y='jumlah',
        title=None,
        labels={'tanggal': 'Tanggal', 'jumlah': 'Jumlah Permintaan'},
        color='tanggal',
        template=template
    )
    st.plotly_chart(box_plot, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Boxplot untuk menganalisis distribusi permintaan barang pada berbagai tanggal, termasuk nilai ekstrem.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Histogram: Distribusi Jumlah Permintaan per Tanggal
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>📊 Distribusi Jumlah Permintaan per Tanggal</h3>", unsafe_allow_html=True)
    histogram = px.histogram(
        filtered_data,
        x='tanggal',
        y='jumlah',
        nbins=20,
        title=None,
        labels={'tanggal': 'Tanggal', 'jumlah': 'Jumlah Permintaan'},
        color='tanggal',
        template=template
    )
    st.plotly_chart(histogram, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Histogram yang menunjukkan pola distribusi permintaan barang pada tanggal tertentu.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)

    # Violin Plot: Jumlah per Tanggal
    st.markdown(f"<div style='border: 1px solid {font_color}; padding: 15px; margin-bottom: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{font_color};'>🎻 Violin Plot Jumlah Permintaan per Tanggal</h3>", unsafe_allow_html=True)
    violin_plot = px.violin(
        filtered_data,
        x='tanggal',
        y='jumlah',
        title=None,
        labels={'tanggal': 'Tanggal', 'jumlah': 'Jumlah Permintaan'},
        color='tanggal',
        box=True,
        points="all",
        template=template
    )
    st.plotly_chart(violin_plot, use_container_width=True)
    st.markdown(
        f"""<div style='background-color:{background_color}; padding:10px; border-radius:10px;'>
        <b style='color:{font_color};'>Penjelasan:</b> Memberikan distribusi mendetail dari jumlah permintaan barang per tanggal.
        </div>""",
        unsafe_allow_html=True
    )
    st.markdown(f"</div>", unsafe_allow_html=True)