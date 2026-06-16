# knowledge_base.py
# Versi RINGKAS - 6 aturan untuk UAS

RULES = [
    # 1. Defisiensi Zat Besi (Anemia)
    {
        "if": {
            "gejala_lelah": True,
            "gejala_rambut_rontok": True,
            "gejala_kuku_rapuh": True,
            "gejala_pusing": True,
            "pola_jarang_sayur": True
        },
        "then": {
            "kondisi": "Defisiensi Zat Besi (Anemia ringan)",
            "rekomendasi": [
                "🍖 Konsumsi hati ayam/sapi 1x/minggu",
                "🥬 Makan bayam, kangkung, brokoli",
                "🥜 Tambahkan kacang-kacangan",
                "🍊 Konsumsi vitamin C untuk membantu penyerapan"
            ],
            "penjelasan": "Zat besi penting untuk pembentukan hemoglobin. Kekurangan zat besi menyebabkan kelelahan, rambut rontok, pusing, dan kuku rapuh."
        },
        "penjelasan_singkat": "Lelah + rambut rontok + jarang sayur = defisiensi zat besi."
    },
    
    # 2. Defisiensi Vitamin C
    {
        "if": {
            "gejala_sariawan": True,
            "gejala_gusi_berdarah": True,
            "gejala_luka_lama": True,
            "pola_jarang_buah": True
        },
        "then": {
            "kondisi": "Defisiensi Vitamin C",
            "rekomendasi": [
                "🍊 Konsumsi jeruk, jambu biji, kiwi setiap hari",
                "🫑 Makan paprika merah, brokoli, tomat",
                "🥦 Sayuran segar lebih baik (vitamin C rusak oleh panas)",
                "💊 Suplemen vitamin C jika perlu"
            ],
            "penjelasan": "Vitamin C penting untuk pembentukan kolagen dan penyembuhan luka. Kekurangan vitamin C menyebabkan sariawan, gusi berdarah, dan luka sulit sembuh."
        },
        "penjelasan_singkat": "Sariawan + gusi berdarah + jarang buah = defisiensi vitamin C."
    },
    
    # 3. Defisiensi Vitamin D
    {
        "if": {
            "gejala_nyeri_tulang": True,
            "gejala_kesemutan": True,
            "gejala_sering_sakit": True,
            "kebiasaan_jarang_matahari": True
        },
        "then": {
            "kondisi": "Defisiensi Vitamin D",
            "rekomendasi": [
                "☀️ Berjemur 15-30 menit sebelum jam 9 pagi",
                "🐟 Konsumsi ikan salmon, tuna, sarden",
                "🥚 Makan kuning telur",
                "🥛 Minum susu yang diperkaya vitamin D"
            ],
            "penjelasan": "Vitamin D membantu penyerapan kalsium. Kekurangan vitamin D menyebabkan nyeri tulang, kesemutan, dan daya tahan tubuh menurun."
        },
        "penjelasan_singkat": "Nyeri tulang + jarang matahari = defisiensi vitamin D."
    },
    
    # 4. Defisiensi Kalsium
    {
        "if": {
            "gejala_kesemutan": True,
            "gejala_kuku_rapuh": True,
            "gejala_nyeri_tulang": True,
            "pola_kurang_susu": True
        },
        "then": {
            "kondisi": "Defisiensi Kalsium",
            "rekomendasi": [
                "🥛 Minum susu 2 gelas/hari atau yogurt",
                "🧀 Konsumsi keju, tahu, tempe",
                "🥬 Makan sayuran hijau (brokoli, bayam)",
                "🐟 Ikan teri dengan tulangnya"
            ],
            "penjelasan": "Kalsium penting untuk tulang dan gigi. Kekurangan kalsium menyebabkan kram otot, kuku rapuh, dan risiko osteoporosis."
        },
        "penjelasan_singkat": "Kesemutan + kurang susu + nyeri tulang = defisiensi kalsium."
    },
    
    # 5. Dehidrasi
    {
        "if": {
            "pola_kurang_air": True,
            "gejala_pusing": True,
            "gejala_lelah": True
        },
        "then": {
            "kondisi": "Dehidrasi Ringan",
            "rekomendasi": [
                "💧 Minum 8-10 gelas air putih per hari",
                "📱 Gunakan aplikasi pengingat minum air",
                "🍉 Konsumsi buah berair (semangka, jeruk)",
                "☕ Kurangi kafein (kopi, teh)"
            ],
            "penjelasan": "Air penting untuk semua fungsi tubuh. Dehidrasi menyebabkan pusing, lelah, dan sulit fokus."
        },
        "penjelasan_singkat": "Kurang minum + pusing + lelah = dehidrasi."
    },
    
    # 6. Kelebihan Garam
    {
        "if": {
            "pola_garam_berlebih": True,
            "gejala_pusing": True,
            "pola_sering_junkfood": True
        },
        "then": {
            "kondisi": "Kelebihan Asupan Garam (Risiko Hipertensi)",
            "rekomendasi": [
                "🧂 Kurangi garam (maks 1 sendok teh/hari)",
                "🥗 Hindari makanan olahan, mie instan",
                "🍌 Perbanyak kalium dari pisang, alpukat",
                "💧 Minum air putih lebih banyak"
            ],
            "penjelasan": "Kelebihan garam meningkatkan tekanan darah dan risiko penyakit jantung."
        },
        "penjelasan_singkat": "Makanan asin + pusing = kelebihan garam."
    },
]

def get_total_rules():
    return len(RULES)

def get_all_jurusan():
    return [rule["then"]["kondisi"] for rule in RULES]