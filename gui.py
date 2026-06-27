# gui.py
# Sistem Pakar Gizi & Pola Makan - Dengan Input Nama dan Usia

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
        
        # Data Pengguna
        self.nama = ""
        self.usia = ""
        
        # Data Jawaban
        self.fakta = {}
        self.current_question_index = 0
        self.riwayat_jawaban = []
        
        self.create_widgets()
        self.tampil_form_identitas()
    
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
        
        self.progress_label = tk.Label(self.main_frame, text="", bg=BG_COLOR, 
                                       font=("Arial", 10), fg=PRIMARY_COLOR)
        
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
        
        # Sembunyikan di awal
        self.btn_kembali.pack_forget()
        self.btn_ya.pack_forget()
        self.btn_tidak.pack_forget()
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
    
    # ========== FORM IDENTITAS ==========
    def tampil_form_identitas(self):
        """Menampilkan form input nama dan usia"""
        
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        
        form_frame = tk.Frame(self.question_frame, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=50)
        
        # Judul
        judul = tk.Label(form_frame, text="👤 IDENTITAS DIRI", 
                        font=("Arial", 16, "bold"), 
                        bg="white", fg=PRIMARY_COLOR)
        judul.pack(pady=(0, 10))
        
        sub_judul = tk.Label(form_frame, text="Silakan isi data diri Anda sebelum memulai konsultasi", 
                            font=("Arial", 10), 
                            bg="white", fg="#7f8c8d")
        sub_judul.pack(pady=(0, 30))
        
        # Frame input
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(pady=10)
        
        # Nama
        tk.Label(input_frame, text="Nama:", font=("Arial", 12), 
                bg="white", fg=PRIMARY_COLOR).grid(row=0, column=0, pady=10, padx=(0, 10))
        self.entry_nama = tk.Entry(input_frame, font=("Arial", 12), 
                                   width=25, relief=tk.GROOVE, bd=2)
        self.entry_nama.grid(row=0, column=1, pady=10)
        self.entry_nama.focus_set()
        
        # Usia
        tk.Label(input_frame, text="Usia:", font=("Arial", 12), 
                bg="white", fg=PRIMARY_COLOR).grid(row=1, column=0, pady=10, padx=(0, 10))
        self.entry_usia = tk.Entry(input_frame, font=("Arial", 12), 
                                   width=10, relief=tk.GROOVE, bd=2)
        self.entry_usia.grid(row=1, column=1, sticky="w", pady=10)
        
        # Tombol
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=30)
        
        btn_mulai = tk.Button(btn_frame, text="🚀 MULAI", 
                             font=("Arial", 12, "bold"),
                             bg=SECONDARY_COLOR, fg="white",
                             padx=30, pady=10,
                             command=self.simpan_identitas)
        btn_mulai.pack()
        
        btn_keluar = tk.Button(btn_frame, text="❌ Keluar", 
                              font=("Arial", 10),
                              bg=DANGER_COLOR, fg="white",
                              padx=15, pady=5,
                              command=self.root.quit)
        btn_keluar.pack(pady=(10, 0))
    
    def simpan_identitas(self):
        nama = self.entry_nama.get().strip()
        usia = self.entry_usia.get().strip()
        
        if not nama:
            messagebox.showwarning("Peringatan", "Masukkan nama Anda!")
            self.entry_nama.focus_set()
            return
        
        if not usia:
            messagebox.showwarning("Peringatan", "Masukkan usia Anda!")
            self.entry_usia.focus_set()
            return
        
        if not usia.isdigit():
            messagebox.showwarning("Peringatan", "Usia harus angka!")
            self.entry_usia.delete(0, tk.END)
            self.entry_usia.focus_set()
            return
        
        self.nama = nama
        self.usia = usia
        
        # Hapus form
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        
        # Kembalikan label pertanyaan
        self.question_label = tk.Label(self.question_frame, text="", 
                                       font=("Arial", 14), 
                                       wraplength=750, 
                                       bg="white", 
                                       fg=PRIMARY_COLOR,
                                       pady=50,
                                       padx=30)
        self.question_label.pack(expand=True)
        
        # Tampilkan komponen
        self.progress_bar.pack(pady=(0, 15))
        self.progress_label.pack()
        self.btn_ya.pack(side=tk.LEFT, padx=10)
        self.btn_tidak.pack(side=tk.LEFT, padx=10)
        self.btn_kembali.pack(side=tk.LEFT, padx=10)
        
        self.tampil_pertanyaan()
    
    # ========== FUNGSI UTAMA ==========
    def kembali(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            _, key = QUESTIONS[self.current_question_index]
            if key in self.fakta:
                del self.fakta[key]
            if self.riwayat_jawaban:
                self.riwayat_jawaban.pop()
            self.tampil_pertanyaan()
    
    def tampil_pertanyaan(self):
        if self.current_question_index < len(QUESTIONS):
            text, key = QUESTIONS[self.current_question_index]
            
            jawaban_sebelumnya = self.fakta.get(key)
            if jawaban_sebelumnya is not None:
                status = "✅ YA" if jawaban_sebelumnya else "❌ TIDAK"
                self.question_label.config(text=f"{text}\n\n┌─────────────────────────┐\n│ {status} │\n└─────────────────────────┘")
            else:
                self.question_label.config(text=text)
            
            progress = (self.current_question_index / len(QUESTIONS)) * 100
            self.progress_var.set(progress)
            self.progress_label.config(text=f"Pertanyaan {self.current_question_index + 1} dari {len(QUESTIONS)}")
            
            self.btn_kembali.config(state=tk.DISABLED if self.current_question_index == 0 else tk.NORMAL)
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
                               "Tidak ditemukan kondisi gizi yang signifikan.\n"
                               "Pola makan Anda sudah cukup sehat! 💪")
            self.btn_reset.pack(pady=10)
            return
        
        self.question_label.pack_forget()
        self.progress_label.pack_forget()
        self.progress_bar.pack_forget()
        
        hasil_frame = tk.Frame(self.question_frame, bg="white")
        hasil_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ===== INFO PENGGUNA =====
        info_frame = tk.Frame(hasil_frame, bg="#e8f8f5", relief=tk.GROOVE, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(info_frame, text=f"👤 {self.nama}  |  📅 {self.usia} tahun", 
                font=("Arial", 11, "bold"), bg="#e8f8f5", fg=PRIMARY_COLOR, pady=8).pack()
        
        # ===== HASIL =====
        text_area = scrolledtext.ScrolledText(hasil_frame, wrap=tk.WORD, 
                                              font=("Arial", 11), height=18, bg="#fafafa")
        text_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
        explanation = explain_recommendation(hasil, self.nama, self.usia)
        text_area.insert(tk.END, explanation)
        text_area.config(state=tk.DISABLED)
        
        # ===== TOMBOL =====
        action_frame = tk.Frame(hasil_frame, bg="white")
        action_frame.pack(pady=10)
        
        btn_simpan = tk.Button(action_frame, text="💾 Simpan", 
                              font=("Arial", 10), bg=SECONDARY_COLOR, fg="white",
                              padx=15, pady=5,
                              command=lambda: self.simpan_hasil(hasil))
        btn_simpan.pack(side=tk.LEFT, padx=10)
        
        btn_reset_here = tk.Button(action_frame, text="🔄 Ulang", 
                                  font=("Arial", 10), bg=WARNING_COLOR, fg="white",
                                  padx=15, pady=5, command=self.reset_sistem)
        btn_reset_here.pack(side=tk.LEFT, padx=10)
        
        btn_exit = tk.Button(action_frame, text="❌ Keluar", 
                            font=("Arial", 10), bg=DANGER_COLOR, fg="white",
                            padx=15, pady=5, command=self.root.quit)
        btn_exit.pack(side=tk.LEFT, padx=10)
    
    def simpan_hasil(self, hasil):
        try:
            filename = save_recommendations_to_file(hasil, self.nama, self.usia)
            messagebox.showinfo("Berhasil", f"✅ Hasil disimpan di:\n{os.path.abspath(filename)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def reset_sistem(self):
        self.fakta = {}
        self.current_question_index = 0
        self.riwayat_jawaban = []
        
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        
        self.progress_bar.pack(pady=(0, 15))
        self.progress_label.pack()
        
        self.question_label = tk.Label(self.question_frame, text="", 
                                       font=("Arial", 14), wraplength=750,
                                       bg="white", fg=PRIMARY_COLOR, pady=50, padx=30)
        self.question_label.pack(expand=True)
        
        self.btn_ya.pack(side=tk.LEFT, padx=10)
        self.btn_tidak.pack(side=tk.LEFT, padx=10)
        self.btn_kembali.pack(side=tk.LEFT, padx=10)
        self.btn_kembali.config(state=tk.DISABLED)
        self.btn_reset.pack_forget()
        
        self.tampil_form_identitas()