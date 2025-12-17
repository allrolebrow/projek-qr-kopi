import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import time

# --- 1. KONFIGURASI HALAMAN (MODERN UI) ---
st.set_page_config(
    page_title="AntiInflam Traceability",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS CUSTOM (Agar Tampilan Lebih Cantik) ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    h1 {
        color: #4b2c20; /* Warna Kopi */
    }
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #c3e6cb;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI LOAD DATA ---
def get_data():
    try:
        return pd.read_csv('data_mutu.csv')
    except:
        return pd.DataFrame()

df = get_data()

# --- HEADER APLIKASI (BAGIAN YANG SUDAH DIPERBAIKI) ---
# Menggunakan width (lebar) bukan height (tinggi)
st.image("https://img.freepik.com/free-vector/coffee-production-concept-illustration_114360-6395.jpg?w=826", width=250)

st.title("🛡️ AntiInflam Traceability")
st.markdown("**Sistem Kontrol Mutu Berbasis Nano-Technology & IT**")
st.divider()

# --- LOGIKA NAVIGASI ---
tab1, tab2 = st.tabs(["🔍 SCAN / LACAK MUTU", "⚙️ ADMIN PANEL"])

# =========================================
# TAB 1: TAMPILAN KONSUMEN (HP USER)
# =========================================
with tab1:
    query_params = st.query_params
    batch_url = query_params.get("batch", None)

    col_input, col_btn = st.columns([3,1])
    with col_input:
        input_val = batch_url if batch_url else ""
        cari_batch = st.text_input("Batch ID:", value=input_val, placeholder="Contoh: NANO-001")
    
    with col_btn:
        st.write("") 
        st.write("") 
        cari_btn = st.button("🔍 Cek", type="primary")

    if cari_batch:
        hasil = df[df['Batch_ID'] == cari_batch]

        if not hasil.empty:
            data = hasil.iloc[0]
            
            with st.spinner('Menganalisis Blockchain Data...'):
                time.sleep(0.8) 

            st.markdown(f"""
            <div class="success-box">
                <b>✅ TERVERIFIKASI:</b> Produk Asli AntiInflam Coffee NanoCaps.<br>
                Diproduksi pada: {data['Tanggal_Produksi']}
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📍 Asal-Usul (Traceability)")
            st.info(f"**Sumber Kopi:** {data['Sumber_Kopi']}\n\n**Rempah:** {data['Varietas_Rempah']}")

            st.subheader("🔬 Kualitas Bioaktif (Lab Result)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Ukuran Nano", f"{data['Ukuran_Partikel_nm']} nm", "Optimal <200nm")
            with col2:
                st.metric("Total Fenolik", f"{data['Total_Fenolik']} mg/g", "Antioksidan")
            with col3:
                st.metric("Anti-Inflamasi", f"{data['Aktivitas_Anti_Inflamasi']}%", "Sangat Tinggi")

            st.subheader("📊 Performa vs Produk Biasa")
            chart_data = pd.DataFrame({
                'Kategori': ['Produk Ini', 'Kopi Biasa', 'Minuman Vitamin C'],
                'Kadar Anti-Inflamasi (%)': [data['Aktivitas_Anti_Inflamasi'], 40, 95]
            })
            st.bar_chart(chart_data, x='Kategori', y='Kadar Anti-Inflamasi (%)', color='#4b2c20')

        else:
            st.error("❌ Data Batch tidak ditemukan! Mohon cek kode pada kemasan.")

    else:
        st.info("Silakan scan QR Code pada kemasan atau masukkan kode Batch ID secara manual.")

# =========================================
# TAB 2: TAMPILAN ADMIN (PEMBUAT QR)
# =========================================
with tab2:
    st.write("### 🖨️ Generator QR Code")
    st.caption("Pilih batch produksi untuk mencetak label.")
    
    pilihan = st.selectbox("Pilih Batch ID:", df['Batch_ID'])
    
    base_url = st.text_input("URL Aplikasi (Link Web):", "http://192.168.1.5:8501") 
    
    if st.button("Buat QR Code"):
        full_link = f"{base_url}?batch={pilihan}"
        
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(full_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf)
        
        c1, c2 = st.columns([1,2])
        with c1:
            st.image(buf, width=200, caption=f"QR: {pilihan}")
        with c2:
            st.success("Gambar QR Siap!")
            st.code(full_link, language="text")
            st.info("Klik kanan pada gambar -> 'Save Image As' untuk menyimpan dan print.")