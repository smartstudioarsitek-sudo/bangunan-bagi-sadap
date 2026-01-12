# modules/visualisasi.py
import matplotlib.pyplot as plt

def plot_penampang(b, h, label_tipe="Saluran"):
    """Fungsi untuk menggambar penampang sederhana."""
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Koordinat kotak sederhana
    x = [0, 0, b, b]
    y = [h, 0, 0, h]
    
    ax.fill_between(x, y, color='#3498db', alpha=0.5, label='Air')
    ax.plot([0, 0, b, b], [h+0.5, 0, 0, h+0.5], color='black', linewidth=2, label='Dinding')
    
    ax.set_title(f"Visualisasi: {label_tipe}")
    ax.set_xlabel("Lebar (m)")
    ax.set_ylabel("Tinggi Muka Air (m)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.3)
    
    return fig