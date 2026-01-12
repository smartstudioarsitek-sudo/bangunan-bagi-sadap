# modules/hidrolika.py
import math

# --- RUMUS 1: Untuk SADAP (Tipe Pelimpah/Romijn) ---
def hitung_romijn(h, b, Cd=1.71):
    """
    Rumus untuk Pintu Romijn (Bangunan Sadap).
    Q = Cd * b * h^1.5
    Output: Debit (m3/det)
    """
    if h <= 0: return 0
    return Cd * b * math.pow(h, 1.5)

def cari_lebar_romijn(Q, h, Cd=1.71):
    """Mencari lebar (b) jika Q dan h diketahui."""
    if h <= 0: return 0
    return Q / (Cd * math.pow(h, 1.5))


# --- RUMUS 2: Untuk BAGI (Tipe Sorong/Sluice Gate) ---
def hitung_pintu_sorong(b, a, h1, K=0.6, g=9.81):
    """
    Rumus untuk Pintu Sorong (Bangunan Bagi).
    Q = K * b * a * sqrt(2 * g * h1)
    
    Variabel:
    b  = Lebar pintu (m)
    a  = Bukaan pintu (m) -> tinggi bukaan bawah
    h1 = Tinggi air di hulu (m)
    K  = Koefisien debit (standar: 0.6 - 0.8)
    """
    if h1 <= 0 or a <= 0: return 0
    return K * b * a * math.sqrt(2 * g * h1)

def cari_bukaan_sorong(Q, b, h1, K=0.6, g=9.81):
    """
    Mencari seberapa tinggi pintu harus dibuka (a).
    a = Q / (K * b * sqrt(2 * g * h1))
    """
    if h1 <= 0: return 0
    pembagi = K * b * math.sqrt(2 * g * h1)
    if pembagi == 0: return 0
    return Q / pembagi
def cek_neraca_air(Q_masuk, list_Q_keluar):
    """
    Memeriksa apakah debit masuk == total debit keluar.
    Digunakan untuk simulasi Bangunan Bagi.
    """
    total_keluar = sum(list_Q_keluar)
    selisih = Q_masuk - total_keluar
    # Toleransi selisih 0.001 (untuk pembulatan)
    seimbang = abs(selisih) < 0.001
    return seimbang, total_keluar, selisih

def cek_neraca_air(Q_masuk, list_Q_keluar):
    """
    Memeriksa apakah debit masuk == total debit keluar.
    Digunakan untuk simulasi Bangunan Bagi.
    """
    total_keluar = sum(list_Q_keluar)
    selisih = Q_masuk - total_keluar
    # Toleransi selisih 0.001 (untuk pembulatan)
    seimbang = abs(selisih) < 0.001
    return seimbang, total_keluar, selisih

# hidrolika.py
import math

# ... (kode fungsi romijn yang lama biarkan saja) ...

def hitung_bukaan_sorong_z(Q, b, z, C=0.8, g=9.81):
    """
    Menghitung bukaan pintu (a) berdasarkan Beda Tinggi Tekan (z).
    Sesuai Gambar Manual Kakak (Rumus Orifice Tenggelam).
    
    Rumus: a = Q / (C * b * sqrt(2 * g * z))
    """
    if z <= 0: return 0
    
    akar_2gz = math.sqrt(2 * g * z)
    penyebut = C * b * akar_2gz
    
    if penyebut == 0: return 0
    
    a = Q / penyebut
    return a

# ... (fungsi cek_neraca_air biarkan ada di bawah) ...



