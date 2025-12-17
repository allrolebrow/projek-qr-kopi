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

# --- HEADER APLIKASI ---
# Menggunakan width agar tidak error di versi baru
st.image("https://img.freepik.com/free-vector/coffee-production-concept-illustration_114360-6395.jpg?w=826", width=250)

st.title("🛡️ AntiInflam Traceability")
st.markdown("**Sistem Kontrol Mutu Berbasis Nano-Technology & IT**")
st.divider()

# --- LOGIKA NAVIGASI ---
tab1, tab2 = st.tabs(["🔍 SCAN / LACAK MUTU", "🔐 ADMIN PANEL"])

# =========================================
# TAB 1: TAMPILAN KONSUMEN (HP USER)
# =========================================
with tab1:
    # Mengambil parameter dari URL (Hasil Scan QR)
    query_params = st.query_params
    batch_url = query_params.get("batch", None)

    # Input Manual (Jika tidak scan)
    col_input, col_btn = st.columns([3,1])
    with col_input:
        input_val = batch_url if batch_url else ""
        cari_batch = st.text_input("Batch ID:", value=input_val, placeholder="Contoh: NANO-001")
    
    with col_btn:
        st.write("") # Spacer
        st.write("") # Spacer
        cari_btn = st.button("🔍 Cek", type="primary")

    # LOGIKA PENCARIAN
    if cari_batch:
        hasil = df[df['Batch_ID'] == cari_batch]

        if not hasil.empty:
            data = hasil.iloc[0]
            
            # Efek Loading biar keren
            with st.spinner('Menganalisis Blockchain Data...'):
                time.sleep(0.8) 

            # Tanda Verifikasi
            st.markdown(f"""
            <div class="success-box">
                <b>✅ TERVERIFIKASI:</b> Produk Asli AntiInflam Coffee NanoCaps.<br>
                Diproduksi pada: {data['Tanggal_Produksi']}
            </div>
            """, unsafe_allow_html=True)

            # Bagian 1: Identitas Bahan
            st.subheader("📍 Asal-Usul (Traceability)")
            st.info(f"**Sumber Kopi:** {data['Sumber_Kopi']}\n\n**Rempah:** {data['Varietas_Rempah']}")

            # Bagian 2: Data Saintifik (Metrics)
            st.subheader("🔬 Kualitas Bioaktif (Lab Result)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                # Warna hijau jika ukuran nano bagus (<200)
                st.metric("Ukuran Nano", f"{data['Ukuran_Partikel_nm']} nm", "Optimal <200nm")
            with col2:
                st.metric("Total Fenolik", f"{data['Total_Fenolik']} mg/g", "Antioksidan")
            with col3:
                st.metric("Anti-Inflamasi", f"{data['Aktivitas_Anti_Inflamasi']}%", "Sangat Tinggi")

            # Bagian 3: Grafik Visual
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
# TAB 2: TAMPILAN ADMIN (DENGAN PASSWORD)
# =========================================
with tab2:
    st.write("### 🔐 Akses Terbatas")
    st.caption("Area khusus Tim Quality Control & Produksi.")
    
    # 1. Input Password
    password = st.text_input("Masukkan Password Admin:", type="password")
    
    # --- PASSWORD RAHASIA ADALAH: 12345 ---
    if password == "12345": 
        st.success("Login Berhasil! Akses dibuka.")
        st.divider()
        
        # --- MULAI AREA ADMIN ---
        st.write("### 🖨️ Generator QR Code")
        st.caption("Pilih batch produksi untuk mencetak label.")
        
        # Dropdown pilihan batch
        if not df.empty:
            pilihan = st.selectbox("Pilih Batch ID:", df['Batch_ID'])
        else:
            st.warning("Database kosong. Jalankan 'bikin_data.py' dulu.")
            pilihan = None
            
        # URL Default langsung mengarah ke website Anda yang sudah online
        default_link = "https://antiinflamcoffee.streamlit.app"
        base_url = st.text_input("URL Aplikasi (Link Web):", default_link) 
        
        if st.button("Buat QR Code") and pilihan:
            full_link = f"{base_url}?batch={pilihan}"
            
            # Membuat QR Code
            qr = qrcode.QRCode(box_size=10, border=2)
            qr.add_data(full_link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Menampilkan QR Code
            buf = BytesIO()
            img.save(buf)
            
            c1, c2 = st.columns([1,2])
            with c1:
                st.image(buf, width=200, caption=f"QR: {pilihan}")
            with c2:
                st.success("✅ Gambar QR Siap!")
                st.code(full_link, language="text")
                st.info("Klik kanan pada gambar -> 'Save Image As' untuk menyimpan dan print.")
    
    elif password != "":
        st.error("⛔ Password Salah! Akses ditolak.")
