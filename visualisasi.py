import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- MODUL VISUALISASI GAMBAR ---

def plot_penampang(b, h, label_tipe="Saluran", kedalaman_saluran=1.5):
    """Menggambar Cross Section Pintu/Saluran"""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Gambar Dinding/Saluran (Wadah)
    # Asumsi kedalaman saluran sedikit lebih tinggi dari air
    H_total = max(h + 0.5, kedalaman_saluran)
    
    x_tanah = [0, 0, b, b]
    y_tanah = [H_total, 0, 0, H_total]
    
    ax.plot(x_tanah, y_tanah, color='black', linewidth=3, label='Dinding')
    
    # Gambar Air
    if h > 0:
        x_air = [0, 0, b, b]
        y_air = [h, 0, 0, h]
        ax.fill_between(x_air, y_air, color='#3498db', alpha=0.6, label='Muka Air')
        # Garis permukaan air
        ax.plot([0, b], [h, h], color='blue', linestyle='--')
        ax.text(b/2, h + 0.05, f"MA = {h:.2f} m", ha='center', color='blue', fontsize=9)

    # Dimensi Lebar
    ax.annotate(f"B = {b:.2f} m", xy=(b/2, 0), xytext=(b/2, -0.2),
                ha='center', arrowprops=dict(arrowstyle='<->'))

    ax.set_title(f"Penampang Melintang: {label_tipe}")
    ax.set_xlim(-0.5, b + 0.5)
    ax.set_ylim(-0.5, H_total + 0.5)
    ax.axis('off') # Matikan axis grid agar seperti gambar teknik
    
    return fig

def plot_skema_bagi_sadap(Q_masuk, Q_hilir, Q_sadap, nama_bangunan="B. Bagi-Sadap"):
    """Menggambar Denah Aliran (Skema Irigasi)"""
    fig, ax = plt.subplots(figsize=(7, 5))
    
    # 1. Aliran Masuk (Kiri ke Pusat)
    ax.arrow(0, 0, 2, 0, head_width=0.15, head_length=0.2, fc='blue', ec='blue', width=0.04)
    ax.text(1, 0.3, f"Q Masuk\n{Q_masuk} m³/s", ha='center', color='blue', fontweight='bold')
    
    # 2. Aliran Ke Hilir/Bagi (Pusat ke Kanan)
    ax.arrow(2.2, 0, 2, 0, head_width=0.15, head_length=0.2, fc='green', ec='green', width=0.04)
    ax.text(3.2, 0.3, f"Ke Hilir (Bagi)\n{Q_hilir:.3f} m³/s", ha='center', color='green', fontweight='bold')
    
    # 3. Aliran Sadap (Pusat ke Bawah) - Belok Kanan/Kiri tergantung skema
    ax.arrow(2.1, -0.1, 0, -2, head_width=0.15, head_length=0.2, fc='red', ec='red', width=0.04)
    ax.text(2.3, -1.2, f"Ke Tersier (Sadap)\n{Q_sadap:.3f} m³/s", va='center', color='red', fontweight='bold')
    
    # Simbol Bangunan (Kotak di tengah)
    rect = patches.Rectangle((1.8, -0.4), 0.6, 0.8, linewidth=2, edgecolor='black', facecolor='white')
    ax.add_patch(rect)
    ax.text(2.1, 0, "BANGUNAN\nUTAMA", ha='center', va='center', fontsize=8)
    
    ax.set_title(f"Skema Denah Aliran: {nama_bangunan}", fontsize=12)
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-3, 1.5)
    ax.axis('off')
    
    return fig
