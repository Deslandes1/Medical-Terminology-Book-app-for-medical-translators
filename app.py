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

# Helper to run async function synchronously with timeout
def run_async_with_timeout(coro, timeout=30):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(asyncio.wait_for(coro, timeout=timeout))
    finally:
        loop.close()

async def save_speech(text, file_path):
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    await communicate.save(file_path)

def generate_audio(text, output_path):
    if not EDGE_TTS_AVAILABLE:
        raise Exception("edge-tts not installed")
    run_async_with_timeout(save_speech(text, output_path))

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

# ========== FULL LESSONS DATA (1 to 20) ==========
lessons_data = {
    1: {
        "theme": "General Medical Examination",
        "terms": ["Symptom", "Diagnosis", "Treatment", "Prescription", "Physical exam", "Vital signs", "Blood pressure", "Heart rate", "Temperature", "Medical history", "Allergy", "Injection", "Wound", "Fever", "Infection"],
        "acronyms": ["PCP (Primary Care Physician)", "EHR (Electronic Health Record)", "BMI (Body Mass Index)", "CBC (Complete Blood Count)", "BP (Blood Pressure)"],
        "abbreviations": ["Rx (prescription)", "Hx (history)", "Dx (diagnosis)", "Tx (treatment)", "q.d. (every day)"],
        "conversation": [
            ("D", "Good morning, Mr. Johnson. What brings you in today?"),
            ("P", "Doctor, I've been having headaches and a low fever for three days."),
            ("T", "(on phone) Doctor says: Good morning, Mr. Johnson. What brings you in today? Patient says: Doctor, I've been having headaches and a low fever for three days."),
            ("D", "Let me check your vital signs. Your blood pressure is slightly elevated. Any other symptoms?"),
            ("P", "Yes, I feel very tired and my throat hurts."),
            ("T", "(on phone) Doctor: Let me check your vital signs. Your blood pressure is slightly elevated. Any other symptoms? Patient: Yes, I feel very tired and my throat hurts."),
            ("D", "I'll prescribe an antibiotic and some rest. Come back if the fever persists."),
            ("P", "Thank you, doctor. I will follow your advice."),
            ("T", "(on phone) Doctor: I'll prescribe an antibiotic and some rest. Come back if the fever persists. Patient: Thank you, doctor. I will follow your advice.")
        ]
    },
    2: {
        "theme": "Cardiology",
        "terms": ["Heart", "Artery", "Vein", "Chest pain", "Palpitations", "Hypertension", "Cholesterol", "Stent", "Angina", "Myocardial infarction", "Echocardiogram", "Electrocardiogram", "Cardiologist", "Heart failure", "Blood clot"],
        "acronyms": ["ECG/EKG (Electrocardiogram)", "CAD (Coronary Artery Disease)", "CHF (Congestive Heart Failure)", "MI (Myocardial Infarction)", "HTN (Hypertension)"],
        "abbreviations": ["ACS (Acute Coronary Syndrome)", "CVD (Cardiovascular Disease)", "LV (Left Ventricle)", "RV (Right Ventricle)", "CCU (Cardiac Care Unit)"],
        "conversation": [
            ("D", "Your ECG shows some irregularities. Have you ever had chest pain?"),
            ("P", "Yes, when I walk fast, I feel pressure in my chest."),
            ("T", "(on phone) Doctor: Your ECG shows some irregularities. Have you ever had chest pain? Patient: Yes, when I walk fast, I feel pressure in my chest."),
            ("D", "That could be angina. I want you to have a stress test and an echocardiogram."),
            ("P", "Is it serious, doctor?"),
            ("T", "(on phone) Doctor: That could be angina. I want you to have a stress test and an echocardiogram. Patient: Is it serious, doctor?"),
            ("D", "We need to rule out coronary artery disease. Meanwhile, take this medication and avoid heavy exercise."),
            ("P", "I understand. I'll do as you say."),
            ("T", "(on phone) Doctor: We need to rule out coronary artery disease. Meanwhile, take this medication and avoid heavy exercise. Patient: I understand. I'll do as you say.")
        ]
    },
    3: {
        "theme": "Pulmonology",
        "terms": ["Lungs", "Bronchi", "Alveoli", "Cough", "Shortness of breath", "Asthma", "COPD", "Pneumonia", "Pulmonary embolism", "Sputum", "Chest X-ray", "Spirometry", "Oxygen saturation", "Wheezing", "Pleural effusion"],
        "acronyms": ["COPD (Chronic Obstructive Pulmonary Disease)", "PE (Pulmonary Embolism)", "ARDS (Acute Respiratory Distress Syndrome)", "TB (Tuberculosis)", "OSA (Obstructive Sleep Apnea)"],
        "abbreviations": ["SOB (shortness of breath)", "O2 (oxygen)", "PFT (pulmonary function test)", "ABG (arterial blood gas)", "RR (respiratory rate)"],
        "conversation": [
            ("D", "You've been coughing for three weeks. Any shortness of breath?"),
            ("P", "Yes, especially when I climb stairs. I also wheeze at night."),
            ("T", "(on phone) Doctor: You've been coughing for three weeks. Any shortness of breath? Patient: Yes, especially when I climb stairs. I also wheeze at night."),
            ("D", "I suspect asthma or COPD. We'll do a spirometry test today."),
            ("P", "What does that involve?"),
            ("T", "(on phone) Doctor: I suspect asthma or COPD. We'll do a spirometry test today. Patient: What does that involve?"),
            ("D", "You'll blow into a machine to measure your lung function. It's simple and painless."),
            ("P", "Okay, I'll do it. Thank you, doctor."),
            ("T", "(on phone) Doctor: You'll blow into a machine to measure your lung function. It's simple and painless. Patient: Okay, I'll do it. Thank you, doctor.")
        ]
    },
    4: {
        "theme": "Gastroenterology",
        "terms": ["Stomach", "Intestines", "Liver", "Pancreas", "Gallbladder", "Nausea", "Vomiting", "Diarrhea", "Constipation", "Abdominal pain", "Acid reflux", "Ulcer", "Colonoscopy", "Endoscopy", "Hepatitis"],
        "acronyms": ["GERD (Gastroesophageal Reflux Disease)", "IBS (Irritable Bowel Syndrome)", "IBD (Inflammatory Bowel Disease)", "UGI (Upper Gastrointestinal)", "NG (Nasogastric)"],
        "abbreviations": ["GI (gastrointestinal)", "PO (by mouth)", "NPO (nothing by mouth)", "BM (bowel movement)", "EUS (endoscopic ultrasound)"],
        "conversation": [
            ("D", "Where is the pain? Can you point to it?"),
            ("P", "It's in my upper belly, especially after eating. Sometimes I feel bloated."),
            ("T", "(on phone) Doctor: Where is the pain? Can you point to it? Patient: It's in my upper belly, especially after eating. Sometimes I feel bloated."),
            ("D", "It could be gastritis or an ulcer. Have you taken any medication?"),
            ("P", "I tried antacids, but they only help a little."),
            ("T", "(on phone) Doctor: It could be gastritis or an ulcer. Have you taken any medication? Patient: I tried antacids, but they only help a little."),
            ("D", "I recommend an upper endoscopy to see inside your stomach. Meanwhile, avoid spicy food and alcohol."),
            ("P", "I understand. I'll schedule the procedure."),
            ("T", "(on phone) Doctor: I recommend an upper endoscopy to see inside your stomach. Meanwhile, avoid spicy food and alcohol. Patient: I understand. I'll schedule the procedure.")
        ]
    },
    5: {
        "theme": "Neurology",
        "terms": ["Brain", "Spinal cord", "Nerves", "Headache", "Dizziness", "Seizure", "Stroke", "Multiple sclerosis", "Parkinson's disease", "Neuropathy", "CT scan", "MRI", "Lumbar puncture", "Reflexes", "Tremor"],
        "acronyms": ["CNS (Central Nervous System)", "PNS (Peripheral Nervous System)", "TIA (Transient Ischemic Attack)", "ALS (Amyotrophic Lateral Sclerosis)", "EEG (Electroencephalogram)"],
        "abbreviations": ["LOC (loss of consciousness)", "GCS (Glasgow Coma Scale)", "ICP (intracranial pressure)", "CSF (cerebrospinal fluid)", "MS (multiple sclerosis)"],
        "conversation": [
            ("D", "You mentioned numbness in your left hand. When did it start?"),
            ("P", "About a week ago. Now my fingers feel tingly too."),
            ("T", "(on phone) Doctor: You mentioned numbness in your left hand. When did it start? Patient: About a week ago. Now my fingers feel tingly too."),
            ("D", "I need to check your reflexes and order an MRI to rule out multiple sclerosis or a pinched nerve."),
            ("P", "Is it very serious?"),
            ("T", "(on phone) Doctor: I need to check your reflexes and order an MRI to rule out multiple sclerosis or a pinched nerve. Patient: Is it very serious?"),
            ("D", "Not necessarily, but we must diagnose it early. The MRI is painless and gives us clear images."),
            ("P", "Alright, I'll do it. Thank you."),
            ("T", "(on phone) Doctor: Not necessarily, but we must diagnose it early. The MRI is painless and gives us clear images. Patient: Alright, I'll do it. Thank you.")
        ]
    },
    6: {
        "theme": "Orthopedics",
        "terms": ["Bone", "Joint", "Muscle", "Ligament", "Tendon", "Fracture", "Sprain", "Dislocation", "Arthritis", "Osteoporosis", "X-ray", "Cast", "Physical therapy", "Range of motion", "Swelling"],
        "acronyms": ["ACL (Anterior Cruciate Ligament)", "PCL (Posterior Cruciate Ligament)", "OA (Osteoarthritis)", "RA (Rheumatoid Arthritis)", "ROM (Range of Motion)"],
        "abbreviations": ["Fx (fracture)", "ORIF (open reduction internal fixation)", "PT (physical therapy)", "NWB (non-weight bearing)", "WBAT (weight bearing as tolerated)"],
        "conversation": [
            ("D", "How did you injure your knee?"),
            ("P", "I was playing soccer and twisted it. Now it hurts to walk."),
            ("T", "(on phone) Doctor: How did you injure your knee? Patient: I was playing soccer and twisted it. Now it hurts to walk."),
            ("D", "Let me examine. I think you may have torn your ACL. We'll need an MRI."),
            ("P", "Will I need surgery?"),
            ("T", "(on phone) Doctor: Let me examine. I think you may have torn your ACL. We'll need an MRI. Patient: Will I need surgery?"),
            ("D", "Possibly, but first let's confirm the diagnosis. Meanwhile, rest, ice, and elevate your leg."),
            ("P", "I'll follow your advice. Thank you."),
            ("T", "(on phone) Doctor: Possibly, but first let's confirm the diagnosis. Meanwhile, rest, ice, and elevate your leg. Patient: I'll follow your advice. Thank you.")
        ]
    },
    7: {
        "theme": "Pediatrics",
        "terms": ["Infant", "Child", "Vaccination", "Growth chart", "Developmental milestones", "Fever", "Rash", "Ear infection", "Asthma", "ADHD", "Immunization", "Pediatrician", "Breastfeeding", "Colic", "Chickenpox"],
        "acronyms": ["AAP (American Academy of Pediatrics)", "NICU (Neonatal Intensive Care Unit)", "PICU (Pediatric Intensive Care Unit)", "RSV (Respiratory Syncytial Virus)", "VUR (Vesicoureteral Reflux)"],
        "abbreviations": ["PO (by mouth)", "PR (per rectum)", "IM (intramuscular)", "SC (subcutaneous)", "gtt (drops)"],
        "conversation": [
            ("D", "How long has your daughter had a fever?"),
            ("P", "Two days. She also has a runny nose and cough."),
            ("T", "(on phone) Doctor: How long has your daughter had a fever? Patient: Two days. She also has a runny nose and cough."),
            ("D", "Let me check her ears and throat. It looks like a viral infection. Give her plenty of fluids and acetaminophen for fever."),
            ("P", "When should I bring her back?"),
            ("T", "(on phone) Doctor: Let me check her ears and throat. It looks like a viral infection. Give her plenty of fluids and acetaminophen for fever. Patient: When should I bring her back?"),
            ("D", "If the fever lasts more than five days or she becomes lethargic, come back immediately."),
            ("P", "Thank you, doctor. I'll monitor her closely."),
            ("T", "(on phone) Doctor: If the fever lasts more than five days or she becomes lethargic, come back immediately. Patient: Thank you, doctor. I'll monitor her closely.")
        ]
    },
    8: {
        "theme": "Obstetrics & Gynecology",
        "terms": ["Pregnancy", "Fetus", "Uterus", "Ovary", "Cervix", "Menstruation", "Contraception", "Prenatal care", "Ultrasound", "Amniocentesis", "Cesarean section", "Labor", "Delivery", "Mammogram", "Pap smear"],
        "acronyms": ["OB (Obstetrics)", "GYN (Gynecology)", "PID (Pelvic Inflammatory Disease)", "PCOS (Polycystic Ovary Syndrome)", "IUGR (Intrauterine Growth Restriction)"],
        "abbreviations": ["G (gravida)", "P (para)", "LMP (last menstrual period)", "EDD (estimated due date)", "C/S (cesarean section)"],
        "conversation": [
            ("D", "Congratulations on your pregnancy. Have you had any bleeding or pain?"),
            ("P", "No, but I feel very tired and nauseous."),
            ("T", "(on phone) Doctor: Congratulations on your pregnancy. Have you had any bleeding or pain? Patient: No, but I feel very tired and nauseous."),
            ("D", "That's normal in the first trimester. Let's schedule your first ultrasound to check the baby's heartbeat."),
            ("P", "When will I feel the baby move?"),
            ("T", "(on phone) Doctor: That's normal in the first trimester. Let's schedule your first ultrasound to check the baby's heartbeat. Patient: When will I feel the baby move?"),
            ("D", "Usually between 18 and 22 weeks. Meanwhile, take prenatal vitamins and avoid alcohol."),
            ("P", "I will. Thank you, doctor."),
            ("T", "(on phone) Doctor: Usually between 18 and 22 weeks. Meanwhile, take prenatal vitamins and avoid alcohol. Patient: I will. Thank you, doctor.")
        ]
    },
    9: {
        "theme": "Urology",
        "terms": ["Kidney", "Bladder", "Ureter", "Urethra", "Urine", "Urinary tract infection", "Kidney stone", "Incontinence", "Prostate", "Hematuria", "Cystoscopy", "Nephrectomy", "Dialysis", "Catheter", "UTI"],
        "acronyms": ["UTI (Urinary Tract Infection)", "BPH (Benign Prostatic Hyperplasia)", "ESRD (End Stage Renal Disease)", "PKD (Polycystic Kidney Disease)", "TURP (Transurethral Resection of Prostate)"],
        "abbreviations": ["UA (urinalysis)", "Cr (creatinine)", "BUN (blood urea nitrogen)", "IVP (intravenous pyelogram)", "VCUG (voiding cystourethrogram)"],
        "conversation": [
            ("D", "You said it burns when you urinate. How long has this been happening?"),
            ("P", "About three days. I also feel the urge to go frequently."),
            ("T", "(on phone) Doctor: You said it burns when you urinate. How long has this been happening? Patient: About three days. I also feel the urge to go frequently."),
            ("D", "It sounds like a urinary tract infection. I'll order a urinalysis and prescribe antibiotics."),
            ("P", "Can I get a kidney stone from this?"),
            ("T", "(on phone) Doctor: It sounds like a urinary tract infection. I'll order a urinalysis and prescribe antibiotics. Patient: Can I get a kidney stone from this?"),
            ("D", "Not directly, but we'll check your urine for crystals. Drink plenty of water."),
            ("P", "I will. Thank you, doctor."),
            ("T", "(on phone) Doctor: Not directly, but we'll check your urine for crystals. Drink plenty of water. Patient: I will. Thank you, doctor.")
        ]
    },
    10: {
        "theme": "Ophthalmology",
        "terms": ["Eye", "Cornea", "Retina", "Lens", "Iris", "Vision", "Glaucoma", "Cataract", "Macular degeneration", "Conjunctivitis", "Refraction", "Visual acuity", "Ophthalmoscope", "Eye drop", "Laser surgery"],
        "acronyms": ["AMD (Age-related Macular Degeneration)", "IOP (Intraocular Pressure)", "OCT (Optical Coherence Tomography)", "PRK (Photorefractive Keratectomy)", "LASIK (Laser-Assisted In Situ Keratomileusis)"],
        "abbreviations": ["OD (right eye)", "OS (left eye)", "OU (both eyes)", "VA (visual acuity)", "VF (visual field)"],
        "conversation": [
            ("D", "You mentioned blurry vision. Is it near or far?"),
            ("P", "Both, but especially when reading. I also see floaters."),
            ("T", "(on phone) Doctor: You mentioned blurry vision. Is it near or far? Patient: Both, but especially when reading. I also see floaters."),
            ("D", "I'll check your intraocular pressure and examine your retina. It could be early cataracts or simply needing glasses."),
            ("P", "Do I need surgery?"),
            ("T", "(on phone) Doctor: I'll check your intraocular pressure and examine your retina. It could be early cataracts or simply needing glasses. Patient: Do I need surgery?"),
            ("D", "Not yet. First we'll do a refraction test and see if glasses help."),
            ("P", "That's a relief. Thank you."),
            ("T", "(on phone) Doctor: Not yet. First we'll do a refraction test and see if glasses help. Patient: That's a relief. Thank you.")
        ]
    },
    11: {
        "theme": "Dermatology",
        "terms": ["Skin", "Rash", "Lesion", "Biopsy", "Eczema", "Psoriasis", "Acne", "Melanoma", "Basal cell carcinoma", "Wart", "Fungal infection", "Urticaria", "Dermatitis", "Mole", "Scar"],
        "acronyms": ["BCC (Basal Cell Carcinoma)", "SCC (Squamous Cell Carcinoma)", "MM (Malignant Melanoma)", "HER2 (Human Epidermal Growth Factor Receptor 2)", "PUVA (Psoralen + UVA)"],
        "abbreviations": ["ID (intradermal)", "SC (subcutaneous)", "BID (twice a day)", "TID (three times a day)", "QHS (every night at bedtime)"],
        "conversation": [
            ("D", "How long have you had this rash on your arm?"),
            ("P", "About two weeks. It itches a lot and sometimes weeps fluid."),
            ("T", "(on phone) Doctor: How long have you had this rash on your arm? Patient: About two weeks. It itches a lot and sometimes weeps fluid."),
            ("D", "It looks like eczema. Have you changed any soaps or lotions recently?"),
            ("P", "Yes, I started using a new body wash."),
            ("T", "(on phone) Doctor: It looks like eczema. Have you changed any soaps or lotions recently? Patient: Yes, I started using a new body wash."),
            ("D", "Stop using it. I'll prescribe a topical steroid cream. Apply twice a day."),
            ("P", "Will it go away completely?"),
            ("T", "(on phone) Doctor: Stop using it. I'll prescribe a topical steroid cream. Apply twice a day. Patient: Will it go away completely?"),
            ("D", "With treatment, yes. But eczema can flare up again. Keep your skin moisturized."),
            ("T", "(on phone) Doctor: With treatment, yes. But eczema can flare up again. Keep your skin moisturized.")
        ]
    },
    12: {
        "theme": "Endocrinology",
        "terms": ["Hormone", "Gland", "Thyroid", "Pancreas", "Adrenal", "Pituitary", "Diabetes", "Hyperthyroidism", "Hypothyroidism", "Insulin", "Glucose", "Metabolism", "Cortisol", "Growth hormone", "Menopause"],
        "acronyms": ["DM (Diabetes Mellitus)", "T1DM (Type 1 Diabetes Mellitus)", "T2DM (Type 2 Diabetes Mellitus)", "HbA1c (Hemoglobin A1c)", "TSH (Thyroid Stimulating Hormone)"],
        "abbreviations": ["BG (blood glucose)", "FBS (fasting blood sugar)", "RBS (random blood sugar)", "T3 (triiodothyronine)", "T4 (thyroxine)"],
        "conversation": [
            ("D", "Your blood sugar levels are high. Have you been feeling very thirsty or urinating frequently?"),
            ("P", "Yes, both. I also feel tired all the time."),
            ("T", "(on phone) Doctor: Your blood sugar levels are high. Have you been feeling very thirsty or urinating frequently? Patient: Yes, both. I also feel tired all the time."),
            ("D", "You likely have type 2 diabetes. We'll start metformin and discuss diet changes."),
            ("P", "Is this reversible?"),
            ("T", "(on phone) Doctor: You likely have type 2 diabetes. We'll start metformin and discuss diet changes. Patient: Is this reversible?"),
            ("D", "With weight loss and exercise, you may put it into remission. Let's work together on a plan."),
            ("P", "I'm ready to make changes. Thank you."),
            ("T", "(on phone) Doctor: With weight loss and exercise, you may put it into remission. Let's work together on a plan. Patient: I'm ready to make changes. Thank you.")
        ]
    },
    13: {
        "theme": "Hematology",
        "terms": ["Blood", "Red blood cell", "White blood cell", "Platelet", "Hemoglobin", "Anemia", "Leukemia", "Lymphoma", "Hemophilia", "Transfusion", "Bone marrow", "Coagulation", "Iron", "Vitamin B12", "Sickle cell disease"],
        "acronyms": ["RBC (Red Blood Cell)", "WBC (White Blood Cell)", "Hgb (Hemoglobin)", "Hct (Hematocrit)", "PT (Prothrombin Time)", "INR (International Normalized Ratio)"],
        "abbreviations": ["CBC (complete blood count)", "DIC (disseminated intravascular coagulation)", "ITP (immune thrombocytopenic purpura)", "TTP (thrombotic thrombocytopenic purpura)", "ALL (acute lymphoblastic leukemia)"],
        "conversation": [
            ("D", "Your blood test shows low hemoglobin. Have you been feeling weak or dizzy?"),
            ("P", "Yes, and my skin looks pale."),
            ("T", "(on phone) Doctor: Your blood test shows low hemoglobin. Have you been feeling weak or dizzy? Patient: Yes, and my skin looks pale."),
            ("D", "You have iron-deficiency anemia. I'll prescribe iron supplements and ask you to eat more red meat and leafy greens."),
            ("P", "Could it be something more serious?"),
            ("T", "(on phone) Doctor: You have iron-deficiency anemia. I'll prescribe iron supplements and ask you to eat more red meat and leafy greens. Patient: Could it be something more serious?"),
            ("D", "We'll repeat the blood test in a month. If no improvement, we may need a bone marrow biopsy."),
            ("P", "I'll follow your advice. Thank you."),
            ("T", "(on phone) Doctor: We'll repeat the blood test in a month. If no improvement, we may need a bone marrow biopsy. Patient: I'll follow your advice. Thank you.")
        ]
    },
    14: {
        "theme": "Oncology",
        "terms": ["Cancer", "Tumor", "Malignant", "Benign", "Metastasis", "Chemotherapy", "Radiation", "Surgery", "Biopsy", "Staging", "Remission", "Oncologist", "Palliative care", "Hospice", "Immunotherapy"],
        "acronyms": ["NSCLC (Non-Small Cell Lung Cancer)", "SCLC (Small Cell Lung Cancer)", "BRCA (Breast Cancer Gene)", "PSA (Prostate Specific Antigen)", "HPV (Human Papillomavirus)"],
        "abbreviations": ["Ca (cancer)", "mets (metastases)", "RT (radiation therapy)", "CTx (chemotherapy)", "BMT (bone marrow transplant)"],
        "conversation": [
            ("D", "The biopsy results show a malignant tumor in your breast."),
            ("P", "Oh no. What are my options?"),
            ("T", "(on phone) Doctor: The biopsy results show a malignant tumor in your breast. Patient: Oh no. What are my options?"),
            ("D", "We have several: surgery, chemotherapy, radiation, or a combination. I've referred you to an oncologist."),
            ("P", "Will I lose my hair?"),
            ("T", "(on phone) Doctor: We have several: surgery, chemotherapy, radiation, or a combination. I've referred you to an oncologist. Patient: Will I lose my hair?"),
            ("D", "Some chemo drugs cause hair loss, but it grows back after treatment. Let's take this one step at a time."),
            ("P", "I'm scared, but I'll do what's necessary."),
            ("T", "(on phone) Doctor: Some chemo drugs cause hair loss, but it grows back after treatment. Let's take this one step at a time. Patient: I'm scared, but I'll do what's necessary.")
        ]
    },
    15: {
        "theme": "Infectious Diseases",
        "terms": ["Bacteria", "Virus", "Fungus", "Parasite", "Infection", "Fever", "Sepsis", "Antibiotic", "Antiviral", "Vaccine", "Contagious", "Incubation period", "Quarantine", "Isolation", "Zoonosis"],
        "acronyms": ["HIV (Human Immunodeficiency Virus)", "AIDS (Acquired Immunodeficiency Syndrome)", "COVID-19 (Coronavirus Disease 2019)", "MRSA (Methicillin-resistant Staphylococcus aureus)", "TB (Tuberculosis)"],
        "abbreviations": ["ID (infectious disease)", "IV (intravenous)", "PO (oral)", "IM (intramuscular)", "STAT (immediately)"],
        "conversation": [
            ("D", "You have a bacterial infection in your lungs. We need to start antibiotics."),
            ("P", "Is it contagious? My family is at home."),
            ("T", "(on phone) Doctor: You have a bacterial infection in your lungs. We need to start antibiotics. Patient: Is it contagious? My family is at home."),
            ("D", "Yes, especially through coughing. I recommend you wear a mask and wash hands frequently."),
            ("P", "How long until I feel better?"),
            ("T", "(on phone) Doctor: Yes, especially through coughing. I recommend you wear a mask and wash hands frequently. Patient: How long until I feel better?"),
            ("D", "You should see improvement in 48 hours. Finish the full course of antibiotics even if you feel better."),
            ("P", "I understand. Thank you."),
            ("T", "(on phone) Doctor: You should see improvement in 48 hours. Finish the full course of antibiotics even if you feel better. Patient: I understand. Thank you.")
        ]
    },
    16: {
        "theme": "Emergency Medicine",
        "terms": ["Trauma", "Fracture", "Laceration", "Burn", "Head injury", "Chest pain", "Stroke", "Anaphylaxis", "Cardiac arrest", "Resuscitation", "Intubation", "CPR", "Defibrillator", "Triage", "Ambulance"],
        "acronyms": ["ER (Emergency Room)", "EMS (Emergency Medical Services)", "ICU (Intensive Care Unit)", "CPR (Cardiopulmonary Resuscitation)", "MI (Myocardial Infarction)"],
        "abbreviations": ["ABC (airway, breathing, circulation)", "LOC (loss of consciousness)", "GCS (Glasgow Coma Scale)", "ETT (endotracheal tube)", "IV (intravenous)"],
        "conversation": [
            ("D", "He was in a car accident. We need a cervical collar and IV access."),
            ("P", "I'm the patient's wife. Is he going to be okay?"),
            ("T", "(on phone) Doctor: He was in a car accident. We need a cervical collar and IV access. Patient's wife: I'm the patient's wife. Is he going to be okay?"),
            ("D", "He has a fractured leg and possible concussion. We're doing a CT scan now."),
            ("P", "Can I see him?"),
            ("T", "(on phone) Doctor: He has a fractured leg and possible concussion. We're doing a CT scan now. Patient's wife: Can I see him?"),
            ("D", "Not yet. Please wait in the waiting room. We'll update you as soon as we know more."),
            ("P", "Thank you, doctor."),
            ("T", "(on phone) Doctor: Not yet. Please wait in the waiting room. We'll update you as soon as we know more. Patient's wife: Thank you, doctor.")
        ]
    },
    17: {
        "theme": "Pharmacology",
        "terms": ["Drug", "Medication", "Dosage", "Side effect", "Contraindication", "Prescription", "Over-the-counter", "Generic", "Brand name", "Tablet", "Capsule", "Liquid", "Topical", "Injection", "Infusion"],
        "acronyms": ["OTC (Over-the-Counter)", "NSAID (Non-Steroidal Anti-Inflammatory Drug)", "ACE (Angiotensin-Converting Enzyme)", "ARB (Angiotensin II Receptor Blocker)", "SSRI (Selective Serotonin Reuptake Inhibitor)"],
        "abbreviations": ["mg (milligram)", "mL (milliliter)", "g (gram)", "po (by mouth)", "prn (as needed)"],
        "conversation": [
            ("D", "I'm prescribing lisinopril for your blood pressure. Take one tablet daily."),
            ("P", "What are the common side effects?"),
            ("T", "(on phone) Doctor: I'm prescribing lisinopril for your blood pressure. Take one tablet daily. Patient: What are the common side effects?"),
            ("D", "Some people get a dry cough or dizziness. If that happens, call me."),
            ("P", "Can I take it with my other medications?"),
            ("T", "(on phone) Doctor: Some people get a dry cough or dizziness. If that happens, call me. Patient: Can I take it with my other medications?"),
            ("D", "Let me review your list. Yes, it's safe with what you're taking now."),
            ("P", "Thank you, doctor."),
            ("T", "(on phone) Doctor: Let me review your list. Yes, it's safe with what you're taking now. Patient: Thank you, doctor.")
        ]
    },
    18: {
        "theme": "Radiology",
        "terms": ["X-ray", "CT scan", "MRI", "Ultrasound", "Mammogram", "Fluoroscopy", "Contrast agent", "Radiation", "Radiologist", "Tomography", "Nuclear medicine", "PET scan", "Bone scan", "Angiography", "Myelogram"],
        "acronyms": ["CT (Computed Tomography)", "MRI (Magnetic Resonance Imaging)", "PET (Positron Emission Tomography)", "SPECT (Single Photon Emission Computed Tomography)", "IVP (Intravenous Pyelogram)"],
        "abbreviations": ["CXR (chest X-ray)", "KUB (kidney, ureter, bladder)", "US (ultrasound)", "MRA (magnetic resonance angiography)", "CTA (CT angiography)"],
        "conversation": [
            ("D", "We need a CT scan of your abdomen to see the source of the pain."),
            ("P", "Does it involve radiation?"),
            ("T", "(on phone) Doctor: We need a CT scan of your abdomen to see the source of the pain. Patient: Does it involve radiation?"),
            ("D", "Yes, a small amount. But the benefit of finding the problem outweighs the risk."),
            ("P", "Do I need to drink anything?"),
            ("T", "(on phone) Doctor: Yes, a small amount. But the benefit of finding the problem outweighs the risk. Patient: Do I need to drink anything?"),
            ("D", "You'll drink an oral contrast liquid one hour before the scan. It helps highlight your intestines."),
            ("P", "Alright, let's do it."),
            ("T", "(on phone) Doctor: You'll drink an oral contrast liquid one hour before the scan. It helps highlight your intestines. Patient: Alright, let's do it.")
        ]
    },
    19: {
        "theme": "Psychiatry",
        "terms": ["Depression", "Anxiety", "Bipolar disorder", "Schizophrenia", "Psychosis", "Insomnia", "PTSD", "OCD", "Panic attack", "Phobia", "Therapy", "Antidepressant", "Antipsychotic", "Mood stabilizer", "Psychiatrist"],
        "acronyms": ["PTSD (Post-Traumatic Stress Disorder)", "OCD (Obsessive-Compulsive Disorder)", "ADHD (Attention Deficit Hyperactivity Disorder)", "GAD (Generalized Anxiety Disorder)", "ECT (Electroconvulsive Therapy)"],
        "abbreviations": ["CBT (cognitive behavioral therapy)", "SSRI (selective serotonin reuptake inhibitor)", "MAOI (monoamine oxidase inhibitor)", "SNRI (serotonin-norepinephrine reuptake inhibitor)", "TCA (tricyclic antidepressant)"],
        "conversation": [
            ("D", "You mentioned feeling sad and losing interest in things you used to enjoy. How long?"),
            ("P", "About three months. I also have trouble sleeping and feel worthless."),
            ("T", "(on phone) Doctor: You mentioned feeling sad and losing interest in things you used to enjoy. How long? Patient: About three months. I also have trouble sleeping and feel worthless."),
            ("D", "This sounds like major depression. I recommend therapy and possibly an antidepressant."),
            ("P", "Will I have to take it forever?"),
            ("T", "(on phone) Doctor: This sounds like major depression. I recommend therapy and possibly an antidepressant. Patient: Will I have to take it forever?"),
            ("D", "Usually 6 to 12 months, but some people need longer. We'll monitor your progress."),
            ("P", "I'm willing to try. Thank you."),
            ("T", "(on phone) Doctor: Usually 6 to 12 months, but some people need longer. We'll monitor your progress. Patient: I'm willing to try. Thank you.")
        ]
    },
    20: {
        "theme": "Medical Acronyms & Abbreviations Review",
        "terms": ["Review of all previous terms: symptom, diagnosis, treatment, prescription, vital signs, blood pressure, heart rate, temperature, allergy, infection, heart, artery, vein, chest pain, hypertension, cholesterol, angina, MI, ECG, lungs, cough, shortness of breath, asthma, COPD, pneumonia, stomach, nausea, vomiting, diarrhea, constipation, brain, headache, seizure, stroke, bone, fracture, arthritis, pregnancy, fetus, kidney, UTI, diabetes, anemia, cancer, virus, antibiotic, vaccine, ER, ICU, CPR, medication, side effect, X-ray, CT, MRI, depression, anxiety"],
        "acronyms": ["All from previous lessons: PCP, EHR, BMI, CBC, BP, ECG, CAD, CHF, MI, HTN, COPD, PE, ARDS, TB, OSA, GERD, IBS, IBD, CNS, TIA, ALS, EEG, ACL, OA, RA, AAP, NICU, PICU, RSV, OB, GYN, PID, PCOS, UTI, BPH, ESRD, AMD, IOP, OCT, LASIK, BCC, SCC, MM, DM, T1DM, T2DM, HbA1c, TSH, RBC, WBC, Hgb, Hct, PT, INR, HIV, AIDS, COVID, MRSA, ER, EMS, ICU, CPR, OTC, NSAID, ACE, ARB, SSRI, CT, MRI, PET, PTSD, OCD, ADHD, GAD, ECT"],
        "abbreviations": ["All from previous lessons: Rx, Hx, Dx, Tx, q.d., ACS, CVD, LV, RV, CCU, SOB, O2, PFT, ABG, RR, GI, PO, NPO, BM, EUS, LOC, GCS, ICP, CSF, Fx, ORIF, PT, NWB, WBAT, PR, IM, SC, gtt, G, P, LMP, EDD, C/S, UA, Cr, BUN, IVP, VCUG, OD, OS, OU, VA, VF, ID, BID, TID, QHS, BG, FBS, RBS, T3, T4, Ca, mets, RT, CTx, BMT, STAT, ABC, ETT, IV, mg, mL, g, prn, CXR, KUB, US, MRA, CTA, CBT, MAOI, SNRI, TCA"],
        "conversation": [
            ("D", "Today we'll review everything you've learned. What does 'BP' stand for?"),
            ("P", "Blood pressure."),
            ("T", "(on phone) Doctor: Today we'll review everything you've learned. What does 'BP' stand for? Patient: Blood pressure."),
            ("D", "Correct. And what is the normal range for adult BP?"),
            ("P", "Around 120/80 mmHg."),
            ("T", "(on phone) Doctor: Correct. And what is the normal range for adult BP? Patient: Around 120/80 mmHg."),
            ("D", "Excellent. Now, what does 'STAT' mean?"),
            ("P", "Immediately – used in emergencies."),
            ("T", "(on phone) Doctor: Excellent. Now, what does 'STAT' mean? Patient: Immediately – used in emergencies."),
            ("D", "You have mastered medical terminology. Congratulations, translator!"),
            ("P", "Thank you, doctor. I feel confident now."),
            ("T", "(on phone) Doctor: You have mastered medical terminology. Congratulations, translator! Patient: Thank you, doctor. I feel confident now.")
        ]
    }
}

