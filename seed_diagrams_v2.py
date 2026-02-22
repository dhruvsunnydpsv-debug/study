"""
Verix Audit Engine — Seed diagram-rich questions for all subjects.
Uses verified Wikimedia Commons URLs that are publicly accessible.
"""
import httpx, uuid, json, time

SUPABASE_URL = "https://wfegooasrtbhpursgcvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# =========== VERIFIED WIKIMEDIA COMMONS DIAGRAM URLS ===========
DIAGRAMS = {
    # Biology
    "animal_cell": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Animal_cell_structure_en.svg/800px-Animal_cell_structure_en.svg.png",
    "plant_cell": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Plant_cell_structure_svg_labels.svg/800px-Plant_cell_structure_svg_labels.svg.png",
    "mitosis": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Mitosis_Stages.svg/800px-Mitosis_Stages.svg.png",
    "onion_cells": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Onion_cells_2.jpg",
    "tissue_types": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Illu_epithelium.svg/640px-Illu_epithelium.svg.png",
    "heart": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Diagram_of_the_human_heart_%28cropped%29.svg/600px-Diagram_of_the_human_heart_%28cropped%29.svg.png",
    # Chemistry
    "atom_structure": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Hydrogen_Atom.svg/600px-Hydrogen_Atom.svg.png",
    "periodic_table": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Colour_18-column_periodic_table.svg/800px-Colour_18-column_periodic_table.svg.png",
    "water_molecule": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/H2O_2D_labelled.svg/400px-H2O_2D_labelled.svg.png",
    "states_matter": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Phase_change_-_en.svg/640px-Phase_change_-_en.svg.png",
    # Physics
    "force_diagram": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Free_body_diagram2.svg/400px-Free_body_diagram2.svg.png",
    "speed_time": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Velocity_vs_time_graph.svg/600px-Velocity_vs_time_graph.svg.png",
    "wave": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Sine_wave_amplitude.svg/600px-Sine_wave_amplitude.svg.png",
    # Maths
    "triangle": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Triangle_with_notations_2.svg/400px-Triangle_with_notations_2.svg.png",
    "circle": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Circle-withsegments.svg/400px-Circle-withsegments.svg.png",
    "coordinate": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Cartesian-coordinate-system.svg/500px-Cartesian-coordinate-system.svg.png",
    "parallelogram": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Parallelogram_area.svg/400px-Parallelogram_area.svg.png",
    # SST Maps
    "india_map": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/India-map-en.svg/600px-India-map-en.svg.png",
    "india_rivers": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/India_rivers_and_lakes_map.svg/500px-India_rivers_and_lakes_map.svg.png",
    "india_climate": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/India_climatic_zone_map_en.svg/500px-India_climatic_zone_map_en.svg.png",
    "french_rev": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Serment_du_Jeu_de_paume.jpg/800px-Serment_du_Jeu_de_paume.jpg",
    # English charts
    "bar_graph": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Simple_bar_graph.svg/600px-Simple_bar_graph.svg.png",
}

