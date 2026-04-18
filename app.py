import streamlit as st
import asyncio
import tempfile
import base64
import os
import random

# ----- Audio setup with edge-tts -----
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

def run_async_with_timeout(coro, timeout=30):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(asyncio.wait_for(coro, timeout=timeout))
    finally:
        loop.close()

async def save_speech(text, file_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

def generate_audio(text, output_path, voice):
    if not EDGE_TTS_AVAILABLE:
        raise Exception("edge-tts not installed")
    run_async_with_timeout(save_speech(text, output_path, voice))

# Consistent voices for each role
VOICES = {
    "doctor": "en-US-GuyNeural",                 # male, always English
    "translator_english": "en-US-AriaNeural",   # female, English (consistent identity)
    "translator_spanish": "es-ES-AlvaroNeural", # male, Spanish (same interpreter, native)
    "patient_english": "en-US-JennyNeural",     # female, English (fallback)
    "patient_spanish": "es-ES-ElviraNeural",    # female, Spanish (native)
    "default": "en-US-JennyNeural"
}

st.set_page_config(page_title="Let's Learn Medical Terminology With Gesner", layout="wide")

# ========== STYLING ==========
def set_medical_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a2f2f, #1a4a4a, #0a2f2f); }
        .main-header { background: linear-gradient(135deg, #00c9a7, #00a8c5, #005f6b); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        .stText { color: white !important; font-size: 1rem; background: transparent !important; }
        .stTabs [role="tab"] { color: white !important; background: rgba(0,200,160,0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: #00c9a7; color: white !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #00c9a7; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #00a8c5; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0a2f2f, #1a4a4a); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #1a4a4a; border: 1px solid #00c9a7; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
        div[data-baseweb="popover"] ul { background-color: #1a4a4a; border: 1px solid #00c9a7; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #1a4a4a; }
        div[data-baseweb="popover"] li:hover { background-color: #00c9a7; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#00c9a7" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00c9a7"/>
                    <stop offset="50%" stop-color="#00a8c5"/>
                    <stop offset="100%" stop-color="#005f6b"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">🩺</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ========== AUTHENTICATION ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_medical_style()
    st.title("🔐 Access Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn Medical Terminology With Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00c9a7;'>20 lessons for medical translators – terms, acronyms, abbreviations & real conversations</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

set_medical_style()
st.markdown("""
<div class="main-header">
    <h1>📘 Let's Learn Medical Terminology With Gesner</h1>
    <p>20 interactive lessons | Medical terms | Acronyms | Abbreviations | Doctor‑Patient‑Translator conversations | Quizzes</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Select a lesson")
    lesson_number = st.selectbox("Lesson", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Your progress")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lesson {lesson_number} of 20 completed")
    st.markdown("---")
    
    st.markdown("## 🧑‍⚕️ For Medical Translators")
    st.markdown("""
    **Citadel Language & Contact Services** is hiring remote contract Medical Interpreters.
    
    We are currently seeking qualified professionals in:
    - Spanish
    - Haitian Creole
    - Portuguese
    - French
    - Polish
    - Mandarin
    - Cantonese
    - Arabic
    - Russian
    - Vietnamese
    
    If you are an experienced interpreter with strong communication skills, professionalism, and a commitment to accuracy and confidentiality, we would love to hear from you.
    
    **To apply:** Send your resume to **Join@GoCLCS.com**  
    🌐 [www.GoCLCS.com](https://www.GoCLCS.com)
    
    *Know someone who may be a fit? Tag them or share this post.*
    """)
    st.markdown("---")
    
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$299 USD** (full book – 20 lessons, source code, certificate)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ========== GENERATE ALL 20 LESSONS DYNAMICALLY ==========
# List of patient languages (one per lesson)
patient_languages = [
    "Spanish", "Haitian Creole", "Portuguese", "French", "Polish",
    "Mandarin", "Cantonese", "Arabic", "Russian", "Vietnamese",
    "German", "Italian", "Japanese", "Korean", "Turkish",
    "Hindi", "Bengali", "Urdu", "Swahili", "Dutch"
]

# Medical themes for each lesson
themes = [
    "General Medical Examination", "Cardiology", "Pulmonology", "Gastroenterology", "Neurology",
    "Orthopedics", "Pediatrics", "Obstetrics & Gynecology", "Urology", "Ophthalmology",
    "Dermatology", "Endocrinology", "Hematology", "Oncology", "Infectious Diseases",
    "Emergency Medicine", "Pharmacology", "Radiology", "Psychiatry", "Medical Acronyms & Abbreviations Review"
]

# Predefined medical terms, acronyms, abbreviations (reused across lessons with slight variation)
base_terms = [
    "Symptom", "Diagnosis", "Treatment", "Prescription", "Physical exam",
    "Vital signs", "Blood pressure", "Heart rate", "Temperature", "Medical history",
    "Allergy", "Injection", "Wound", "Fever", "Infection", "Heart", "Artery", "Vein",
    "Chest pain", "Palpitations", "Hypertension", "Cholesterol", "Stent", "Angina",
    "Myocardial infarction", "Lungs", "Cough", "Shortness of breath", "Asthma",
    "COPD", "Pneumonia", "Stomach", "Nausea", "Vomiting", "Diarrhea", "Constipation",
    "Brain", "Headache", "Seizure", "Stroke", "Bone", "Fracture", "Arthritis",
    "Pregnancy", "Fetus", "Kidney", "Bladder", "UTI", "Diabetes", "Anemia", "Cancer"
]

base_acronyms = [
    "PCP (Primary Care Physician)", "EHR (Electronic Health Record)", "BMI (Body Mass Index)",
    "CBC (Complete Blood Count)", "BP (Blood Pressure)", "ECG/EKG (Electrocardiogram)",
    "CAD (Coronary Artery Disease)", "CHF (Congestive Heart Failure)", "MI (Myocardial Infarction)",
    "HTN (Hypertension)", "COPD (Chronic Obstructive Pulmonary Disease)", "PE (Pulmonary Embolism)",
    "ARDS (Acute Respiratory Distress Syndrome)", "TB (Tuberculosis)", "GERD (Gastroesophageal Reflux Disease)",
    "IBS (Irritable Bowel Syndrome)", "CNS (Central Nervous System)", "TIA (Transient Ischemic Attack)",
    "ACL (Anterior Cruciate Ligament)", "OA (Osteoarthritis)", "NICU (Neonatal Intensive Care Unit)",
    "UTI (Urinary Tract Infection)", "DM (Diabetes Mellitus)", "HIV (Human Immunodeficiency Virus)",
    "ER (Emergency Room)", "ICU (Intensive Care Unit)", "CPR (Cardiopulmonary Resuscitation)",
    "OTC (Over-the-Counter)", "NSAID (Non-Steroidal Anti-Inflammatory Drug)", "CT (Computed Tomography)",
    "MRI (Magnetic Resonance Imaging)", "PTSD (Post-Traumatic Stress Disorder)", "ADHD (Attention Deficit Hyperactivity Disorder)"
]

base_abbreviations = [
    "Rx (prescription)", "Hx (history)", "Dx (diagnosis)", "Tx (treatment)", "q.d. (every day)",
    "ACS (Acute Coronary Syndrome)", "SOB (shortness of breath)", "O2 (oxygen)", "PFT (pulmonary function test)",
    "GI (gastrointestinal)", "PO (by mouth)", "NPO (nothing by mouth)", "LOC (loss of consciousness)",
    "Fx (fracture)", "PT (physical therapy)", "PR (per rectum)", "IM (intramuscular)", "gtt (drops)",
    "UA (urinalysis)", "Cr (creatinine)", "OD (right eye)", "OS (left eye)", "BID (twice a day)",
    "BG (blood glucose)", "FBS (fasting blood sugar)", "Ca (cancer)", "STAT (immediately)",
    "ABC (airway, breathing, circulation)", "IV (intravenous)", "mg (milligram)", "prn (as needed)"
]

def build_lesson(num):
    lang = patient_languages[num-1]
    theme = themes[num-1]
    # Select a subset of terms, acronyms, abbreviations (15 terms, 5 acronyms, 5 abbreviations)
    terms = base_terms[(num*3) % len(base_terms):][:15] + base_terms[:max(0, 15 - ((num*3) % len(base_terms)))]
    acronyms = base_acronyms[(num*2) % len(base_acronyms):][:5] + base_acronyms[:max(0, 5 - ((num*2) % len(base_acronyms)))]
    abbreviations = base_abbreviations[(num*4) % len(base_abbreviations):][:5] + base_abbreviations[:max(0, 5 - ((num*4) % len(base_abbreviations)))]
    
    # Build conversation template (same logical structure, but with realistic medical content)
    # For Spanish we have native voices; for others we use fallback (but you can extend)
    # We'll create a simple generic conversation that uses the theme and some terms.
    doctor_lines = [
        f"Good morning, Mrs. Johnson. What brings you in today? I'd like to ask about {terms[0]} and {terms[1]}.",
        f"Let me check your vital signs. Your blood pressure is slightly elevated. Have you experienced {terms[2]}?",
        f"I suspect you might have a condition related to {acronyms[0].split('(')[0]}. We should run a {abbreviations[0]}.",
        f"I will prescribe medication. Please follow the treatment plan. If you feel {terms[3]}, come back immediately.",
        f"Any questions about the {acronyms[1]} or the prescription?"
    ]
    patient_responses_en = [
        f"I've had {terms[0]} and {terms[1]} for three days.",
        f"Yes, I also feel {terms[2]} and sometimes {terms[3]}.",
        f"Is it serious? What does {acronyms[0]} mean?",
        f"Thank you, doctor. I will take the medication as prescribed.",
        f"No, I understand. Thank you for explaining the {acronyms[1]}."
    ]
    # For non-Spanish languages, we still show the English translation of patient responses.
    # The actual patient speech in their native language is simulated with placeholder text.
    # To keep the code clean, we just use the English text but mark it as the native language.
    # For a real deployment, you would add actual translations.
    conversation = []
    for i in range(min(len(doctor_lines), len(patient_responses_en))):
        # Doctor line (English)
        conversation.append(("D", doctor_lines[i]))
        # Translator interprets doctor's line to patient's language
        conversation.append(("T", f"(Interprets to {lang}) {doctor_lines[i]}"))
        # Patient responds in their language (we show the English translation but mark as native)
        conversation.append(("P", f"(in {lang}) {patient_responses_en[i]}"))
        # Translator interprets patient's response back to doctor
        conversation.append(("T", f"(Interprets to English) {patient_responses_en[i]}"))
    
    return {
        "theme": theme,
        "patient_language": lang,
        "terms": terms[:15],
        "acronyms": acronyms[:5],
        "abbreviations": abbreviations[:5],
        "conversation": conversation
    }

lessons_data = {i: build_lesson(i) for i in range(1, 21)}

# ========== AUDIO FUNCTION ==========
def play_audio(text, key, voice=VOICES["default"]):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled. Please install edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                generate_audio(text, tmp.name, voice)
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Audio error: {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ========== DISPLAY LESSON ==========
lesson = lessons_data[lesson_number]
st.markdown(f"## 📖 Lesson {lesson_number}: {lesson['theme']}")
st.markdown(f"**🌐 Patient's language today:** {lesson['patient_language']}")

tab1, tab2, tab3, tab4 = st.tabs(["📚 Terminology", "🗣️ Conversation", "❓ Quiz", "📝 Notes"])

# ----- TAB 1: TERMINOLOGY -----
with tab1:
    st.subheader("🏥 Medical Terms")
    cols = st.columns(3)
    for idx, term in enumerate(lesson["terms"]):
        with cols[idx % 3]:
            st.markdown(f"**{term}**")
            play_audio(term, f"term_{lesson_number}_{idx}", VOICES["default"])
    
    st.markdown("---")
    st.subheader("🔤 Acronyms")
    for idx, acro in enumerate(lesson["acronyms"]):
        st.markdown(f"• {acro}")
        play_audio(acro, f"acro_{lesson_number}_{idx}", VOICES["default"])
    
    st.markdown("---")
    st.subheader("✍️ Abbreviations")
    for idx, abbr in enumerate(lesson["abbreviations"]):
        st.markdown(f"• {abbr}")
        play_audio(abbr, f"abbr_{lesson_number}_{idx}", VOICES["default"])

# ----- TAB 2: CONVERSATION with consistent role voices -----
with tab2:
    st.markdown("### 👨‍⚕️ Doctor – Patient – Medical Translator (over the phone)")
    st.caption("The interpreter translates between English and the patient's language. Listen and practice.")
    for idx, (speaker, line) in enumerate(lesson["conversation"]):
        if speaker == "D":
            st.markdown(f"**👨‍⚕️ Doctor (English):** {line}")
            play_audio(line, f"conv_{lesson_number}_{idx}_D", VOICES["doctor"])
        elif speaker == "T":
            # Determine if this line is interpreting to patient's language or to English
            if "Interprets to English" in line:
                st.markdown(f"**📞 Translator (to English):** {line}")
                play_audio(line, f"conv_{lesson_number}_{idx}_T", VOICES["translator_english"])
            else:
                # Interpreting to patient's language
                if lesson['patient_language'] == "Spanish":
                    st.markdown(f"**📞 Translator (to Spanish):** {line}")
                    play_audio(line, f"conv_{lesson_number}_{idx}_T", VOICES["translator_spanish"])
                else:
                    # For other languages, use English voice as fallback
                    st.markdown(f"**📞 Translator (to {lesson['patient_language']}):** {line}")
                    play_audio(line, f"conv_{lesson_number}_{idx}_T", VOICES["translator_english"])
        elif speaker == "P":
            # Patient speaking in their language
            if lesson['patient_language'] == "Spanish":
                st.markdown(f"**🧑‍🦱 Patient (in Spanish):** {line}")
                play_audio(line, f"conv_{lesson_number}_{idx}_P", VOICES["patient_spanish"])
            else:
                st.markdown(f"**🧑‍🦱 Patient (in {lesson['patient_language']}):** {line}")
                play_audio(line, f"conv_{lesson_number}_{idx}_P", VOICES["patient_english"])
        st.markdown("---")

# ----- TAB 3: QUIZ (unchanged) -----
with tab3:
    st.markdown("Test your knowledge of this lesson's terminology and acronyms.")
    quiz_questions = []
    sample_terms = random.sample(lesson["terms"], min(3, len(lesson["terms"])))
    for term in sample_terms:
        quiz_questions.append({
            "question": f"What does the medical term '{term}' refer to?",
            "options": ["A type of medication", "A medical condition or body part", "A surgical instrument", "A hospital department"],
            "answer": "A medical condition or body part"
        })
    sample_acros = random.sample(lesson["acronyms"], min(2, len(lesson["acronyms"])))
    for acro in sample_acros:
        if "(" in acro:
            parts = acro.split(" (")
            acronym = parts[0]
            full = parts[1].rstrip(")")
        else:
            acronym = acro
            full = acro
        quiz_questions.append({
            "question": f"What does the acronym '{acronym}' stand for?",
            "options": [full, "A medical test", "A type of drug", "A hospital unit"],
            "answer": full
        })
    
    if not quiz_questions:
        quiz_questions = [{"question": "What is the main focus of this lesson?", "options": ["Cardiology", "Terminology", "Surgery", "Pediatrics"], "answer": "Terminology"}]
    
    score = 0
    user_answers = {}
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        play_audio(q['question'], f"quiz_q_{lesson_number}_{i}", VOICES["default"])
        answer = st.radio("Select your answer:", q['options'], key=f"quiz_{lesson_number}_{i}", index=None)
        if answer:
            user_answers[i] = answer
        st.markdown("---")
    
    if st.button("Check answers", key=f"check_{lesson_number}"):
        for i, q in enumerate(quiz_questions):
            if user_answers.get(i) == q["answer"]:
                score += 1
        st.success(f"You got {score} out of {len(quiz_questions)} correct!")
        if score == len(quiz_questions):
            st.balloons()
            st.markdown("🎉 Perfect! You have mastered this lesson.")
        else:
            with st.expander("Show correct answers"):
                for i, q in enumerate(quiz_questions):
                    st.write(f"{i+1}. {q['question']} → Correct answer: {q['answer']}")
                    play_audio(f"Correct answer: {q['answer']}", f"correct_{lesson_number}_{i}", VOICES["default"])

# ----- TAB 4: NOTES -----
with tab4:
    st.markdown("### 📝 Study Notes")
    st.markdown(f"""
    - **Theme:** {lesson['theme']}
    - **Patient language:** {lesson['patient_language']}
    - **Key terms:** {', '.join(lesson['terms'][:5])} ...
    - **Acronyms to remember:** {', '.join([a.split('(')[0] for a in lesson['acronyms'][:3]])}
    - **Common abbreviations:** {', '.join(lesson['abbreviations'][:3])}
    - **Role of the translator:** Interpret accurately, maintain neutrality, clarify when needed. Always ask for repetition if you miss something.
    """)

# ========== END OF BOOK ==========
if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Congratulations! You have completed the Medical Terminology Book.")
    st.markdown("""
    ### 📞 To continue with advanced medical interpreting courses, contact us:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Keep practicing with real scenarios and expand your medical vocabulary.
    """)