# ========== AUDIO FUNCTION (FIXED TIMEOUT) ==========
def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled. Please install edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                # Use the fixed synchronous wrapper
                generate_audio(text, tmp.name)
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

tab1, tab2, tab3, tab4 = st.tabs(["📚 Terminology", "🗣️ Conversation", "❓ Quiz", "📝 Notes"])

# ----- TAB 1: TERMINOLOGY (terms, acronyms, abbreviations) -----
with tab1:
    st.subheader("🏥 Medical Terms")
    cols = st.columns(3)
    for idx, term in enumerate(lesson["terms"]):
        with cols[idx % 3]:
            st.markdown(f"**{term}**")
            play_audio(term, f"term_{lesson_number}_{idx}")
    
    st.markdown("---")
    st.subheader("🔤 Acronyms")
    for idx, acro in enumerate(lesson["acronyms"]):
        st.markdown(f"• {acro}")
        play_audio(acro, f"acro_{lesson_number}_{idx}")
    
    st.markdown("---")
    st.subheader("✍️ Abbreviations")
    for idx, abbr in enumerate(lesson["abbreviations"]):
        st.markdown(f"• {abbr}")
        play_audio(abbr, f"abbr_{lesson_number}_{idx}")

# ----- TAB 2: CONVERSATION (Doctor-Patient-Translator) -----
with tab2:
    st.markdown("### 👨‍⚕️ Doctor – Patient – Medical Translator (over the phone)")
    st.caption("The translator repeats both sides. Listen and practice interpreting.")
    for idx, (speaker, line) in enumerate(lesson["conversation"]):
        if speaker == "D":
            st.markdown(f"**👨‍⚕️ Doctor:** {line}")
        elif speaker == "P":
            st.markdown(f"**🧑‍🦱 Patient:** {line}")
        else:  # T = Translator
            st.markdown(f"**📞 Translator (on phone):** {line}")
        play_audio(line, f"conv_{lesson_number}_{idx}")
        st.markdown("---")

# ----- TAB 3: QUIZ -----
with tab3:
    st.markdown("Test your knowledge of this lesson's terminology and acronyms.")
    # Generate up to 5 quiz questions from the lesson's terms and acronyms
    quiz_questions = []
    # Take up to 3 random terms
    sample_terms = random.sample(lesson["terms"], min(3, len(lesson["terms"])))
    for term in sample_terms:
        quiz_questions.append({
            "question": f"What does the medical term '{term}' refer to?",
            "options": ["A type of medication", "A medical condition or body part", "A surgical instrument", "A hospital department"],
            "answer": "A medical condition or body part"
        })
    # Take up to 2 random acronyms
    sample_acros = random.sample(lesson["acronyms"], min(2, len(lesson["acronyms"])))
    for acro in sample_acros:
        parts = acro.split(" (")
        acronym = parts[0]
        full = parts[1].rstrip(")")
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
        play_audio(q['question'], f"quiz_q_{lesson_number}_{i}")
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
                    play_audio(f"Correct answer: {q['answer']}", f"correct_{lesson_number}_{i}")

# ----- TAB 4: NOTES -----
with tab4:
    st.markdown("### 📝 Study Notes")
    st.markdown(f"""
    - **Theme:** {lesson['theme']}
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