# =========== QUESTIONS WITH DIAGRAMS ===========
QUESTIONS = [
    # ===== SCIENCE — BIOLOGY (with diagrams) =====
    {"subject":"Science","chapter":"Cell","difficulty":"Medium",
     "question_text":f"Observe the diagram of an animal cell given below and answer the questions that follow. [Image: {DIAGRAMS['animal_cell']}] (a) Identify the organelle labelled 'A' that is known as the powerhouse of the cell. (A) Mitochondria (B) Ribosome (C) Golgi apparatus (D) Endoplasmic reticulum"},
    {"subject":"Science","chapter":"Cell","difficulty":"Medium",
     "question_text":f"Study the diagram of a plant cell shown below. [Image: {DIAGRAMS['plant_cell']}] (a) Name two organelles that are present in a plant cell but absent in an animal cell. (b) What is the function of the large central vacuole in plant cells? (c) Why is the cell wall important for plant cells?"},
    {"subject":"Science","chapter":"Cell","difficulty":"Hard",
     "question_text":f"The following diagram shows the stages of mitosis. [Image: {DIAGRAMS['mitosis']}] (a) Identify the stage in which chromosomes align at the equatorial plate. [1] (b) In which stage does the nuclear membrane reappear? [1] (c) Explain the significance of mitosis in multicellular organisms. [2]"},
    {"subject":"Science","chapter":"Tissues","difficulty":"Medium",
     "question_text":f"The diagram below shows different types of epithelial tissues found in the human body. [Image: {DIAGRAMS['tissue_types']}] (a) Name the type of epithelial tissue that lines blood vessels. (A) Squamous epithelium (B) Cuboidal epithelium (C) Columnar epithelium (D) Stratified epithelium"},
    {"subject":"Science","chapter":"Cell","difficulty":"Easy",
     "question_text":f"A student observed onion peel cells under a microscope as shown. [Image: {DIAGRAMS['onion_cells']}] (a) What shape are the cells? (A) Circular (B) Rectangular (C) Triangular (D) Irregular"},
    {"subject":"Science","chapter":"Tissues","difficulty":"Hard",
     "question_text":f"Case Study: The Human Heart. The diagram shows the internal structure of the human heart. [Image: {DIAGRAMS['heart']}] (i) How many chambers does the human heart have? [1] (ii) Why is the wall of the left ventricle thicker than the right ventricle? [1] (iii) Trace the path of blood from the lungs to the body tissues. [2]"},

    # ===== SCIENCE — CHEMISTRY (with diagrams) =====
    {"subject":"Science","chapter":"Structure of Atom","difficulty":"Easy",
     "question_text":f"The diagram shows the structure of an atom. [Image: {DIAGRAMS['atom_structure']}] (a) The negatively charged particles revolving around the nucleus are called: (A) Protons (B) Neutrons (C) Electrons (D) Photons"},
    {"subject":"Science","chapter":"Structure of Atom","difficulty":"Medium",
     "question_text":f"Study the structure of a water molecule shown below. [Image: {DIAGRAMS['water_molecule']}] (a) What type of bond holds the atoms together in a water molecule? (b) Why is water called a 'universal solvent'? (c) State two unique properties of water that are important for life."},
    {"subject":"Science","chapter":"Matter","difficulty":"Medium",
     "question_text":f"The diagram shows the changes of state of matter. [Image: {DIAGRAMS['states_matter']}] (a) Name the process by which a solid changes directly to gas. (A) Evaporation (B) Sublimation (C) Condensation (D) Deposition"},
    {"subject":"Science","chapter":"Structure of Atom","difficulty":"Hard",
     "question_text":f"Refer to the periodic table given below. [Image: {DIAGRAMS['periodic_table']}] (a) Which group contains the noble gases? (b) Why do elements in the same group have similar chemical properties? (c) Identify the element with atomic number 11 and state its valency."},

    # ===== SCIENCE — PHYSICS (with diagrams) =====
    {"subject":"Science","chapter":"Force and Laws of Motion","difficulty":"Medium",
     "question_text":f"The free body diagram below shows forces acting on a block on a surface. [Image: {DIAGRAMS['force_diagram']}] (a) If the block is in equilibrium, what can you say about the net force? (A) Net force is zero (B) Net force is upward (C) Net force is to the right (D) Net force is downward"},
    {"subject":"Science","chapter":"Motion","difficulty":"Medium",
     "question_text":f"Study the velocity-time graph given below. [Image: {DIAGRAMS['speed_time']}] (a) What does the slope of a velocity-time graph represent? (b) What does the area under the curve represent? (c) Identify the portion of the graph where the object is decelerating."},
    {"subject":"Science","chapter":"Sound","difficulty":"Easy",
     "question_text":f"The diagram shows a transverse wave. [Image: {DIAGRAMS['wave']}] (a) The maximum displacement from the mean position is called: (A) Wavelength (B) Frequency (C) Amplitude (D) Time period"},

    # ===== MATHS (with diagrams) =====
    {"subject":"Maths","chapter":"Triangles","difficulty":"Medium",
     "question_text":f"In the triangle shown below, AB = AC. [Image: {DIAGRAMS['triangle']}] (a) If angle B = 50°, find angle A. (b) Name the type of triangle. (c) Prove that the angles opposite to equal sides are equal."},
    {"subject":"Maths","chapter":"Circles","difficulty":"Medium",
     "question_text":f"Study the circle diagram shown below with centre O. [Image: {DIAGRAMS['circle']}] (a) The longest chord of a circle is called: (A) Radius (B) Diameter (C) Secant (D) Arc"},
    {"subject":"Maths","chapter":"Coordinate Geometry","difficulty":"Easy",
     "question_text":f"The Cartesian coordinate system is shown below. [Image: {DIAGRAMS['coordinate']}] (a) A point (3, -2) lies in which quadrant? (A) I (B) II (C) III (D) IV"},
    {"subject":"Maths","chapter":"Areas of Parallelograms","difficulty":"Medium",
     "question_text":f"The diagram shows a parallelogram ABCD with base and height marked. [Image: {DIAGRAMS['parallelogram']}] (a) If the base is 12 cm and the height is 8 cm, find the area. (b) If a triangle is drawn on the same base and between the same parallels, what will be its area? (c) Prove that the area of a triangle is half the area of the parallelogram on the same base and between the same parallels."},
    {"subject":"Maths","chapter":"Triangles","difficulty":"Hard",
     "question_text":f"Case Study: Geometry in Architecture. An architect uses triangular structures for stability. [Image: {DIAGRAMS['triangle']}] (i) In triangle ABC, if AB = BC = CA = 10 cm, what is the measure of each angle? [1] (ii) What is the name given to such a triangle? [1] (iii) Find the area of this equilateral triangle using Heron's formula. [2]"},

    # ===== SOCIAL SCIENCE — MAP QUESTIONS =====
    {"subject":"Social Science","chapter":"India - Size and Location","difficulty":"Medium",
     "question_text":f"On the given outline map of India, identify and locate the following: [Image: {DIAGRAMS['india_map']}] (a) The Tropic of Cancer (b) The Standard Meridian of India (c) The southernmost point of the Indian mainland"},
    {"subject":"Social Science","chapter":"Drainage","difficulty":"Medium",
     "question_text":f"Study the map of India showing major rivers. [Image: {DIAGRAMS['india_rivers']}] (a) Name the river system marked in the northern plains. (A) Godavari (B) Ganga (C) Krishna (D) Narmada"},
    {"subject":"Social Science","chapter":"Climate","difficulty":"Hard",
     "question_text":f"The climatic zone map of India is shown below. [Image: {DIAGRAMS['india_climate']}] (a) Name the type of climate found in most parts of India. (b) Why does the coastal region of Kerala receive more rainfall than Rajasthan? (c) Explain the role of the Himalayas in influencing India's climate."},
    {"subject":"Social Science","chapter":"French Revolution","difficulty":"Medium",
     "question_text":f"Study the image of the Tennis Court Oath during the French Revolution. [Image: {DIAGRAMS['french_rev']}] (a) In which year did the Tennis Court Oath take place? (A) 1789 (B) 1791 (C) 1793 (D) 1799"},

    # ===== ENGLISH — ANALYTICAL PARAGRAPH =====
    {"subject":"English","chapter":"Writing Skills","difficulty":"Medium",
     "question_text":f"Study the bar graph given below which shows the number of students enrolled in different extracurricular activities in a school. [Image: {DIAGRAMS['bar_graph']}] Write an analytical paragraph (100-120 words) describing the data. Include the most popular and least popular activities, and suggest a reason for the trend."},
]

def upload_questions():
    client = httpx.Client(timeout=30)
    total = len(QUESTIONS)
    success = 0
    failed = 0
    
    for i, q in enumerate(QUESTIONS):
        row = {
            "question_text": q["question_text"],
            "subject": q["subject"],
            "chapter": q.get("chapter", "General"),
            "difficulty": q.get("difficulty", "Medium"),
            "is_rationalised": True,
            "appearance_count": 0
        }
        try:
            r = client.post(
                f"{SUPABASE_URL}/rest/v1/question_bank",
                headers=HEADERS,
                json=row
            )
            if r.status_code in (200, 201):
                success += 1
                print(f"  [{i+1}/{total}] OK: {q['subject']} - {q['chapter']}")
            else:
                failed += 1
                print(f"  [{i+1}/{total}] FAIL ({r.status_code}): {r.text[:100]}")
        except Exception as e:
            failed += 1
            print(f"  [{i+1}/{total}] ERROR: {e}")
        time.sleep(0.2)
    
    print(f"\nDone! {success} uploaded, {failed} failed out of {total}")

if __name__ == "__main__":
    print(f"Uploading {len(QUESTIONS)} diagram-rich questions to Supabase...")
    upload_questions()
