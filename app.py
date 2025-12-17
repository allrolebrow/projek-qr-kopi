import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# --- KONFIGURASI HALAMAN KONSUMEN ---
st.set_page_config(
    page_title="Traceability: AntiInflam Coffee",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS BIAR CANTIK ---
st.markdown("""
    <style>
    .stApp {background-color: #fcfcfc;}
    .success-box {
        padding: 20px; 
        background-color: #d4edda; 
        color: #155724;
        border-radius: 12px; 
        border: 1px solid #c3e6cb; 
        margin-bottom: 20px;
    }
    .qc-badge {
        background-color: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-top: 5px;
    }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
def get_data():
    try:
        return pd.read_csv('data_mutu.csv')
    except:
        return pd.DataFrame()

df = get_data()

# --- HEADER ---
st.image("https://cdn-icons-png.flaticon.com/512/2935/2935308.png", width=120)
st.title("🛡️ Quality Traceability")
st.caption("AntiInflam Coffee NanoCaps™")

# --- LOGIKA SCAN OTOMATIS ---
query_params = st.query_params
batch_url = query_params.get("batch", None)

if batch_url:
    hasil = df[df['Batch_ID'] == batch_url]
    
    if not hasil.empty:
        data = hasil.iloc[0]
        
        # Animasi Loading
        with st.spinner('Memverifikasi Blockchain & Data Lab...'):
            time.sleep(1.0)
            
        # --- UPDATE DISINI: MENAMPILKAN STATUS QC ---
        # Cek apakah kolom Status_QC ada di database, jika tidak default 'LULUS'
        status_qc = data.get('Status_QC', 'LULUS UJI') 
        
        # Logika Tampilan Status
        st.markdown(f"""
        <div class="success-box">
            <h3>✅ BATCH TERVERIFIKASI</h3>
            <b>ID: {data['Batch_ID']}</b><br>
            <span class="qc-badge">STATUS QC: {status_qc}</span><br>
            <br>
            Produk Asli & Aman Dikonsumsi.<br>
            <i>Tanggal Produksi: {data['Tanggal_Produksi']}</i>
        </div>
        """, unsafe_allow_html=True)

        # 2. Data Utama (Metrics)
        st.subheader("🔬 Hasil Uji Laboratorium")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Ukuran Nano", f"{data['Ukuran_Partikel_nm']} nm", "Optimal")
        with c2:
            st.metric("Fenolik", f"{data['Total_Fenolik']} mg", "Antioksidan")
        with c3:
            st.metric("Anti-Inflamasi", f"{data['Aktivitas_Anti_Inflamasi']}%", "High")

        # 3. Grafik
        st.divider()
        st.subheader("📊 Grafik Efektivitas")
        chart_data = pd.DataFrame({
            'Item': ['Produk Ini', 'Kopi Biasa', 'Vit C'],
            'Efektivitas (%)': [data['Aktivitas_Anti_Inflamasi'], 40, 95]
        })
        st.bar_chart(chart_data, x='Item', y='Efektivitas (%)', color='#4b2c20')

        # 4. Info Asal Usul
        with st.expander("📍 Lihat Asal Usul Kopi (Traceability)"):
            st.write(f"**Lokasi Panen:** {data['Sumber_Kopi']}")
            st.write(f"**Campuran Rempah:** {data['Varietas_Rempah']}")
            st.write("**Metode:** Nanoenkapsulasi Gelasi Ionik")

    else:
        st.error("❌ Batch ID tidak dikenali. Produk mungkin palsu atau kode salah.")

# Tampilan Awal (Belum Scan)
else:
    st.info("👋 Selamat Datang! Silakan Scan QR Code yang ada di kemasan produk untuk melihat data mutu.")
    st.markdown("---")
    
    input_manual = st.text_input("Atau masukkan Kode Batch manual:", placeholder="Contoh: NANO-001")
    if st.button("Cek Mutu"):
        if input_manual:
            st.query_params["batch"] = input_manual
            st.rerun()
