# inference.py
from typing import Dict, List

def forward_chaining(fakta_pengguna: Dict[str, bool], rules: List[Dict]) -> Dict:
    """
    Forward chaining MURNI untuk sistem pakar gizi
    """
    rekomendasi_tepat = []
    rekomendasi_mendekati = []
    
    for rule in rules:
        kondisi_yang_diperlukan = rule["if"]
        total_kondisi = len(kondisi_yang_diperlukan)
        kondisi_terpenuhi = 0
        kondisi_tidak_terpenuhi = []
        
        for kondisi, nilai_yang_diharapkan in kondisi_yang_diperlukan.items():
            nilai_pengguna = fakta_pengguna.get(kondisi, False)
            if nilai_pengguna == nilai_yang_diharapkan:
                kondisi_terpenuhi += 1
            else:
                kondisi_tidak_terpenuhi.append(kondisi)
        
        if kondisi_terpenuhi == total_kondisi:
            rekomendasi_tepat.append({
                "kondisi": rule["then"]["kondisi"],
                "rekomendasi": rule["then"]["rekomendasi"],
                "penjelasan": rule["then"]["penjelasan"],
                "status": "✅ SANGAT COCOK - Semua indikator terpenuhi",
                "kriteria_terpenuhi": kondisi_terpenuhi,
                "total_kriteria": total_kondisi
            })
        elif kondisi_terpenuhi >= total_kondisi - 1:
            rekomendasi_mendekati.append({
                "kondisi": rule["then"]["kondisi"],
                "rekomendasi": rule["then"]["rekomendasi"],
                "penjelasan": rule["then"]["penjelasan"],
                "status": f"⚠️ COCOK - ({kondisi_terpenuhi} dari {total_kondisi} indikator terpenuhi)",
                "kriteria_terpenuhi": kondisi_terpenuhi,
                "total_kriteria": total_kondisi
            })
    
    return {"tepat": rekomendasi_tepat, "mendekati": rekomendasi_mendekati}


def explain_recommendation(hasil: Dict) -> str:
    rekomendasi_tepat = hasil["tepat"]
    rekomendasi_mendekati = hasil["mendekati"]
    
    if not rekomendasi_tepat and not rekomendasi_mendekati:
        return "=" * 70 + "\n" + \
               " " * 20 + "TIDAK ADA REKOMENDASI\n" + \
               "=" * 70 + "\n\n" + \
               "Berdasarkan jawaban Anda, tidak ditemukan kondisi gizi yang signifikan.\n\n" + \
               "✅ Kabar baik! Pola makan dan gaya hidup Anda sudah cukup sehat.\n\n" + \
               "💡 SARAN UMUM:\n" + \
               "   1. Tetap jaga pola makan seimbang (sayur, buah, protein)\n" + \
               "   2. Minum air putih 8 gelas/hari\n" + \
               "   3. Olahraga teratur 30 menit/hari\n" + \
               "   4. Tidur cukup 7-8 jam/hari\n\n" + \
               "=" * 70
    
    explanation = "=" * 70 + "\n"
    explanation += " " * 15 + "SISTEM PAKAR GIZI & POLA MAKAN\n"
    explanation += "=" * 70 + "\n\n"
    
    if rekomendasi_tepat:
        explanation += "🎯 REKOMENDASI UTAMA (Sangat Cocok)\n"
        explanation += "─" * 70 + "\n\n"
        
        for i, rec in enumerate(rekomendasi_tepat, 1):
            explanation += f"{i}. 🥗 {rec['kondisi']}\n"
            explanation += f"   {rec['status']}\n\n"
            explanation += f"   📝 PENJELASAN:\n   {rec['penjelasan']}\n\n"
            explanation += f"   🍽️ REKOMENDASI:\n"
            for r in rec['rekomendasi']:
                explanation += f"      {r}\n"
            explanation += "\n"
    
    if rekomendasi_mendekati:
        if rekomendasi_tepat:
            explanation += "\n🔄 REKOMENDASI LAIN (Cukup Cocok)\n"
            explanation += "─" * 70 + "\n\n"
        else:
            explanation += "🔄 REKOMENDASI TERDEKAT\n"
            explanation += "─" * 70 + "\n\n"
            explanation += "💡 Berikut kondisi yang paling mendekati profil Anda:\n\n"
        
        for i, rec in enumerate(rekomendasi_mendekati, 1):
            explanation += f"{i}. 🥗 {rec['kondisi']}\n"
            explanation += f"   {rec['status']}\n\n"
            explanation += f"   🍽️ REKOMENDASI:\n"
            for r in rec['rekomendasi'][:3]:
                explanation += f"      {r}\n"
            explanation += "\n"
    
    explanation += "=" * 70 + "\n"
    explanation += "⚠️ DISCLAIMER MEDIS ⚠️\n"
    explanation += "Sistem ini hanya untuk EDUKASI GIZI. Bukan pengganti konsultasi dengan\n"
    explanation += "dokter atau ahli gizi. Jika gejala parah/berlanjut, segera konsultasi\n"
    explanation += "ke tenaga kesehatan profesional.\n"
    explanation += "=" * 70
    
    return explanation