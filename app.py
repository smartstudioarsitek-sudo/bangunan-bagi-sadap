# app.py

import streamlit as st
import pandas as pd
# Import modul buatan kita sendiri
import hidrolika as hydro
import visualisasi as vis

st.set_page_config(page_title="Desain Bangunan Irigasi", layout="wide")

st.title("Aplikasi Desain Bangunan Irigasi Modular")
st.markdown("---")

# Sidebar
tipe = st.sidebar.selectbox("Pilih Modul Perhitungan:", 
                            ["Bangunan Bagi", "Bangunan Sadap"])

if tipe == "Bangunan Sadap":
    st.subheader("Desain Pintu Romijn (Sadap)")
    
    col1, col2 = st.columns(2)
    with col1:
        Q_input = st.number_input("Debit Rencana (m³/det)", value=0.5)
        h_input = st.number_input("Tinggi Energi (m)", value=0.4)
    
    with col2:
        # Panggil rumus dari modul hidrolika
        lebar = hydro.hitung_lebar_romijn(Q_input, h_input)
        st.success(f"Lebar Pintu Diperlukan: **{lebar:.3f} meter**")
        
    # Panggil grafik dari modul visualisasi
    gambar = vis.plot_penampang(lebar, h_input, "Pintu Romijn")
    st.pyplot(gambar)

elif tipe == "Bangunan Bagi":
    st.subheader("Simulasi Pembagian Debit")
    # ... (Logika input lainnya)
    Q_masuk = st.number_input("Q Masuk", value=2.0)
    Q_kiri = st.number_input("Q Cabang Kiri", value=1.0)
    Q_kanan = st.number_input("Q Cabang Kanan", value=1.0)
    
    # Menggunakan fungsi cek neraca
    seimbang, total, selisih = hydro.cek_neraca_air(Q_masuk, [Q_kiri, Q_kanan])
    
    if seimbang:
        st.success("Neraca Air: OK")
    else:

        st.error(f"Neraca Air: SELISIH {selisih:.3f} m³/det")
