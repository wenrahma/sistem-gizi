# utils.py
import os
from datetime import datetime
from typing import Dict

def save_recommendations_to_file(hasil_rekomendasi: Dict, nama: str = "", usia: str = "", 
                                  folder: str = "data/hasil_rekomendasi") -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"rekomendasi_{timestamp}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(" " * 18 + "SISTEM PAKAR GIZI & POLA MAKAN\n")
        f.write("=" * 70 + "\n")
        f.write(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        if nama and usia:
            f.write(f"👤 {nama}  |  📅 {usia} tahun\n")
        f.write("=" * 70 + "\n\n")
        
        for rec in hasil_rekomendasi.get("tepat", []):
            f.write(f"✅ {rec['kondisi']}\n")
            f.write("-" * 50 + "\n")
            f.write(f"{rec['status']}\n\n")
            f.write(f"{rec['penjelasan']}\n\n")
            f.write("Rekomendasi:\n")
            for r in rec['rekomendasi']:
                f.write(f"  {r}\n")
            f.write("\n")
        
        for rec in hasil_rekomendasi.get("mendekati", []):
            f.write(f"⚠️ {rec['kondisi']}\n")
            f.write("-" * 50 + "\n")
            f.write(f"{rec['status']}\n\n")
            f.write("Rekomendasi:\n")
            for r in rec['rekomendasi'][:3]:
                f.write(f"  {r}\n")
            f.write("\n")
        
        f.write("=" * 70 + "\n")
        f.write("⚠️ EDUKASI GIZI - BUKAN PENGGANTI DOKTER\n")
    
    return filename