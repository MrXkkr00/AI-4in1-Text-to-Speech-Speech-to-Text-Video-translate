import streamlit as st
# import tempfile, os
# # from transformers import pipeline
import whisper
# from moviepy.editor import VideoFileClip, AudioFileClip
# from transliterate import to_cyrillic, to_latin
# import torch
# import soundfile as sf
# from transformers import VitsModel, AutoTokenizer

import warnings
from transformers.utils import logging


# Transformers loglarini o'chirish
logging.set_verbosity_error()

# PyTorch va umumiy ogohlantirishlarni o'chirish
warnings.filterwarnings("ignore")

from pydub import AudioSegment

# ---------- Models ----------
# TTS_MODEL = "facebook/mms-tts-uzb-script_cyrillic"
# STT_MODEL = "small"   # whisper model (tiny, base, small, medium, large)

# MODEL_ID = "facebook/mms-tts-uzb-script_cyrillic"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
# model = VitsModel.from_pretrained(MODEL_ID)





# def text_to_speech(text, out_path="text2speech.wav"):
#     """Matndan audio yaratish"""
#     inputs = tokenizer(text, return_tensors="pt")

#     with torch.no_grad():
#         audio = model(**inputs).waveform.squeeze(0).cpu().numpy()
#     sf.write(out_path, audio, model.config.sampling_rate)
#     return out_path


# def text_to_speech2(text, out_path="text2speech.wav"):
#     if not text.strip():  # bo'sh bo'lsa
#         raise ValueError("Matn bo'sh, TTS bajarilmadi")

#     inputs = tokenizer(text, return_tensors="pt")
#     input_ids = inputs["input_ids"].long()

#     with torch.no_grad():
#         audio = model(input_ids=input_ids).waveform.squeeze(0).cpu().numpy()

#     sf.write(out_path, audio, model.config.sampling_rate)
#     return out_path



# --- 1) Yangilangan text_to_speech funksiyasi ---





# TTS pipeline
# tts = pipeline("text-to-speech", model=TTS_MODEL)

# Whisper STT (uzbek uchun)
# whisper_model = whisper.load_model(STT_MODEL)

# ---------- Streamlit UI ----------


# 1. BIRINCHI qatorlarda, hech qanday st.* chaqirilmasdan
st.set_page_config(page_title="Tarjima platformasi", layout="wide")

# 2. Endi tepadagi muallif nomi
st.markdown(
    "<h5 style='text-align:left; color:gray;'>Rasulbek Qodomboyev tomonidan yaratilgan</h5>",
    unsafe_allow_html=True
)

# 3. Asosiy sarlavha
st.markdown("<h1 style='text-align:center'>🌐 Tarjima va Ovoz Platformasi</h1>", unsafe_allow_html=True)


# --- Custom CSS bilan tabs balandligini oshirish ---
st.markdown(
    """
    <style>
    /* Tab buttonlarini kattalashtirish */
    .stTabs [role="tab"] {
        min-height: 60px;      /* Balandlik */
        font-size: 14px;       /* Matn kattaligi */
        padding: 5px 1px;    /* Ichki bo'sh joy */
    }
    </style>
    """,
    unsafe_allow_html=True
)


tabs = st.tabs([
    "🔊 Textni ovozga aylantirish",
    "🎬 Video tarjimon Uzbek tiliga",
    "📝 Ovozni text qilib berish",
    "🔄 Kiril ↔ Lotin transliteratsiya"
])

# -------------------- 2. TEXT -> VOICE --------------------


# with tabs[0]:
#     st.header("🔊 Textni ovozga aylantirish")

#     script_type = st.radio("Matn yozuv turini tanlang:", ["Lotin","Кирилча"], horizontal=True)

#     user_text = st.text_area("Matnni kiriting :")

#     if st.button("🎙️ Ovoz yaratish"):
#         if user_text.strip():

#             if script_type == "Lotin":
#                 print(user_text)
#                 try:
#                     from transliterate import to_cyrillic
#                     text_for_tts = to_cyrillic(user_text)
#                 except:
#                     st.error("❌ Lotindan Kirilga o'tkazish uchun transliteratsiya kutubxonasi kerak!")
#                     text_for_tts = user_text
#             else:
#                 text_for_tts = user_text


#             print(text_for_tts)
#             out_wav = text_to_speech(text_for_tts, "text2speech.wav")

#             # Ovoz eshittirish
#             st.audio(out_wav)

