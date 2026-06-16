# utils.py
import os
from datetime import datetime
from typing import Dict

def save_recommendations_to_file(hasil_rekomendasi: Dict, folder: str = "data/hasil_rekomendasi") -> str:
    """
    Menyimpan semua hasil rekomendasi ke file teks
    Mencakup rekomendasi UTAMA (100%) dan MENDEKATI (80%/66%)
    """
    # Buat folder jika belum ada
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Buat nama file dengan timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"rekomendasi_gizi_{timestamp}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        # HEADER
        f.write("=" * 70 + "\n")
        f.write(" " * 18 + "SISTEM PAKAR GIZI & POLA MAKAN\n")
        f.write("=" * 70 + "\n")
        f.write(f"Tanggal : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        # CEK APAKAH ADA HASIL
        rekomendasi_tepat = hasil_rekomendasi.get("tepat", [])
        rekomendasi_mendekati = hasil_rekomendasi.get("mendekati", [])
        
        if not rekomendasi_tepat and not rekomendasi_mendekati:
            f.write("❌ TIDAK ADA REKOMENDASI\n")
            f.write("-" * 50 + "\n")
            f.write("Berdasarkan jawaban Anda, tidak ditemukan kondisi gizi yang signifikan.\n")
            f.write("Pola makan dan gaya hidup Anda sudah cukup sehat!\n\n")
            f.write("💡 SARAN UMUM:\n")
            f.write("   1. Tetap jaga pola makan seimbang (sayur, buah, protein)\n")
            f.write("   2. Minum air putih 8 gelas/hari\n")
            f.write("   3. Olahraga teratur 30 menit/hari\n")
            f.write("   4. Tidur cukup 7-8 jam/hari\n")
        else:
            # ===== REKOMENDASI UTAMA (100%) =====
            if rekomendasi_tepat:
                f.write("🎯 REKOMENDASI UTAMA (Sangat Cocok)\n")
                f.write("─" * 70 + "\n\n")
                
                for i, rec in enumerate(rekomendasi_tepat, 1):
                    f.write(f"{i}. 🥗 {rec['kondisi']}\n")
                    f.write(f"   {rec['status']}\n\n")
                    f.write(f"   📝 Penjelasan:\n")
                    f.write(f"   {rec['penjelasan']}\n\n")
                    f.write(f"   🍽️ Rekomendasi Makanan:\n")
                    for r in rec['rekomendasi']:
                        f.write(f"      {r}\n")
                    f.write("\n")
            
            # ===== REKOMENDASI MENDEKATI (80%/66%) =====
            if rekomendasi_mendekati:
                if rekomendasi_tepat:
                    f.write("\n🔄 REKOMENDASI LAIN (Cukup Cocok)\n")
                    f.write("─" * 70 + "\n\n")
                else:
                    f.write("🔄 REKOMENDASI TERDEKAT\n")
                    f.write("─" * 70 + "\n\n")
                    f.write("💡 Tidak ada rekomendasi yang 100% cocok.\n")
                    f.write("   Berikut rekomendasi yang paling mendekati:\n\n")
                
                for i, rec in enumerate(rekomendasi_mendekati, 1):
                    f.write(f"{i}. 🥗 {rec['kondisi']}\n")
                    f.write(f"   {rec['status']}\n")
                    f.write(f"   ({rec.get('kriteria_terpenuhi', 0)} dari {rec.get('total_kriteria', 0)} kriteria terpenuhi)\n\n")
                    f.write(f"   📝 Penjelasan:\n")
                    f.write(f"   {rec['penjelasan']}\n\n")
                    f.write(f"   🍽️ Rekomendasi Makanan:\n")
                    for r in rec['rekomendasi']:
                        f.write(f"      {r}\n")
                    f.write("\n")
        
        # FOOTER
        f.write("\n" + "=" * 70 + "\n")
        f.write("⚠️ DISCLAIMER MEDIS ⚠️\n")
        f.write("Sistem ini hanya untuk EDUKASI GIZI. Bukan pengganti konsultasi\n")
        f.write("dengan dokter atau ahli gizi. Jika gejala parah atau berlanjut,\n")
        f.write("segera konsultasikan ke tenaga kesehatan profesional.\n")
        f.write("=" * 70 + "\n")
        f.write(f"\n📁 File ini disimpan pada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    return filename