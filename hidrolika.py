import math

# --- MODUL HIDROLIKA & PERHITUNGAN (Standar KP-04) ---

def cek_neraca_air(Q_masuk, list_Q_keluar):
    """
    Cek Keseimbangan Debit (Inflow vs Outflow).
    Output: (Boolean Seimbang, Total Keluar, Selisih)
    """
    total_keluar = sum(list_Q_keluar)
    selisih = Q_masuk - total_keluar
    seimbang = abs(selisih) < 0.001
    return seimbang, total_keluar, selisih

# --- TIPE 1: PINTU ROMIJN (PELUAP) ---
# Biasanya untuk Bangunan Sadap Tersier standar
def cari_lebar_romijn(Q, h, Cd=1.71):
    """
    Mencari Lebar Efektif (b) untuk Pintu Romijn.
    Rumus: Q = 1.71 * b * h^1.5
    """
    if h <= 0: return 0
    # b = Q / (1.71 * h^1.5)
    return Q / (Cd * math.pow(h, 1.5))

def hitung_debit_romijn(b, h, Cd=1.71):
    if h <= 0: return 0
    return Cd * b * math.pow(h, 1.5)


# --- TIPE 2: PINTU SORONG (ORIFICE / SLUICE GATE) ---
# Digunakan untuk Pintu Bagi atau Pintu Sadap Sederhana (Crump)

def hitung_bukaan_sorong_z(Q, b, z, C=0.8, g=9.81):
    """
    Menghitung bukaan pintu (a) berdasarkan Beda Tinggi Tekan/Kehilangan Energi (z).
    Sesuai standar perhitungan lapangan (Rumus Orifice Tenggelam).
    
    Rumus: Q = C * b * a * sqrt(2 * g * z)
    Maka : a = Q / (C * b * sqrt(2 * g * z))
    
    Parameter:
    Q : Debit (m3/s)
    b : Lebar Pintu (m)
    z : Kehilangan energi / beda tinggi muka air hulu-hilir (m)
    C : Koefisien Debit (Standar: 0.8 untuk rounded, 0.6 untuk tajam)
    """
    if z <= 0: return 0
    
    akar_2gz = math.sqrt(2 * g * z)
    penyebut = C * b * akar_2gz
    
    if penyebut == 0: return 0
    
    a = Q / penyebut
    return a

def hitung_debit_sorong_z(a, b, z, C=0.8, g=9.81):
    """Menghitung Debit (Q) jika bukaan (a) diketahui."""
    if z <= 0: return 0
    return C * b * a * math.sqrt(2 * g * z)
