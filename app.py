import streamlit as st
import pandas as pd
import hidrolika as hydro
import visualisasi as vis

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Jiat Smart Studio - Desain Irigasi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR: REFERENSI TEKNIS (KP-04) ---
st.sidebar.title("📚 Referensi KP-04")
st.sidebar.info("Gunakan data berikut sebagai acuan perencanaan.")

with st.sidebar.expander("Koefisien Debit (C / µ)"):
    st.markdown("""
    **Untuk Pintu Sorong (Sluice Gate):**
    * **0.80** : Ambang bulat/tumpul (Paling umum).
    * **0.60 - 0.62** : Ambang tajam (Sharp edge).
    
    **Untuk Pintu Romijn:**
    * **1.71** : Koefisien Debit standar ($C_d$).
    """)

with st.sidebar.expander("Kecepatan Izin Saluran"):
    st.markdown("""
    * **Pasangan Batu/Beton**: 1.5 - 2.0 m/s
    * **Tanah Liat**: 0.6 - 0.8 m/s
    * **Pasir**: 0.3 - 0.5 m/s
    """)

st.sidebar.divider()
st.sidebar.caption("Jiat Smart Studio | Engineering Tool")

# --- JUDUL APLIKASI ---
st.title("🏗️ Aplikasi Desain Bangunan Irigasi (Standar PU)")
st.markdown("Alat bantu perhitungan hidrolis bangunan Bagi, Sadap, dan Bagi-Sadap.")
st.divider()

# --- PILIHAN MODUL ---
tipe_bangunan = st.radio(
    "Pilih Jenis Bangunan:",
    ["Bangunan Bagi", "Bangunan Sadap", "Bangunan Bagi-Sadap"],
    horizontal=True
)

# ==============================================================================
# MODUL 1: BANGUNAN SADAP (TERSIER)
# ==============================================================================
if tipe_bangunan == "Bangunan Sadap":
    st.subheader("Desain Bangunan Sadap (Intake Tersier)")
    
    col_set, col_viz = st.columns([1, 1])
    
    with col_set:
        st.markdown("### 1. Data Perencanaan")
        # Pilihan metode sesuai request user (bisa Romijn atau Sorong)
        metode_sadap = st.selectbox("Tipe Pintu:", ["Pintu Sorong (Orifice)", "Pintu Romijn (Peluap)"])
        
        if metode_sadap == "Pintu Sorong (Orifice)":
            st.caption("Digunakan untuk sadap sederhana atau debit kecil (Rumus: $Q = C \cdot b \cdot a \cdot \sqrt{2gz}$)")
            Q_rencana = st.number_input("Debit Rencana (m³/s)", value=0.012, format="%.4f")
            lebar_pintu = st.number_input("Lebar Pintu (B) [m]", value=0.30)
            z_loss = st.number_input("Kehilangan Energi (z) [m]", value=0.05, step=0.01, help="Beda tinggi muka air hulu dan hilir")
            koef_c = st.number_input("Koefisien Debit (C)", value=0.80)
            
            # Hitung
            bukaan_a = hydro.hitung_bukaan_sorong_z(Q_rencana, lebar_pintu, z_loss, koef_c)
            
            st.success(f"Tinggi Bukaan Pintu (a): **{bukaan_a:.3f} m** ({bukaan_a*100:.1f} cm)")
            
            # Cek Peringatan
            if bukaan_a > lebar_pintu:
                st.error("⚠️ Bukaan pintu melebihi lebar pintu (aspek rasio tidak ideal)!")
            if bukaan_a > 1.0: # Asumsi pintu sadap tersier jarang > 1m
                st.warning("⚠️ Bukaan pintu terlihat terlalu besar untuk sadap tersier.")
                
            fig_cross = vis.plot_penampang(lebar_pintu, bukaan_a, "Bukaan Pintu Sorong")

        else: # ROMIJN
            st.caption("Digunakan untuk pengukuran debit presisi (Rumus: $Q = 1.71 \cdot b \cdot h^{1.5}$)")
            Q_rencana = st.number_input("Debit Rencana (m³/s)", value=0.050, format="%.3f")
            h_air = st.number_input("Tinggi Energi di atas mercu (m)", value=0.30)
            
            # Hitung
            lebar_b = hydro.cari_lebar_romijn(Q_rencana, h_air)
            
            st.success(f"Lebar Efektif Pintu (b): **{lebar_b:.3f} m**")
            fig_cross = vis.plot_penampang(lebar_b, h_air, "Muka Air di Romijn")

    with col_viz:
        st.markdown("### 2. Visualisasi")
        st.pyplot(fig_cross)

# ==============================================================================
# MODUL 2: BANGUNAN BAGI (SEKUNDER)
# ==============================================================================
elif tipe_bangunan == "Bangunan Bagi":
    st.subheader("Desain Bangunan Bagi")
    st.info("Bangunan Bagi biasanya menggunakan Pintu Sorong untuk mengatur muka air ke arah hilir.")
    
    col1, col2 = st.columns(2)
    with col1:
        Q_bagi = st.number_input("Debit Rencana ke Hilir (m³/s)", value=1.50)
        B_saluran = st.number_input("Lebar Pintu/Saluran (m)", value=1.50)
        z_bagi = st.number_input("Kehilangan Energi (z) [m]", value=0.10)
        C_bagi = st.number_input("Koefisien C", value=0.80)
        
    with col2:
        bukaan_bagi = hydro.hitung_bukaan_sorong_z(Q_bagi, B_saluran, z_bagi, C_bagi)
        st.metric("Tinggi Bukaan Pintu (a)", f"{bukaan_bagi:.3f} m")
        st.caption("Pastikan bukaan pintu tidak melebihi tinggi jagaan saluran.")
        
    st.pyplot(vis.plot_penampang(B_saluran, bukaan_bagi, "Pintu Bagi (Sorong)"))