#             # Yuklab olish tugmasi
#             with open(out_wav, "rb") as f:
#                 st.download_button("⬇️ Ovoz faylini yuklab olish", f, file_name="uzbek_tts.wav")
#         else:
#             st.warning("Matn kiritilmadi!")



# -------------------- 1. VIDEO TARJIMON --------------------
# with tabs[1]:
#     st.header("🎬 Video tarjimon Uzbek tiliga")

#     lang = st.radio("Tilni tanlang:", ["Rus", "English"], horizontal=True)

#     uploaded_video = st.file_uploader("Videoni yuklang", type=["mp4", "mov", "avi"])
#     if uploaded_video:
#         st.video(uploaded_video)

#         if st.button("✅ Tarjima qilish"):
#             with st.spinner("Videoni qayta ishlash..."):

#                 # 1. Save temp video
#                 temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#                 temp_video.write(uploaded_video.read())

#                 # 2. Extract audio
#                 video_clip = VideoFileClip(temp_video.name)
#                 audio_path = temp_video.name.replace(".mp4", ".wav")
#                 video_clip.audio.write_audiofile(audio_path)

#                 # 3. STT (Speech to text) - Whisper
#                 result = whisper_model.transcribe(audio_path, language="ru" if lang=="Rus" else "en")
#                 text = result["text"]

#                 # 4. Translate text -> Uzbek
#                 from deep_translator import GoogleTranslator
#                 translated = GoogleTranslator(source="auto", target="uz").translate(text)
#                 translated = to_cyrillic(translated)
#                 print(translated)

#                 # 5. TTS (Uzbek) - facebook/mms-tts-uzb-script_cyrillic
#                 out_wav = temp_video.name.replace(".mp4", "_uz.wav")
#                 out_wav = text_to_speech2(translated, out_wav)

#                 # Ovoz eshittirish
#                 st.audio(out_wav)

#                 # Ovoz faylini yuklab olish tugmasi
#                 with open(out_wav, "rb") as f:
#                     st.download_button("⬇️ Ovoz faylini yuklab olish", f, file_name="uzbek_tts.wav")

#                 # 6. Replace audio in video
#                 audio_clip = AudioFileClip(out_wav)
#                 final_video = temp_video.name.replace(".mp4", "_uzbek.mp4")
#                 new_video = video_clip.set_audio(audio_clip)
#                 new_video.write_videofile(final_video)

#                 st.success("✅ Tarjima tugadi!")
#                 st.video(final_video)
#                 with open(final_video, "rb") as f:
#                     st.download_button("⬇️ Uzbekcha videoni yuklab olish", f, file_name="video_uzbek.mp4")
# # 
# -------------------- 3. VOICE -> TEXT --------------------
# with tabs[2]:
#     st.header("📝 Ovozni text qilib berish")

#     uploaded_audio = st.file_uploader("Audio yuklang (uzbek)", type=["wav", "mp3", "m4a"])
#     if uploaded_audio:
#         if st.button("📜 Textga o'tkazish"):
#             temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#             temp_audio.write(uploaded_audio.read())
#             result = whisper_model.transcribe(temp_audio.name, language="uz")
#             st.success("✅ Audio matnga o'tkazildi!")
#             st.text_area("Natija:", result["text"], height=200)

# -------------------- 4. KRIL ↔ LOTIN --------------------
with tabs[3]:
    st.header("🔄 Kiril ↔ Lotin transliteratsiya")

    translit_type = st.radio("Yo'nalishni tanlang:", [ "Lotin → Кирил", "Кирил → Lotin"], horizontal=True)

    user_text_translit = st.text_area("Matnni kiriting:")

    if st.button("📝 O'zgartirish"):
        if user_text_translit.strip():
            try:
                if translit_type == "Кирил → Lotin":
                    from transliterate import to_latin
                    result_text = to_latin(user_text_translit)
                else:
                    from transliterate import to_cyrillic
                    result_text = to_cyrillic(user_text_translit)

                st.success("✅ Matn transliteratsiya qilindi!")
                st.text_area("Natija:", result_text, height=200)

                # Yuklab olish tugmasi
                with open("transliterated.txt", "w", encoding="utf-8") as f:
                    f.write(result_text)
                with open("transliterated.txt", "rb") as f:
                    st.download_button("⬇️ Matnni yuklab olish", f, file_name="transliterated.txt")
            except Exception as e:
                st.error(f"❌ Xato: {e}")
        else:

            st.warning("Matn kiritilmadi!")


