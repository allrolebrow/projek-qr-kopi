import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import os

st.set_page_config(page_title="Admin Panel", page_icon="🔐", layout="wide")

# --- JUDUL HALAMAN ---
st.title("🔐 Admin System Control")
st.markdown("---")

# --- 1. SISTEM LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("Silakan Login untuk mengakses menu kontrol.")
        password = st.text_input("Masukkan Password Admin:", type="password")
        if st.button("Login Masuk"):
            if password == "12345": # GANTI PASSWORD DISINI
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("⛔ Password Salah!")

else:
    # --- 2. JIKA SUDAH LOGIN (DASHBOARD ADMIN) ---
    
    # Tombol Logout di Sidebar
    with st.sidebar:
        st.write(f"Halo, Admin QC")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()
    
    # --- MENU PILIHAN (OPSI) ---
    menu_admin = st.radio(
        "Pilih Tugas:",
        ["📝 Input Data Batch Baru", "🖨️ Generator QR Code", "📂 Lihat Database Lengkap"],
        horizontal=True
    )
    st.divider()

    # ====================================================
    # MENU 1: INPUT DATA BARU (Formulir Tambah Data)
    # ====================================================
    if menu_admin == "📝 Input Data Batch Baru":
        st.subheader("Input Hasil Uji Laboratorium")
        st.caption("Masukkan data batch baru setelah hasil lab keluar.")
        
        with st.form("form_input_data"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                new_batch_id = st.text_input("Batch ID (Kode Unik):", placeholder="Contoh: NANO-005")
                tgl_prod = st.text_input("Tanggal Produksi:", placeholder="Contoh: 12 Des 2025")
                sumber = st.text_input("Sumber Kopi:", placeholder="Contoh: Luwak Liar - Gayo")
                rempah = st.text_input("Varietas Rempah:", placeholder="Contoh: Jahe Merah + Kunyit")
            
            with col_b:
                st.write("**Data Kuantitatif (Lab):**")
                # Menggunakan number_input agar user hanya bisa isi angka
                ukuran_nano = st.number_input("Ukuran Partikel (nm):", min_value=0.0, format="%.2f")
                fenolik = st.number_input("Total Fenolik (mg/g):", min_value=0.0, format="%.2f")
                inflamasi = st.number_input("Aktivitas Anti-Inflamasi (%):", min_value=0.0, max_value=100.0, format="%.2f")
                status_qc = st.selectbox("Status QC:", ["LULUS UJI", "TIDAK LULUS"])

            submit_btn = st.form_submit_button("💾 Simpan ke Database")
        
        # LOGIKA PENYIMPANAN
        if submit_btn:
            if new_batch_id and sumber:
                # 1. Siapkan Data Baru
                new_data = {
                    'Batch_ID': [new_batch_id],
                    'Tanggal_Produksi': [tgl_prod],
                    'Sumber_Kopi': [sumber],
                    'Varietas_Rempah': [rempah],
                    'Ukuran_Partikel_nm': [ukuran_nano],
                    'Total_Fenolik': [fenolik],
                    'Aktivitas_Anti_Inflamasi': [inflamasi],
                    'Status_QC': [status_qc]
                }
                new_df = pd.DataFrame(new_data)
                
                # 2. Cek File CSV, kalau ada append (tambah bawah), kalau belum ada bikin baru
                file_db = 'data_mutu.csv'
                if os.path.exists(file_db):
                    existing_df = pd.read_csv(file_db)
                    # Cek duplikat ID
                    if new_batch_id in existing_df['Batch_ID'].values:
                        st.error(f"❌ Batch ID {new_batch_id} sudah ada! Gunakan kode lain.")
                    else:
                        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                        updated_df.to_csv(file_db, index=False)
                        st.success(f"✅ Sukses! Batch {new_batch_id} berhasil ditambahkan.")
                else:
                    new_df.to_csv(file_db, index=False)
                    st.success(f"✅ Database baru dibuat & Batch {new_batch_id} disimpan.")
            else:
                st.warning("⚠️ Mohon lengkapi minimal Batch ID dan Sumber Kopi.")

    # ====================================================
    # MENU 2: GENERATOR QR CODE
    # ====================================================
    elif menu_admin == "🖨️ Generator QR Code":
        st.subheader("Cetak Label QR")
        
        # Load Data Terbaru
        try:
            df = pd.read_csv('data_mutu.csv')
            list_batch = df['Batch_ID'].tolist()
        except:
            list_batch = []
            st.error("Database belum ada. Silakan input data dulu.")

        if list_batch:
            c1, c2 = st.columns([1, 2])
            with c1:
                pilihan_batch = st.selectbox("Pilih Batch:", list_batch)
                # Link otomatis deteksi default
                base_url = st.text_input("Link Website Konsumen:", "https://antiinflamcoffee.streamlit.app")
            
            with c2:
                if st.button("Generate QR"):
                    full_link = f"{base_url}?batch={pilihan_batch}"
                    
                    qr = qrcode.QRCode(box_size=10, border=2)
                    qr.add_data(full_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    buf = BytesIO()
                    img.save(buf)
                    
                    st.image(buf, width=200, caption=f"Batch: {pilihan_batch}")
                    st.success("Siap Cetak!")
                    st.code(full_link)
        else:
            st.info("Belum ada data batch untuk dibuatkan QR.")

    # ====================================================
    # MENU 3: LIHAT DATABASE (TABEL)
    # ====================================================
    elif menu_admin == "📂 Lihat Database Lengkap":
        st.subheader("Rekap Data Mutu")
        try:
            df = pd.read_csv('data_mutu.csv')
            st.dataframe(df, use_container_width=True)
            
            # Tombol Download CSV (Backup)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Backup CSV",
                data=csv,
                file_name='backup_data_mutu.csv',
                mime='text/csv',
            )
        except:
            st.warning("Data kosong.")
