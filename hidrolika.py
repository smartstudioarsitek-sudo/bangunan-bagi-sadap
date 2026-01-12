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
