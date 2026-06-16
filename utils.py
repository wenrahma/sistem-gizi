# utils.py
import os
from datetime import datetime
from typing import List, Dict

def save_recommendations_to_file(hasil_rekomendasi: Dict, folder: str = "data/hasil_rekomendasi") -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"rekomendasi_gizi_{timestamp}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("SISTEM PAKAR REKOMENDASI GIZI & POLA MAKAN\n")
        f.write(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        for rec in hasil_rekomendasi.get("tepat", []):
            f.write(f"\nREKOMENDASI: {rec['kondisi']}\n")
            f.write("-" * 50 + "\n")
            f.write(f"{rec['status']}\n\n")
            f.write(f"Penjelasan: {rec['penjelasan']}\n\n")
            f.write("Rekomendasi:\n")
            for r in rec['rekomendasi']:
                f.write(f"  {r}\n")
            f.write("\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("⚠️ DISCLAIMER: Ini hanya edukasi gizi, bukan konsultasi medis.\n")
    
    return filename