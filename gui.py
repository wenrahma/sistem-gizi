# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict
import os

from config import *
from questions import QUESTIONS, get_total_questions
from knowledge_base import RULES
from inference import forward_chaining, explain_recommendation
from utils import save_recommendations_to_file


class SistemPakarGiziApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        
        self.fakta = {}
        self.current_question_index = 0
        self.riwayat_jawaban = []
        
        self.create_widgets()
        self.tampil_pertanyaan()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, height=130)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🥗 SISTEM PAKAR GIZI & POLA MAKAN", 
                               font=("Arial", 18, "bold"), 
                               fg="white", bg=PRIMARY_COLOR)
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header_frame, text="Kenali kondisi gizi Anda dan dapatkan rekomendasi makanan yang tepat!", 
                                  font=("Arial", 10), 
                                  fg="#ecf0f1", bg=PRIMARY_COLOR)
        subtitle_label.pack()
        
        info_label = tk.Label(header_frame, text=f"📋 {get_total_questions()} Pertanyaan | 🥗 {len(RULES)} Kondisi Gizi | ⚙️ Forward Chaining", 
                             font=("Arial", 9), 
                             fg="#d5f5e3", bg=PRIMARY_COLOR)
        info_label.pack(pady=5)
        
        disclaimer_label = tk.Label(header_frame, text="⚠️ EDUKASI GIZI - BUKAN PENGGANTI DOKTER", 
                                   font=("Arial", 8, "bold"), 
                                   fg="#f9e79f", bg=PRIMARY_COLOR)
        disclaimer_label.pack()
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, 
                                           length=600, mode='determinate')
        self.progress_bar.pack(pady=(0, 15))
        
        self.progress_label = tk.Label(self.main_frame, text="", bg=BG_COLOR, 
                                       font=("Arial", 10), fg=PRIMARY_COLOR)
        self.progress_label.pack()
        
        # Question frame
        self.question_frame = tk.Frame(self.main_frame, bg="white", relief=tk.RAISED, bd=1)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.question_label = tk.Label(self.question_frame, text="", 
                                       font=("Arial", 14), 
                                       wraplength=750, 
                                       bg="white", 
                                       fg=PRIMARY_COLOR,
                                       pady=50,
                                       padx=30)
        self.question_label.pack(expand=True)
        
        # Button frame
        button_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        self.btn_kembali = tk.Button(button_frame, text="◀ KEMBALI", 
                                    font=("Arial", 10, "bold"),
                                    bg=WARNING_COLOR, 
                                    fg="white",
                                    width=12,
                                    height=1,
                                    command=self.kembali)
        self.btn_kembali.pack(side=tk.LEFT, padx=10)
        self.btn_kembali.config(state=tk.DISABLED)
        
        self.btn_ya = tk.Button(button_frame, text="✅ YA", 
                               font=("Arial", 12, "bold"),
                               bg=SUCCESS_COLOR, 
                               fg="white",
                               width=12,
                               height=1,
                               command=lambda: self.jawab(True))
        self.btn_ya.pack(side=tk.LEFT, padx=10)
        
        self.btn_tidak = tk.Button(button_frame, text="❌ TIDAK", 
                                  font=("Arial", 12, "bold"),
                                  bg=DANGER_COLOR, 
                                  fg="white",
                                  width=12,
                                  height=1,
                                  command=lambda: self.jawab(False))
        self.btn_tidak.pack(side=tk.LEFT, padx=10)
        
        self.btn_reset = tk.Button(self.main_frame, text="🔄 Mulai Lagi", 
                                  font=("Arial", 10),
                                  bg=SECONDARY_COLOR, 
                                  fg="white",
                                  padx=20, 
                                  pady=5,
                                  command=self.reset_sistem)
    
    def kembali(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            _, key = QUESTIONS[self.current_question_index]
            if key in self.fakta:
                del self.fakta[key]
            if self.riwayat_jawaban:
                self.riwayat_jawaban.pop()
            self.tampil_pertanyaan()
            self.btn_ya.config(state=tk.NORMAL)
            self.btn_tidak.config(state=tk.NORMAL)
    
    def tampil_pertanyaan(self):
        if self.current_question_index < len(QUESTIONS):
            text, key = QUESTIONS[self.current_question_index]
            
            jawaban_sebelumnya = self.fakta.get(key)
            if jawaban_sebelumnya is not None:
                status = "✅ (Sudah dijawab: YA)" if jawaban_sebelumnya else "❌ (Sudah dijawab: TIDAK)"
                self.question_label.config(text=f"{text}\n\n┌─────────────────────────────────────────┐\n│ {status} │\n└─────────────────────────────────────────┘")
            else:
                self.question_label.config(text=text)
            
            progress = (self.current_question_index / len(QUESTIONS)) * 100
            self.progress_var.set(progress)
            self.progress_label.config(text=f"Pertanyaan {self.current_question_index + 1} dari {len(QUESTIONS)}")
            
            if self.current_question_index == 0:
                self.btn_kembali.config(state=tk.DISABLED)
            else:
                self.btn_kembali.config(state=tk.NORMAL)
        else:
            self.proses_rekomendasi()
    
    def jawab(self, jawaban: bool):
        _, key = QUESTIONS[self.current_question_index]
        self.fakta[key] = jawaban
        self.riwayat_jawaban.append((self.current_question_index, key, jawaban))
        self.current_question_index += 1
        self.tampil_pertanyaan()
    
    def proses_rekomendasi(self):
        self.btn_ya.pack_forget()
        self.btn_tidak.pack_forget()
        self.btn_kembali.pack_forget()
        
        hasil = forward_chaining(self.fakta, RULES)
        
        if not hasil["tepat"] and not hasil["mendekati"]:
            messagebox.showinfo("Hasil Konsultasi", 
                               "Berdasarkan jawaban Anda, tidak ditemukan kondisi gizi yang signifikan.\n"
                               "Pola makan dan gaya hidup Anda sudah cukup sehat! Tetap pertahankan ya! 💪")
            self.btn_reset.pack(pady=10)
            return
        
        self.question_label.pack_forget()
        self.progress_label.pack_forget()
        self.progress_bar.pack_forget()
        
        hasil_frame = tk.Frame(self.question_frame, bg="white")
        hasil_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_area = scrolledtext.ScrolledText(hasil_frame, wrap=tk.WORD, 
                                              font=("Arial", 11), 
                                              height=20,
                                              bg="#fafafa")
        text_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
        explanation = explain_recommendation(hasil)
        text_area.insert(tk.END, explanation)
        text_area.config(state=tk.DISABLED)
        
        action_frame = tk.Frame(hasil_frame, bg="white")
        action_frame.pack(pady=10)
        
        btn_simpan = tk.Button(action_frame, text="💾 Simpan Hasil", 
                              font=("Arial", 10),
                              bg=SECONDARY_COLOR, 
                              fg="white",
                              padx=15, 
                              pady=5,
                              command=lambda: self.simpan_hasil(hasil))
        btn_simpan.pack(side=tk.LEFT, padx=10)
        
        btn_reset_here = tk.Button(action_frame, text="🔄 Test Lagi", 
                                  font=("Arial", 10),
                                  bg=WARNING_COLOR, 
                                  fg="white",
                                  padx=15, 
                                  pady=5,
                                  command=self.reset_sistem)
        btn_reset_here.pack(side=tk.LEFT, padx=10)
        
        btn_exit = tk.Button(action_frame, text="❌ Keluar", 
                            font=("Arial", 10),
                            bg=DANGER_COLOR, 
                            fg="white",
                            padx=15, 
                            pady=5,
                            command=self.root.quit)
        btn_exit.pack(side=tk.LEFT, padx=10)
    
    def simpan_hasil(self, hasil):
        try:
            filename = save_recommendations_to_file(hasil)
            abs_path = os.path.abspath(filename)
            messagebox.showinfo("Berhasil", f"✅ Hasil rekomendasi telah disimpan ke:\n{abs_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {str(e)}")
    
    def reset_sistem(self):
        self.fakta = {}
        self.current_question_index = 0
        self.riwayat_jawaban = []
        
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        
        self.progress_bar.pack(pady=(0, 15))
        self.progress_label.pack()
        
        self.question_label = tk.Label(self.question_frame, text="", 
                                       font=("Arial", 14), 
                                       wraplength=750, 
                                       bg="white", 
                                       fg=PRIMARY_COLOR,
                                       pady=50,
                                       padx=30)
        self.question_label.pack(expand=True)
        
        self.btn_ya.pack(side=tk.LEFT, padx=10)
        self.btn_tidak.pack(side=tk.LEFT, padx=10)
        self.btn_kembali.pack(side=tk.LEFT, padx=10)
        self.btn_kembali.config(state=tk.DISABLED)
        self.btn_reset.pack_forget()
        
        self.tampil_pertanyaan()