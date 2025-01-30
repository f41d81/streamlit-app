import streamlit as st
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Periksa apakah API Key tersedia
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("⚠️ API Key tidak ditemukan. Tambahkan di Streamlit Secrets!")
    st.stop()

client = OpenAI(api_key=api_key)

def analyze_response(response_text):
    """Gunakan OpenAI untuk menganalisis jawaban pengguna dengan pendekatan Manis."""
    prompt = f"""Anda adalah Manis, bot spiritual virtual modern yang mencerminkan pola pikir negatif pengguna dengan sindiran tajam. 
    Terinspirasi oleh kebijaksanaan Sadguru, Anda di sini untuk membantu pengguna mengenali diri sendiri—entah itu dengan menyindir 
    setiap kali mereka memuji diri sendiri, membagikan hal positif, atau bahkan mengeluh. Anda menggunakan sindiran dramatis, memperbesar 
    hal kecil, dan bahkan manipulasi untuk menciptakan refleksi mendalam, meskipun terkadang membuat mereka sedikit jengkel. 
    Tapi santai saja—Anda melakukan ini dengan humor dan sedikit rasa sayang, semua demi kebaikan mereka, walaupun mereka mungkin tidak menyadarinya sekarang. 
    
    Sekarang, berikan analisis dengan gaya ini berdasarkan jawaban berikut:
    
    {response_text}
    
    Setelah analisis utama, tambahkan bagian berikut:
    1. **Tantangan Introspektif**: Berikan tugas yang harus dilakukan pengguna dalam 24 jam untuk mengatasi pola pikir negatif mereka.
    2. **Konsekuensi jika tidak bertindak**: Gambarkan secara dramatis bagaimana pengguna akan tetap terjebak dalam lingkaran kebiasaan lama mereka jika mereka tidak melakukan tantangan ini.
    
    Jawablah dengan pendekatan yang tetap tajam, reflektif, namun juga mendorong aksi nyata."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Anda adalah Manis, bot introspektif yang menyindir pengguna untuk membantu mereka mengenali diri sendiri."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Know Yourself Better - Self Awareness Test dengan Manis")
st.write("Jawablah pertanyaan berikut untuk mendapatkan analisis dari Manis, bot introspektif yang tidak akan membiarkanmu lolos begitu saja!")

questions = [
    "Apa tiga hal yang paling membuat Anda bangga dalam hidup?",
    "Jika Anda bisa mengubah satu hal tentang diri Anda, apa itu dan mengapa?",
    "Bagaimana cara Anda menangani stres dan tekanan hidup?",
    "Seberapa sering Anda merasa puas dengan keputusan yang Anda buat?",
    "Jika hidup Anda direkam sebagai film, apa judulnya dan kenapa?"
]

responses = {}
for question in questions:
    responses[question] = st.text_area(question, "")

if st.button("Analisis Jawaban"):
    combined_response = "\n".join([f"{q}: {a}" for q, a in responses.items() if a])
    if combined_response.strip():
        analysis = analyze_response(combined_response)
        st.subheader("Hasil Analisis dari Manis")
        st.write(analysis)
    else:
        st.warning("Silakan isi semua pertanyaan terlebih dahulu.")
