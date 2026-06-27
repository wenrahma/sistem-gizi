# inference.py
from typing import Dict, List

def forward_chaining(fakta_pengguna: Dict[str, bool], rules: List[Dict]) -> Dict:
    rekomendasi_tepat = []
    rekomendasi_mendekati = []
    
    for rule in rules:
        total = len(rule["if"])
        terpenuhi = 0
        
        for kondisi, nilai in rule["if"].items():
            if fakta_pengguna.get(kondisi, False) == nilai:
                terpenuhi += 1
        
        if terpenuhi == total:
            rekomendasi_tepat.append({
                "kondisi": rule["then"]["kondisi"],
                "rekomendasi": rule["then"]["rekomendasi"],
                "penjelasan": rule["then"]["penjelasan"],
                "status": "✅ SANGAT COCOK - 100%",
                "kriteria_terpenuhi": terpenuhi,
                "total_kriteria": total
            })
        elif terpenuhi >= total - 1:
            rekomendasi_mendekati.append({
                "kondisi": rule["then"]["kondisi"],
                "rekomendasi": rule["then"]["rekomendasi"],
                "penjelasan": rule["then"]["penjelasan"],
                "status": f"⚠️ COCOK - ({terpenuhi}/{total})",
                "kriteria_terpenuhi": terpenuhi,
                "total_kriteria": total
            })
    
    return {"tepat": rekomendasi_tepat, "mendekati": rekomendasi_mendekati}


def explain_recommendation(hasil: Dict, nama: str = "", usia: str = "") -> str:
    header = "=" * 70 + "\n"
    header += " " * 18 + "SISTEM PAKAR GIZI & POLA MAKAN\n"
    header += "=" * 70 + "\n"
    if nama and usia:
        header += f"👤 {nama}  |  📅 {usia} tahun\n"
        header += "─" * 70 + "\n"
    header += "=" * 70 + "\n\n"
    
    if not hasil["tepat"] and not hasil["mendekati"]:
        return header + "❌ TIDAK ADA REKOMENDASI\n\nPola makan Anda sudah cukup sehat! 💪"
    
    text = header
    
    if hasil["tepat"]:
        text += "🎯 REKOMENDASI UTAMA\n" + "─" * 70 + "\n\n"
        for i, rec in enumerate(hasil["tepat"], 1):
            text += f"{i}. 🥗 {rec['kondisi']}\n"
            text += f"   {rec['status']}\n\n"
            text += f"   📝 {rec['penjelasan']}\n\n"
            text += f"   🍽️ REKOMENDASI:\n"
            for r in rec['rekomendasi']:
                text += f"      {r}\n"
            text += "\n"
    
    if hasil["mendekati"]:
        if hasil["tepat"]:
            text += "\n🔄 REKOMENDASI LAIN\n" + "─" * 70 + "\n\n"
        else:
            text += "🔄 REKOMENDASI TERDEKAT\n" + "─" * 70 + "\n\n"
        
        for i, rec in enumerate(hasil["mendekati"], 1):
            text += f"{i}. 🥗 {rec['kondisi']}\n"
            text += f"   {rec['status']}\n\n"
            for r in rec['rekomendasi'][:3]:
                text += f"      {r}\n"
            text += "\n"
    
    text += "=" * 70 + "\n"
    text += "⚠️ EDUKASI GIZI - BUKAN PENGGANTI DOKTER\n"
    text += "=" * 70
    
    return text