# ==============================================================================
# MODUL 3: BANGUNAN BAGI-SADAP (KOMPLEKS)
# ==============================================================================
elif tipe_bangunan == "Bangunan Bagi-Sadap":
    st.subheader("🏢 Desain Bangunan Bagi-Sadap")
    st.markdown("Perhitungan simultan untuk pembagian air ke hilir dan penyadapan ke tersier.")

    tab1, tab2 = st.tabs(["📝 Input Data Hidrolis", "📊 Hasil & Gambar"])

    with tab1:
        st.write("#### A. Data Aliran Utama")
        col_main1, col_main2 = st.columns(2)
        with col_main1:
            Q_hulu = st.number_input("Debit Hulu (Q Masuk) [m³/s]", value=2.00)
        with col_main2:
            Q_sadap_rencana = st.number_input("Rencana Penyadapan (Liter/detik)", value=200.0)
            Q_sadap_m3 = Q_sadap_rencana / 1000
            
        # Otomatisasi Neraca Air
        Q_hilir = Q_hulu - Q_sadap_m3
        
        st.info(f"""
        **Neraca Air:**
        * Masuk : {Q_hulu:.3f} m³/s
        * Sadap : {Q_sadap_m3:.3f} m³/s
        * **Sisa ke Hilir : {Q_hilir:.3f} m³/s**
        """)
        
        if Q_hilir < 0:
            st.error("❌ Debit Sadap lebih besar dari Debit Hulu! Cek input.")
            st.stop()

        st.divider()
        
        col_a, col_b = st.columns(2)
        
        # INPUT BAGIAN BAGI (KE HILIR)
        with col_a:
            st.write("#### B. Pintu Bagi (Ke Hilir)")
            st.caption("Menggunakan Rumus Pintu Sorong")
            b_bagi = st.number_input("Lebar Pintu Bagi (m)", value=1.5)
            z_bagi = st.number_input("Head Loss Bagi (z) [m]", value=0.1, key="z_bagi")
            c_bagi = st.number_input("Koefisien C Bagi", value=0.8, key="c_bagi")
            
        # INPUT BAGIAN SADAP (KE TERSIER)
        with col_b:
            st.write("#### C. Pintu Sadap (Ke Tersier)")
            tipe_sadap_bs = st.radio("Tipe Pintu Sadap:", ["Sorong", "Romijn"], key="rad_bs")
            
            if tipe_sadap_bs == "Sorong":
                b_sadap = st.number_input("Lebar Pintu Sadap (m)", value=0.5, key="b_sadap_bs")
                z_sadap = st.number_input("Head Loss Sadap (z) [m]", value=0.05, key="z_sadap_bs")
                c_sadap = st.number_input("Koefisien C Sadap", value=0.8, key="c_sadap_bs")
            else:
                h_sadap = st.number_input("Tinggi Energi Sadap (h) [m]", value=0.4, key="h_sadap_bs")

    with tab2:
        # --- PERHITUNGAN OUTPUT ---
        
        # 1. Hitung Bagi (Sorong)
        a_bagi = hydro.hitung_bukaan_sorong_z(Q_hilir, b_bagi, z_bagi, c_bagi)
        
        # 2. Hitung Sadap
        if tipe_sadap_bs == "Sorong":
            a_sadap = hydro.hitung_bukaan_sorong_z(Q_sadap_m3, b_sadap, z_sadap, c_sadap)
            txt_sadap_dimensi = f"Bukaan (a) = {a_sadap:.3f} m"
            val_sadap_dimensi = a_sadap
            label_sadap = "Bukaan Pintu Sorong"
            lebar_visual_sadap = b_sadap
        else:
            b_romijn_perlu = hydro.cari_lebar_romijn(Q_sadap_m3, h_sadap)
            txt_sadap_dimensi = f"Lebar Efektif (b) = {b_romijn_perlu:.3f} m"
            val_sadap_dimensi = h_sadap # Untuk visualisasi tinggi air
            label_sadap = "Lebar Pintu Romijn"
            lebar_visual_sadap = b_romijn_perlu

        # --- TAMPILAN HASIL ---
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.success("✅ Hasil Desain Pintu Bagi")
            st.metric("Debit (Q)", f"{Q_hilir:.3f} m³/s")
            st.metric("Bukaan Pintu (a)", f"{a_bagi:.3f} m")
            
        with res_col2:
            st.info("✅ Hasil Desain Pintu Sadap")
            st.metric("Debit (Q)", f"{Q_sadap_m3:.3f} m³/s")
            st.metric("Dimensi Rencana", txt_sadap_dimensi)
            
        st.divider()
        
        # --- VISUALISASI ---
        st.write("#### 🗺️ Skema & Denah")
        st.pyplot(vis.plot_skema_bagi_sadap(Q_hulu, Q_hilir, Q_sadap_m3))
        
        st.write("#### 📐 Penampang Melintang")
        vcol1, vcol2 = st.columns(2)
        with vcol1:
            st.caption("Penampang Pintu Bagi")
            st.pyplot(vis.plot_penampang(b_bagi, a_bagi, "Pintu Bagi"))
        with vcol2:
            st.caption("Penampang Pintu Sadap")
            st.pyplot(vis.plot_penampang(lebar_visual_sadap, val_sadap_dimensi, label_sadap))
