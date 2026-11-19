"""Project settings."""
import os
from pathlib import Path

# Paths
ROOT = Path(__file__).parent
LABELS_DIR = ROOT / "data" / "labels"
CHROMA_DIR = ROOT / "chroma_db"
RESULTS_DIR = ROOT / "results"
EVAL_FILE = ROOT / "eval" / "questions.json"

# Generic names of the drugs to index
DRUGS = [
    "metformin", "lisinopril", "atorvastatin", "amlodipine", "metoprolol",
    "omeprazole", "simvastatin", "losartan", "levothyroxine", "gabapentin",
    "sertraline", "hydrochlorothiazide", "warfarin", "apixaban", "clopidogrel",
    "ibuprofen", "acetaminophen", "amoxicillin", "azithromycin", "ciprofloxacin",
    "prednisone", "albuterol", "fluoxetine", "escitalopram", "montelukast",
    "pantoprazole", "rosuvastatin", "furosemide", "tramadol", "alprazolam",
    "citalopram", "doxycycline", "lamotrigine", "spironolactone",
]

# Brand name -> generic name
COMMON_BRANDS = {
    "glucophage": "metformin", "zestril": "lisinopril", "prinivil": "lisinopril",
    "lipitor": "atorvastatin", "norvasc": "amlodipine", "lopressor": "metoprolol",
    "toprol": "metoprolol", "prilosec": "omeprazole", "zocor": "simvastatin",
    "cozaar": "losartan", "synthroid": "levothyroxine", "neurontin": "gabapentin",
    "zoloft": "sertraline", "coumadin": "warfarin", "jantoven": "warfarin",
    "eliquis": "apixaban", "plavix": "clopidogrel", "advil": "ibuprofen",
    "motrin": "ibuprofen", "tylenol": "acetaminophen", "zithromax": "azithromycin",
    "cipro": "ciprofloxacin", "proventil": "albuterol", "ventolin": "albuterol",
    "prozac": "fluoxetine", "lexapro": "escitalopram", "singulair": "montelukast",
    "protonix": "pantoprazole", "crestor": "rosuvastatin", "lasix": "furosemide",
    "ultram": "tramadol", "xanax": "alprazolam", "celexa": "citalopram",
    "lamictal": "lamotrigine", "aldactone": "spironolactone", "hctz": "hydrochlorothiazide",
}

# openFDA label field -> section name (old/new/OTC formats map to the same names)
SECTIONS = {
    "boxed_warning": "Boxed Warning",
    "indications_and_usage": "Indications and Usage",
    "dosage_and_administration": "Dosage and Administration",
    "dosage_forms_and_strengths": "Dosage Forms and Strengths",
    "contraindications": "Contraindications",
    "warnings_and_cautions": "Warnings and Precautions",
    "warnings": "Warnings and Precautions",
    "precautions": "Warnings and Precautions",
    "adverse_reactions": "Adverse Reactions",
    "drug_interactions": "Drug Interactions",
    "use_in_specific_populations": "Use in Specific Populations",
    "pregnancy": "Pregnancy",
    "nursing_mothers": "Lactation",
    "lactation": "Lactation",
    "pediatric_use": "Pediatric Use",
    "geriatric_use": "Geriatric Use",
    "overdosage": "Overdosage",
    "mechanism_of_action": "Mechanism of Action",
    "clinical_pharmacology": "Clinical Pharmacology",
    # OTC label fields
    "purpose": "Indications and Usage",
    "do_not_use": "Contraindications",
    "ask_doctor": "Warnings and Precautions",
    "stop_use": "Warnings and Precautions",
    "pregnancy_or_breast_feeding": "Pregnancy",
}

# Chunk size and overlap, in words
CHUNK_WORDS = 180
CHUNK_OVERLAP = 40

# Models and retrieval
EMBED_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
SECTION_BOOST = 0.15  # score bonus for chunks in the section the question targets
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_FALLBACKS = ["gemini-3.5-flash-lite", "gemini-2.5-flash"]  # used on 429/5xx errors
COLLECTION_NAME = "fda_labels"
TOP_K = 5  # chunks passed to the LLM
