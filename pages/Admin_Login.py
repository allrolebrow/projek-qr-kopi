import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO

st.set_page_config(page_title="Admin Panel", page_icon="🔐")

st.title("🔐 Admin System")
st.markdown("---")

# --- SISTEM LOGIN SEDERHANA ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    password = st.text_input("Masukkan Password Admin:", type="password")
    if st.button("Login"):
        if password == "12345": # GANTI PASSWORD DISINI
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Password Salah!")
else:
    # --- JIKA SUDAH LOGIN, TAMPILKAN MENU INI ---
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    st.success("✅ Akses Diterima: Mode Quality Control")
    
    # Load Data (Perlu path ../ karena ada di folder luar)
    try:
        df = pd.read_csv('data_mutu.csv')
    except:
        st.error("Database tidak ditemukan!")
        df = pd.DataFrame()

    st.subheader("🖨️ Generator QR Code")
    
    if not df.empty:
        pilihan_batch = st.selectbox("Pilih Batch untuk Dicetak:", df['Batch_ID'])
        
        # PENTING: Masukkan Link Aplikasi UTAMA (bukan link admin)
        # Contoh: https://kopi-saya.streamlit.app
        base_url = st.text_input("Link Website Utama (Konsumen):", "https://antiinflamcoffee.streamlit.app")
        
        if st.button("Generate QR"):
            # Link mengarah ke app.py (halaman depan), bukan ke admin
            full_link = f"{base_url}?batch={pilihan_batch}"
            
            qr = qrcode.QRCode(box_size=10, border=2)
            qr.add_data(full_link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = BytesIO()
            img.save(buf)
            
            c1, c2 = st.columns([1,2])
            with c1:
                st.image(buf, width=200, caption=f"Batch: {pilihan_batch}")
            with c2:
                st.info("Arahkan kamera HP ke QR ini. Konsumen akan langsung melihat data mutu tanpa login.")
                st.code(full_link)