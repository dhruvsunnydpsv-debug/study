"""
Verix Audit Engine — Production Harvester v2.1 (Architect Edition)
Class 9 CBSE ETL Ingestion Pipeline with Parent-Child Cluster Support

Extracts structured question data, downloads diagrams to Supabase Storage,
and loads everything into the class9_question_bank table.
"""

import os
import re
import json
import uuid
import logging
import time
from typing import Optional, Dict, List, Any
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# --- 1. CONFIGURE PRODUCTION LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("harvest_execution.log"),
        logging.StreamHandler()
    ]
)

# --- 2. INITIALIZE SECURE SUPABASE CLIENT ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logging.critical("CRITICAL ERROR: Supabase credentials missing from environment.")
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DIAGRAM_BUCKET = "question_diagrams"

# --- 3. DIAGRAM HANDLING ---
def download_and_upload_diagram(image_url: str, subject: str, chapter: str) -> Optional[str]:
    """Downloads an image into memory and pipes it to Supabase Storage."""
    if not image_url:
        return None

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(image_url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        # Use a more robust split for extension
        url_path = image_url.split('?')[0]
        file_extension = url_path.split('.')[-1] if '.' in url_path else 'png'
        if file_extension.lower() not in ['jpg', 'jpeg', 'png', 'webp', 'svg']:
            file_extension = 'png'

        safe_chapter = re.sub(r'[^a-z0-9_]', '_', chapter.lower().strip())
        safe_subject = re.sub(r'[^a-z0-9_]', '_', subject.lower().strip())
        unique_filename = f"{safe_subject}/{safe_chapter}/{uuid.uuid4().hex}.{file_extension}"

        supabase.storage.from_(DIAGRAM_BUCKET).upload(
            file=response.content,
            path=unique_filename,
            file_options={"content-type": f"image/{file_extension}"}
        )

        public_url = str(supabase.storage.from_(DIAGRAM_BUCKET).get_public_url(unique_filename))
        logging.info(f"  Diagram uploaded: {unique_filename}")
        return public_url

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error downloading diagram {image_url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Supabase upload failed for {image_url}: {e}")
        return None


# --- 4. OPTIONS PARSER ---
def parse_options(raw_text: str, question_type: str) -> Optional[Dict[str, str]]:
    """
    Parses raw option text into strict JSONB format.
    Returns None for subjective questions.
    """
    if question_type in ('Subjective', 'Case-Based') and not re.search(r'\([A-Da-d]\)', raw_text):
        return None

    # Try standard (A)(B)(C)(D) or (a)(b)(c)(d) format
    opts = re.findall(r'\(([A-Da-d])\)\s*([^(]+?)(?=\([A-Da-d]\)|$)', raw_text)
    if opts:
        return {k.upper(): v.strip() for k, v in opts}

    # Try Assertion-Reason numbered format
    ar_opts = re.findall(r'(\d)\.\s*(.+?)(?=\d\.|$)', raw_text)
    if ar_opts:
        return {k: v.strip() for k, v in ar_opts}

    return None


# --- 5. MASTER QUESTION BANK ---
# Production-grade seed data with V2.1 Parent-Child Cluster Architecture
SEED_DATA = [
    # ==================== ENGLISH (LANGUAGE & LITERATURE) ====================
    {
        "subject": "English", "chapter": "Reading Skills — Discursive Passage",
        "question_type": "Comprehension", "marks": 5, "source": "CBSE Blueprint 2025-26",
        "question_text": "Read the following passage carefully and answer the questions that follow.",
        "options": {
            "passage_text": "The Amazon rainforest plays a crucial part in regulating the world's carbon cycle. Spanning over 5.5 million square kilometers, it absorbs billions of tons of carbon dioxide every year. However, recent data from 2024 shows a 12% increase in deforestation rates, threatening this delicate balance...",
            "sub_questions": [
                {
                    "sub_id": "1",
                    "text": "According to the passage, what is the primary function of the Amazon in the global climate?",
                    "type": "MCQ", "marks": 1,
                    "choices": {"A": "Producing timber", "B": "Regulating the carbon cycle", "C": "Providing wildlife habitats", "D": "Generating rainfall"},
                    "correct_answer": "B"
                },
                {
                    "sub_id": "2",
                    "text": "State the percentage increase in deforestation rates observed in 2024.",
                    "type": "Very Short Answer", "marks": 1,
                    "choices": None, "correct_answer": "12%"
                },
                {
                    "sub_id": "3",
                    "text": "What is the total area covered by the Amazon rainforest?",
                    "type": "MCQ", "marks": 1,
                    "choices": {"A": "2.5 million sq km", "B": "4.5 million sq km", "C": "5.5 million sq km", "D": "6.5 million sq km"},
                    "correct_answer": "C"
                },
                {
                    "sub_id": "4",
                    "text": "The phrase 'delicate balance' suggests that the ecosystem is:",
                    "type": "MCQ", "marks": 1,
                    "choices": {"A": "Sturdy", "B": "Fragile", "C": "Irrelevant", "D": "Expanding"},
                    "correct_answer": "B"
                },
                {
                    "sub_id": "5",
                    "text": "Based on the text, what is the main threat mentioned?",
                    "type": "MCQ", "marks": 1,
                    "choices": {"A": "Pollution", "B": "Deforestation", "C": "Global Warming", "D": "Mining"},
                    "correct_answer": "B"
                }
            ]
        },
        "correct_answer": None
    },
    # ==================== SCIENCE — CASE STUDY (COMPETENCY) ====================
    {
        "subject": "Science", "chapter": "Matter in Our Surroundings",
        "question_type": "Case-Based", "marks": 4, "source": "NCERT Activity",
        "competency_flag": True,
        "question_text": "Read the following experimental setup and answer the questions.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Phase_change_-_en.svg/640px-Phase_change_-_en.svg.png",
        "options": {
            "passage_text": "A student takes 50g of ice at 0°C in a beaker and heats it slowly while stirring. They observe that the temperature remains constant at 0°C until all the ice melts completely, despite continuous heating.",
            "sub_questions": [
                {
                    "sub_id": "1",
                    "text": "Why does the temperature remain constant during the melting process?",
                    "type": "MCQ", "marks": 1,
                    "choices": {"A": "Heat is lost to atmosphere", "B": "Used as Latent Heat of Fusion", "C": "Beaker absorbs all heat", "D": "Thermometer is faulty"},
                    "correct_answer": "B"
                },
                {
                    "sub_id": "2",
                    "text": "What is the state of matter at exactly 0°C during this process?",
                    "type": "MCQ", "marks": 1,
                    "choices": {"A": "Only Solid", "B": "Only Liquid", "C": "Both Solid and Liquid", "D": "Gaseous"},
                    "correct_answer": "C"
                },
                {
                    "sub_id": "3",
                    "text": "Define Latent Heat of Fusion based on this experiment.",
                    "type": "Short Answer", "marks": 2,
                    "choices": None, "correct_answer": "The amount of heat required to change 1kg of solid into liquid at atmospheric pressure at its melting point."
                }
            ]
        },
        "correct_answer": None
    },
    # ==================== SCIENCE — BIOLOGY ====================
    {
        "subject": "Science", "chapter": "Cell — The Fundamental Unit of Life",
        "question_text": "Which organelle is known as the 'powerhouse of the cell'?",
        "options": {"A": "Lysosomes", "B": "Mitochondria", "C": "Plastids", "D": "Endoplasmic Reticulum"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Animal_cell_structure_en.svg/800px-Animal_cell_structure_en.svg.png",
        "source": "NCERT Ch.5"
    },
    {
        "subject": "Science", "chapter": "Cell — The Fundamental Unit of Life",
        "question_text": "Which of the following is present only in plant cells and not in animal cells?",
        "options": {"A": "Cell membrane", "B": "Mitochondria", "C": "Cell wall", "D": "Nucleus"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Plant_cell_structure_svg_labels.svg/800px-Plant_cell_structure_svg_labels.svg.png",
        "source": "NCERT Ch.5"
    },
    {
        "subject": "Science", "chapter": "Cell — The Fundamental Unit of Life",
        "question_text": "Assertion (A): The cell membrane is called a selectively permeable membrane. Reason (R): It allows the movement of only certain molecules in and out of the cell.",
        "options": {"1": "Both A and R are true and R is the correct explanation of A.", "2": "Both A and R are true but R is not the correct explanation of A.", "3": "A is true but R is false.", "4": "A is false but R is true."},
        "correct_answer": "1", "marks": 1, "question_type": "Assertion-Reason",
        "source": "CBSE SQP 2025-26"
    },
    {
        "subject": "Science", "chapter": "Cell — The Fundamental Unit of Life",
        "question_text": "Draw a well-labelled diagram of an animal cell. Mention the function of any two organelles shown in your diagram.",
        "options": None, "correct_answer": "A well-labelled diagram showing cell membrane, nucleus, mitochondria, ER, Golgi apparatus, lysosomes, ribosomes. Mitochondria: oxidize glucose to provide energy (ATP). Lysosomes: contain digestive enzymes for breaking down waste.",
        "marks": 5, "question_type": "Subjective",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Animal_cell_structure_en.svg/800px-Animal_cell_structure_en.svg.png",
        "source": "NCERT Ch.5"
    },
    {
        "subject": "Science", "chapter": "Cell — The Fundamental Unit of Life",
        "question_text": "Case Study: A student observed cells from an onion peel and human cheek under a microscope. She noticed that onion peel cells had a definite shape and rigid boundary, while cheek cells were more irregular. (i) Name the structure responsible for the definite shape in onion peel cells. [1] (ii) Which organelle would be more prominent in cheek cells due to energy needs? [1] (iii) Explain why lysosomes are called 'suicide bags' of the cell. [2]",
        "options": None, "correct_answer": "(i) Cell wall (ii) Mitochondria (iii) Lysosomes contain powerful digestive enzymes. When a cell is damaged or dies, lysosomes burst and their enzymes digest the entire cell contents, hence called suicide bags.",
        "marks": 4, "question_type": "Case-Based",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Onion_cells_2.jpg",
        "source": "CBSE SQP 2025-26"
    },
    {
        "subject": "Science", "chapter": "Tissues",
        "question_text": "Which type of tissue forms the lining of blood vessels?",
        "options": {"A": "Squamous epithelium", "B": "Cuboidal epithelium", "C": "Columnar epithelium", "D": "Stratified epithelium"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.6"
    },
    {
        "subject": "Science", "chapter": "Tissues",
        "question_text": "Differentiate between striated and unstriated muscles. Give one example of each.",
        "options": None, "correct_answer": "Striated muscles: cylindrical, multinucleated, voluntary, show light and dark bands (e.g., biceps). Unstriated muscles: spindle-shaped, uninucleated, involuntary, no striations (e.g., muscles of stomach).",
        "marks": 3, "question_type": "Subjective",
        "source": "NCERT Ch.6"
    },

    # ==================== SCIENCE — CHEMISTRY ====================
    {
        "subject": "Science", "chapter": "Matter in Our Surroundings",
        "question_text": "The process by which a solid directly changes into gas without passing through the liquid state is called:",
        "options": {"A": "Evaporation", "B": "Sublimation", "C": "Condensation", "D": "Deposition"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Phase_change_-_en.svg/640px-Phase_change_-_en.svg.png",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Science", "chapter": "Matter in Our Surroundings",
        "question_text": "Explain with an activity how the rate of evaporation increases with increase in surface area.",
        "options": None, "correct_answer": "Take two plates — one flat and one deep. Pour equal amounts of water in both. The water in the flat plate evaporates faster because it has a larger surface area exposed to the atmosphere.",
        "marks": 3, "question_type": "Subjective",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Science", "chapter": "Is Matter Around Us Pure",
        "question_text": "Which of the following is a homogeneous mixture?",
        "options": {"A": "Air", "B": "Soil", "C": "Blood", "D": "Milk"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.2"
    },
    {
        "subject": "Science", "chapter": "Structure of the Atom",
        "question_text": "The number of protons in the nucleus of an atom is called its:",
        "options": {"A": "Mass number", "B": "Atomic number", "C": "Valency", "D": "Neutron number"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Hydrogen_Atom.svg/600px-Hydrogen_Atom.svg.png",
        "source": "NCERT Ch.4"
    },
    {
        "subject": "Science", "chapter": "Structure of the Atom",
        "question_text": "Compare Thomson's and Rutherford's models of the atom. What was the major limitation of Rutherford's model?",
        "options": None, "correct_answer": "Thomson's model: atom is a positively charged sphere with electrons embedded like seeds in a watermelon. Rutherford's model: atom has a tiny dense positive nucleus with electrons revolving around it. Limitation of Rutherford: could not explain why electrons do not lose energy and spiral into the nucleus.",
        "marks": 5, "question_type": "Subjective",
        "source": "NCERT Ch.4"
    },
    {
        "subject": "Science", "chapter": "Atoms and Molecules",
        "question_text": "Assertion (A): One mole of oxygen atoms contains 6.022 × 10²³ atoms. Reason (R): The molar mass of oxygen is 16 g/mol.",
        "options": {"1": "Both A and R are true and R is the correct explanation of A.", "2": "Both A and R are true but R is not the correct explanation of A.", "3": "A is true but R is false.", "4": "A is false but R is true."},
        "correct_answer": "2", "marks": 1, "question_type": "Assertion-Reason",
        "source": "CBSE SQP 2025-26"
    },

    # ==================== SCIENCE — PHYSICS ====================
    {
        "subject": "Science", "chapter": "Motion",
        "question_text": "The area under a velocity-time graph represents:",
        "options": {"A": "Speed of the object", "B": "Acceleration", "C": "Distance travelled", "D": "Velocity"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Velocity_vs_time_graph.svg/600px-Velocity_vs_time_graph.svg.png",
        "source": "NCERT Ch.8"
    },
    {
        "subject": "Science", "chapter": "Motion",
        "question_text": "A car starts from rest and attains a velocity of 20 m/s in 10 seconds. Calculate: (a) the acceleration of the car [1] (b) the distance covered in this time [2]",
        "options": None, "correct_answer": "(a) a = (v-u)/t = (20-0)/10 = 2 m/s² (b) s = ut + ½at² = 0 + ½(2)(100) = 100 m",
        "marks": 3, "question_type": "Subjective",
        "source": "NCERT Ch.8"
    },
    {
        "subject": "Science", "chapter": "Force and Laws of Motion",
        "question_text": "Newton's first law of motion is also known as:",
        "options": {"A": "Law of acceleration", "B": "Law of inertia", "C": "Law of action and reaction", "D": "Law of gravitation"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Free_body_diagram2.svg/400px-Free_body_diagram2.svg.png",
        "source": "NCERT Ch.9"
    },
    {
        "subject": "Science", "chapter": "Force and Laws of Motion",
        "question_text": "Case Study: A cricket player moves his hands backward while catching a fast ball. (i) Which law of motion is involved in this action? [1] (ii) Why does the player move his hands backward? [1] (iii) A 150 g ball moving at 20 m/s is caught in 0.1 s. Calculate the force exerted by the ball on the player's hands. [2]",
        "options": None, "correct_answer": "(i) Newton's second law (ii) To increase the time of contact, thereby reducing the force on hands (rate of change of momentum decreases) (iii) F = m(v-u)/t = 0.15(0-20)/0.1 = -30 N. Force = 30 N",
        "marks": 4, "question_type": "Case-Based",
        "source": "CBSE SQP 2025-26"
    },
    {
        "subject": "Science", "chapter": "Gravitation",
        "question_text": "The value of g on the surface of the Moon is 1/6th of that on Earth. What would be the weight of a 60 kg person on the Moon?",
        "options": {"A": "10 N", "B": "60 N", "C": "100 N", "D": "600 N"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.10"
    },
    {
        "subject": "Science", "chapter": "Sound",
        "question_text": "The maximum displacement of a vibrating object from its mean position is called:",
        "options": {"A": "Wavelength", "B": "Frequency", "C": "Amplitude", "D": "Time period"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Sine_wave_amplitude.svg/600px-Sine_wave_amplitude.svg.png",
        "source": "NCERT Ch.12"
    },

    # ==================== MATHEMATICS ====================
    {
        "subject": "Mathematics", "chapter": "Number Systems",
        "question_text": "Every rational number is:",
        "options": {"A": "A natural number", "B": "An integer", "C": "A real number", "D": "A whole number"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Mathematics", "chapter": "Number Systems",
        "question_text": "Rationalise the denominator of 1/(√7 − 2).",
        "options": None, "correct_answer": "Multiply numerator and denominator by (√7 + 2): 1/(√7-2) × (√7+2)/(√7+2) = (√7+2)/(7-4) = (√7+2)/3",
        "marks": 2, "question_type": "Subjective",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Mathematics", "chapter": "Polynomials",
        "question_text": "If p(x) = x² − 3x + 2, then p(1) is equal to:",
        "options": {"A": "0", "B": "1", "C": "2", "D": "-1"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.2"
    },
    {
        "subject": "Mathematics", "chapter": "Polynomials",
        "question_text": "Factorise: x³ − 23x² + 142x − 120 using factor theorem.",
        "options": None, "correct_answer": "p(1) = 1-23+142-120 = 0, so (x-1) is a factor. Dividing: x³-23x²+142x-120 = (x-1)(x²-22x+120) = (x-1)(x-10)(x-12)",
        "marks": 3, "question_type": "Subjective",
        "source": "NCERT Ch.2"
    },
    {
        "subject": "Mathematics", "chapter": "Coordinate Geometry",
        "question_text": "The point (−3, 5) lies in which quadrant?",
        "options": {"A": "I", "B": "II", "C": "III", "D": "IV"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Cartesian-coordinate-system.svg/500px-Cartesian-coordinate-system.svg.png",
        "source": "NCERT Ch.3"
    },
    {
        "subject": "Mathematics", "chapter": "Linear Equations in Two Variables",
        "question_text": "Which of the following is a solution of x + 2y = 6?",
        "options": {"A": "(2, 3)", "B": "(4, 1)", "C": "(6, 1)", "D": "(1, 3)"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.4"
    },
    {
        "subject": "Mathematics", "chapter": "Triangles",
        "question_text": "In △ABC, if AB = AC and ∠B = 65°, find ∠A.",
        "options": None, "correct_answer": "Since AB = AC, ∠B = ∠C = 65°. Sum of angles = 180°. ∠A = 180° - 65° - 65° = 50°",
        "marks": 2, "question_type": "Subjective",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Triangle_with_notations_2.svg/400px-Triangle_with_notations_2.svg.png",
        "source": "NCERT Ch.7"
    },
    {
        "subject": "Mathematics", "chapter": "Triangles",
        "question_text": "Prove that the angles opposite to equal sides of an isosceles triangle are equal.",
        "options": None, "correct_answer": "In △ABC where AB=AC, draw bisector AD of ∠A to BC. In △ABD and △ACD: AB=AC (given), AD=AD (common), ∠BAD=∠CAD (AD bisects ∠A). By SAS, △ABD ≅ △ACD. Therefore ∠B = ∠C (CPCT).",
        "marks": 5, "question_type": "Subjective",
        "source": "NCERT Ch.7"
    },
    {
        "subject": "Mathematics", "chapter": "Circles",
        "question_text": "The longest chord of a circle is its:",
        "options": {"A": "Radius", "B": "Diameter", "C": "Secant", "D": "Arc"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Circle-withsegments.svg/400px-Circle-withsegments.svg.png",
        "source": "NCERT Ch.10"
    },
    {
        "subject": "Mathematics", "chapter": "Heron's Formula",
        "question_text": "Case Study: A triangular park has sides 40 m, 32 m, and 24 m. The municipal corporation wants to plant grass inside the park at a cost of ₹12 per m². (i) Find the semi-perimeter of the triangle. [1] (ii) Find the area using Heron's formula. [1] (iii) Find the total cost of planting grass. [2]",
        "options": None, "correct_answer": "(i) s = (40+32+24)/2 = 48 m (ii) Area = √(48×8×16×24) = √147456 = 384 m² (iii) Cost = 384 × 12 = ₹4608",
        "marks": 4, "question_type": "Case-Based",
        "source": "CBSE SQP 2025-26"
    },
    {
        "subject": "Mathematics", "chapter": "Areas of Parallelograms and Triangles",
        "question_text": "A parallelogram ABCD has base 12 cm and height 8 cm. The area of triangle ABD is:",
        "options": {"A": "48 cm²", "B": "96 cm²", "C": "24 cm²", "D": "72 cm²"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Parallelogram_area.svg/400px-Parallelogram_area.svg.png",
        "source": "NCERT Ch.9"
    },
    {
        "subject": "Mathematics", "chapter": "Statistics",
        "question_text": "The mean of the first 5 natural numbers is:",
        "options": {"A": "2", "B": "3", "C": "4", "D": "5"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.14"
    },
    {
        "subject": "Mathematics", "chapter": "Probability",
        "question_text": "A coin is tossed 1000 times: 560 heads, 440 tails. The probability of getting a tail is:",
        "options": {"A": "0.56", "B": "0.44", "C": "0.50", "D": "0.22"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.15"
    },

    # ==================== SOCIAL SCIENCE — HISTORY ====================
    {
        "subject": "Social Science", "chapter": "The French Revolution",
        "question_text": "The fall of the Bastille took place on:",
        "options": {"A": "14 July 1789", "B": "5 May 1789", "C": "20 June 1789", "D": "4 August 1789"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Serment_du_Jeu_de_paume.jpg/800px-Serment_du_Jeu_de_paume.jpg",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Social Science", "chapter": "The French Revolution",
        "question_text": "Explain the role of philosophers in the French Revolution.",
        "options": None, "correct_answer": "Philosophers like Rousseau (Social Contract, popular sovereignty), Locke (against divine right, government by consent), and Montesquieu (separation of powers) spread ideas of liberty, equality, and individual rights. Their writings were widely discussed in salons and coffee houses, creating an intellectual environment for revolution.",
        "marks": 5, "question_type": "Subjective",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Social Science", "chapter": "Socialism in Europe and the Russian Revolution",
        "question_text": "Which party was led by Lenin during the Russian Revolution?",
        "options": {"A": "Mensheviks", "B": "Bolsheviks", "C": "Social Democrats", "D": "Duma"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.2"
    },

    # ==================== SOCIAL SCIENCE — GEOGRAPHY ====================
    {
        "subject": "Social Science", "chapter": "India — Size and Location",
        "question_text": "The Tropic of Cancer passes through how many Indian states?",
        "options": {"A": "6", "B": "7", "C": "8", "D": "9"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/India-map-en.svg/600px-India-map-en.svg.png",
        "source": "NCERT Ch.1"
    },
    {
        "subject": "Social Science", "chapter": "Drainage",
        "question_text": "Which is the longest river of India?",
        "options": {"A": "Yamuna", "B": "Ganga", "C": "Godavari", "D": "Brahmaputra"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/India_rivers_and_lakes_map.svg/500px-India_rivers_and_lakes_map.svg.png",
        "source": "NCERT Ch.3"
    },
    {
        "subject": "Social Science", "chapter": "Climate",
        "question_text": "Explain the role of the Himalayas in influencing India's climate.",
        "options": None, "correct_answer": "The Himalayas act as a climatic barrier: (1) They block cold Central Asian winds from entering the subcontinent, keeping winters relatively mild. (2) They force the southwest monsoon winds to rise, causing orographic rainfall in the northern plains. (3) They concentrate the monsoon's moisture within the subcontinent.",
        "marks": 3, "question_type": "Subjective",
        "source": "NCERT Ch.4"
    },
    {
        "subject": "Social Science", "chapter": "Climate",
        "question_text": "Map-Based Question: On a political map of India, mark and label: (a) The Tropic of Cancer (b) The Standard Meridian of India (82°30'E) (c) One state receiving highest rainfall",
        "options": None, "correct_answer": "(a) Tropic of Cancer at 23.5°N passing through Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura, Mizoram (b) 82°30'E passing through Mirzapur, UP (c) Meghalaya (Mawsynram/Cherrapunji)",
        "marks": 5, "question_type": "Subjective",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/India_climatic_zone_map_en.svg/500px-India_climatic_zone_map_en.svg.png",
        "source": "CBSE SQP 2025-26"
    },

    # ==================== SOCIAL SCIENCE — CIVICS ====================
    {
        "subject": "Social Science", "chapter": "What is Democracy? Why Democracy?",
        "question_text": "Which of the following is NOT a feature of democracy?",
        "options": {"A": "Rulers elected by the people", "B": "Free and fair elections", "C": "Rule by hereditary monarch", "D": "One person, one vote"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.1 (Civics)"
    },
    {
        "subject": "Social Science", "chapter": "Constitutional Design",
        "question_text": "Who is considered the 'Father of the Indian Constitution'?",
        "options": {"A": "Mahatma Gandhi", "B": "Jawaharlal Nehru", "C": "B.R. Ambedkar", "D": "Sardar Patel"},
        "correct_answer": "C", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.2 (Civics)"
    },

    # ==================== SOCIAL SCIENCE — ECONOMICS ====================
    {
        "subject": "Social Science", "chapter": "The Story of Village Palampur",
        "question_text": "Which of the following is a fixed factor of production?",
        "options": {"A": "Labour", "B": "Land", "C": "Raw materials", "D": "Capital"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Ch.1 (Eco)"
    },
    {
        "subject": "Social Science", "chapter": "People as Resource",
        "question_text": "Case Study: In village Sarvapalli, 60% of workers are engaged in agriculture, 25% in services, and 15% in industry. (i) What does this suggest about the village economy? [1] (ii) What is 'disguised unemployment'? [1] (iii) Suggest two measures to reduce unemployment in such a village. [2]",
        "options": None, "correct_answer": "(i) The economy is primarily agrarian with limited industrialisation. (ii) Disguised unemployment occurs when more people are employed in a job than are actually needed; removing some workers would not reduce output. (iii) (a) Setting up small-scale industries (b) Investing in skill development and vocational training for youth.",
        "marks": 4, "question_type": "Case-Based",
        "source": "CBSE SQP 2025-26"
    },

    # ==================== ENGLISH ====================
    {
        "subject": "English", "chapter": "Writing Skills — Analytical Paragraph",
        "question_text": "Study the bar graph given below which shows the number of students enrolled in different extracurricular activities in a school. Write an analytical paragraph (100-120 words) describing the data shown. Include the most popular and least popular activities, and suggest possible reasons for the trend.",
        "options": None, "correct_answer": "The bar graph illustrates student enrollment across five extracurricular activities. Sports leads with the highest enrollment, followed by Music and Art. Coding Club and Drama have comparatively lower numbers. The data suggests students prefer physical activities, likely due to health awareness campaigns. Creative arts maintain moderate popularity. Technical and performing arts clubs may need promotional efforts to boost participation.",
        "marks": 5, "question_type": "Subjective",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Simple_bar_graph.svg/600px-Simple_bar_graph.svg.png",
        "source": "CBSE SQP 2025-26"
    },
    {
        "subject": "English", "chapter": "Beehive — The Fun They Had",
        "question_text": "How is the school described in 'The Fun They Had' different from schools today?",
        "options": None, "correct_answer": "In the story, the school is a room in Margie's house with a mechanical teacher (computer screen). There are no classmates, no playground, no human teacher. Books are on a screen. This differs from today's schools which have physical classrooms, friends, teachers, and printed books. The story highlights the value of social learning.",
        "marks": 3, "question_type": "Subjective",
        "source": "NCERT Beehive Ch.1"
    },
    {
        "subject": "English", "chapter": "Beehive — The Sound of Music",
        "question_text": "Evelyn Glennie's achievement teaches us that:",
        "options": {"A": "Music is only for talented people", "B": "Disability cannot stop determination", "C": "Everyone should learn percussion", "D": "Scottish musicians are the best"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "NCERT Beehive Ch.2"
    },
    {
        "subject": "English", "chapter": "Grammar — Tenses",
        "question_text": "Fill in the blanks with the correct form of the verb: She _____ (go) to school every day. Yesterday, she _____ (not go) because she _____ (be) unwell.",
        "options": None, "correct_answer": "goes, did not go, was",
        "marks": 2, "question_type": "Subjective",
        "source": "CBSE Grammar"
    },

    # ==================== HINDI ====================
    {
        "subject": "Hindi", "chapter": "दो बैलों की कथा",
        "question_text": "'दो बैलों की कथा' के लेखक कौन हैं?",
        "options": {"A": "प्रेमचंद", "B": "हरिशंकर परसाई", "C": "महादेवी वर्मा", "D": "जयशंकर प्रसाद"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "source": "NCERT क्षितिज"
    },
    {
        "subject": "Hindi", "chapter": "दो बैलों की कथा",
        "question_text": "हीरा और मोती की मित्रता से हमें क्या शिक्षा मिलती है? विस्तार से लिखिए।",
        "options": None, "correct_answer": "हीरा और मोती की मित्रता से हमें सच्ची दोस्ती, एकता, और अन्याय के विरुद्ध संघर्ष की शिक्षा मिलती है। दोनों बैल हर परिस्थिति में एक-दूसरे का साथ देते हैं, चाहे कठिनाई कितनी भी बड़ी हो। यह कहानी हमें सिखाती है कि एकजुट रहकर अत्याचार का सामना किया जा सकता है।",
        "marks": 5, "question_type": "Subjective",
        "source": "NCERT क्षितिज"
    },
    {
        "subject": "Hindi", "chapter": "व्याकरण — संधि",
        "question_text": "'विद्यालय' का सन्धि-विच्छेद है:",
        "options": {"A": "विद्या + लय", "B": "विद्या + आलय", "C": "विद + आलय", "D": "विद्या + अलय"},
        "correct_answer": "B", "marks": 1, "question_type": "MCQ",
        "source": "व्याकरण"
    },

    # ==================== SANSKRIT ====================
    {
        "subject": "Sanskrit", "chapter": "शेमुषी — भारतीवसन्तगीतिः",
        "question_text": "'भारतीवसन्तगीतिः' पाठे वसन्तऋतोः वर्णनम् कुत्र दृश्यते?",
        "options": None, "correct_answer": "भारतीवसन्तगीतिः पाठे प्रकृतेः सौन्दर्यस्य वर्णनं वर्तते। वसन्तकाले पुष्पाणि विकसन्ति, कोकिलाः मधुरं गायन्ति, वायुः सुगन्धितः भवति। सर्वत्र आनन्दस्य वातावरणं दृश्यते।",
        "marks": 2, "question_type": "Subjective",
        "source": "शेमुषी"
    },
    {
        "subject": "Sanskrit", "chapter": "व्याकरण — सन्धिः",
        "question_text": "'सूर्योदयः' इत्यस्य सन्धिविच्छेदम् अस्ति:",
        "options": {"A": "सूर्य + उदयः", "B": "सूर्यो + दयः", "C": "सूर्य + ओदयः", "D": "सूर + उदयः"},
        "correct_answer": "A", "marks": 1, "question_type": "MCQ",
        "source": "व्याकरण"
    },
    },
]


# --- 6. DEEP SCRAPER ENGINE (V2.1) ---
class DeepScraper:
    """Automated scraper for educational portals (NCERTBooks.Guru / LearnCBSE)."""

    @staticmethod
    def scrape_ncert_guru(url: str, subject: str, chapter: str) -> List[Dict[str, Any]]:
        """Scrapes MCQs from NCERTBooks.Guru structure."""
        extracted = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Usually questions are in <p> tags inside .entry-content
            content = soup.select_one('.entry-content')
            if not content:
                content = soup.find('article') or soup.find('body')

            paragraphs = content.find_all('p')
            current_q = None

            for p in paragraphs:
                text = p.get_text(separator=" ", strip=True)
                
                # Detect Question Starts (e.g. "1. Question text")
                q_match = re.match(r'^(\d+)[\.\s]+(.*)', text)
                if q_match:
                    # Save previous question if it exists
                    if current_q and current_q.get("options") and current_q.get("correct_answer"):
                        extracted.append(current_q)
                    
                    q_num = q_match.group(1)
                    q_body = q_match.group(2)
                    
                    # Check if options are in the same paragraph
                    opts = parse_options(q_body, "MCQ")
                    clean_text = re.sub(r'\(a\).*', '', q_body, flags=re.IGNORECASE).strip()
                    
                    current_q = {
                        "subject": subject,
                        "chapter": chapter,
                        "question_text": f"Q{q_num}. {clean_text}",
                        "options": opts,
                        "marks": 1,
                        "question_type": "MCQ",
                        "source": "NCERTBooks.Guru",
                        "correct_answer": None
                    }
                
                # Detect Answer Paragraphs
                elif current_q and not current_q["correct_answer"]:
                    # Look for "Answer: (a)" or just "(a)"
                    ans_match = re.search(r'Answer:?\s*\(([a-dA-D])\)', text, re.IGNORECASE)
                    if not ans_match:
                        ans_match = re.match(r'^\(([a-dA-D])\)', text)
                    
                    if ans_match:
                        current_q["correct_answer"] = ans_match.group(1).upper()
                        # If options weren't in the question paragraph, they might be here or in between
            
            if current_q:
                extracted.append(current_q)
                
            logging.info(f"  [Scraper] Extracted {len(extracted)} questions from {url}")
            return extracted
        except Exception as e:
            logging.error(f"  [Scraper] Failed to scrape {url}: {e}")
            return []

# --- 7. MAIN ETL PIPELINE ---
def execute_harvest_pipeline():
    """Main ETL Pipeline: processes seed data, downloads diagrams, loads into database."""
    logging.info("=" * 60)
    logging.info("VERIX HARVEST ENGINE v2.1 — INITIATING")
    
    # Optional: External Sources for Option B
    EXTERNAL_SOURCES = [
        {"url": "https://www.ncertbooks.guru/mcq-questions-for-class-9-science-chapter-5-with-answers/", "subject": "Science", "chapter": "The Fundamental Unit of Life"},
        {"url": "https://www.ncertbooks.guru/mcq-questions-for-class-9-science-chapter-1-with-answers/", "subject": "Science", "chapter": "Matter in Our Surroundings"},
    ]
    
    full_pool = SEED_DATA.copy()
    for source in EXTERNAL_SOURCES:
        scraped = DeepScraper.scrape_ncert_guru(source["url"], source["subject"], source["chapter"])
        full_pool.extend(scraped)

    logging.info(f"Total items in pool: {len(full_pool)}")
    logging.info("=" * 60)

    successful_inserts = 0
    duplicate_skips = 0
    diagram_uploads = 0
    errors = 0

    for i, item in enumerate(full_pool):
        try:
            # Step 1: Handle Diagram
            permanent_diagram_url = None
            image_url = item.get("image_url")
            if image_url:
                permanent_diagram_url = download_and_upload_diagram(
                    image_url, item["subject"], item["chapter"]
                )
                if permanent_diagram_url:
                    diagram_uploads += 1

            # Step 2: Build Payload (strict JSONB format)
            payload = {
                "subject": item["subject"],
                "chapter": item["chapter"],
                "question_text": item["question_text"],
                "options": item.get("options"),  # Already in correct JSONB format
                "correct_answer": item.get("correct_answer"),
                "diagram_url": permanent_diagram_url or image_url,
                "marks": item.get("marks"),
                "question_type": item.get("question_type"),
                "source_reference": item.get("source"),
                "competency_flag": item.get("competency_flag", False)
            }

            # Step 3: Database Insert
            supabase.table("class9_question_bank").insert(payload).execute()
            successful_inserts += 1
            logging.info(f"  [{i+1}/{len(SEED_DATA)}] SECURED: [{item['subject']}] {item['chapter']} ({item['question_type']}, {item['marks']}m) — Diagram: {'YES' if permanent_diagram_url else 'NO'}")

            # Rate limiting
            time.sleep(0.5)

        except Exception as e:
            if 'duplicate key value' in str(e).lower() or '23505' in str(e):
                logging.warning(f"  [{i+1}/{len(SEED_DATA)}] DUPLICATE: [{item['subject']}] Skipped.")
                duplicate_skips += 1
            else:
                logging.error(f"  [{i+1}/{len(SEED_DATA)}] ERROR: {e}")
                errors += 1

    logging.info("=" * 60)
    logging.info("PIPELINE EXECUTION COMPLETE")
    logging.info(f"  Inserted:   {successful_inserts}")
    logging.info(f"  Duplicates: {duplicate_skips}")
    logging.info(f"  Diagrams:   {diagram_uploads}")
    logging.info(f"  Errors:     {errors}")
    logging.info("=" * 60)


if __name__ == "__main__":
    execute_harvest_pipeline()
