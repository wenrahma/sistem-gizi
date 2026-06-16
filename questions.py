# questions.py

QUESTIONS = [
    # === GEJALA FISIK (1-10) ===
    ("Apakah Anda sering merasa lelah/letih meskipun cukup tidur?", "gejala_lelah"),
    ("Apakah rambut Anda mudah rontok?", "gejala_rambut_rontok"),
    ("Apakah kuku Anda mudah patah/bergaris putih?", "gejala_kuku_rapuh"),
    ("Apakah Anda sering sariawan?", "gejala_sariawan"),
    ("Apakah gusi Anda mudah berdarah saat menyikat gigi?", "gejala_gusi_berdarah"),
    ("Apakah Anda sering kesemutan atau kram otot?", "gejala_kesemutan"),
    ("Apakah tulang Anda terasa nyeri?", "gejala_nyeri_tulang"),
    ("Apakah Anda sering pusing?", "gejala_pusing"),
    ("Apakah luka Anda lama sembuhnya?", "gejala_luka_lama"),
    ("Apakah Anda sering sakit (flu, batuk, demam)?", "gejala_sering_sakit"),
    
    # === POLA MAKAN (11-15) ===
    ("Apakah Anda jarang makan sayur (kurang dari 3x/minggu)?", "pola_jarang_sayur"),
    ("Apakah Anda jarang makan buah (kurang dari 3x/minggu)?", "pola_jarang_buah"),
    ("Apakah Anda mengonsumsi produk susu/minimal?", "pola_kurang_susu"),
    ("Apakah Anda minum air putih <8 gelas per hari?", "pola_kurang_air"),
    ("Apakah Anda vegetarian atau vegan?", "pola_vegetarian"),
    
    # === KEBIASAAN (16-20) ===
    ("Apakah Anda jarang terkena sinar matahari pagi?", "kebiasaan_jarang_matahari"),
    ("Apakah Anda sering makan junk food/makanan instan?", "pola_sering_junkfood"),
    ("Apakah Anda makan makanan bergaram berlebihan?", "pola_garam_berlebih"),
    ("Apakah Anda suka minum kopi/teh setelah makan?", "pola_kopi_setelah_makan"),
    ("Apakah Anda sedang menjalani diet ketat?", "kebiasaan_diet_ketat"),
]

def get_total_questions():
    return len(QUESTIONS)

def get_all_question_keys():
    return [key for _, key in QUESTIONS]