
import json
import random

def generate_questions(grade, subject, count=500):
    questions = []
    
    # Templates for diversity
    templates = {
        "Maths": [
            "Find the value of {var} if {eq}.",
            "In triangle ABC, {prop}.",
            "Calculate the area of a {shape} with {dim}.",
            "If p(x) = {poly}, find the zero of the polynomial.",
            "Solve for x: {eq2}."
        ],
        "Science": [
            "Explain the process of {process}.",
            "What is the function of {part} in the human {system}?",
            "Define {term} and give an example.",
            "Draw a labeled diagram of {diag}. [Image: https://dummyimage.com/600x400/000/fff&text={diag_slug}]",
            "Why is {subst} called the {alias}?"
        ],
        "Physics": [
            "A body of mass {m}kg moves with velocity {v}m/s. Calculate {calc}.",
            "State {law} and give its mathematical expression.",
            "Explain the working of {device} with a diagram. [Image: https://dummyimage.com/600x400/000/fff&text={device_slug}]",
            "Find the equivalent resistance in a {type} circuit with resistors {r1}Ω and {r2}Ω."
        ],
        "Chemistry": [
            "Balance the following chemical equation: {eq}.",
            "What is the atomic number of {element}?",
            "Explain the {bond} bonding in {molecule}.",
            "Define {term} and explain its significance in {topic}."
        ],
        "Social Science": [
            "Discuss the causes of the {event}.",
            "Who was the leader of the {movement}?",
            "On the map of India, mark {place}. [Image: https://dummyimage.com/600x400/000/fff&text=Map_of_{place_slug}]",
            "Explain the importance of {resource} in the economy."
        ],
        "Sanskrit": [
            "अधोलिखितं गद्यांशं पठित्वा प्रश्नानां उत्तराणि लिखत - {text}",
            "सन्धिं कुरुत - {s1} + {s2}",
            "विग्रहं कुरुत - {v1}",
            "शब्दरूपाणि लिखत - {word}"
        ]
    }

    placeholders = {
        "var": ["x", "y", "z", "a", "b"],
        "eq": ["2x + 5 = 15", "x^2 - 4 = 0", "3y - 7 = 14", "sin(x) = 0.5"],
        "prop": ["AB=BC and angle B=90", "AC is the longest side", "the sum of two sides is greater than the third"],
        "shape": ["circle", "square", "rectangle", "trapezium"],
        "dim": ["radius 7cm", "side 5m", "length 10cm and width 4cm", "base 6cm and height 8cm"],
        "poly": ["x^2 + 5x + 6", "2x - 3", "x^3 - 1"],
        "eq2": ["3x/2 + 5 = 11", "log(x) = 2", "x^2 + x + 1 = 0"],
        "process": ["photosynthesis", "respiration", "evaporation", "distillation", "osmosis"],
        "part": ["mitochondria", "nucleus", "chloroplast", "ribosome"],
        "system": ["cell", "body", "plant"],
        "term": ["force", "energy", "work", "power", "isotope", "isobar", "valency"],
        "diag": ["Plant Cell", "Animal Cell", "Nephron", "Human Eye"],
        "diag_slug": ["PlantCell", "AnimalCell", "Nephron", "HumanEye"],
        "subst": ["Mitochondria", "Lysosome", "Ribosome"],
        "alias": ["powerhouse of the cell", "suicide bag", "protein factory"],
        "m": ["2", "5", "10", "0.5"],
        "v": ["10", "20", "30", "5"],
        "calc": ["kinetic energy", "momentum", "force required to stop"],
        "law": ["Newton's First Law", "Ohm's Law", "Law of Conservation of Energy"],
        "device": ["Electric Motor", "Galvanometer", "Prism"],
        "device_slug": ["Motor", "Galvanometer", "Prism"],
        "type": ["series", "parallel"],
        "r1": ["5", "10", "2"],
        "r2": ["10", "20", "4"],
        "bond": ["ionic", "covalent", "metallic"],
        "molecule": ["H2O", "CO2", "NaCl", "CH4"],
        "event": ["French Revolution", "Russian Revolution", "Industrial Revolution"],
        "movement": ["Non-Cooperation Movement", "Quit India Movement", "Civil Disobedience"],
        "place": ["Delhi", "Mumbai", "Kolkata", "Chennai", "Himalayas"],
        "place_slug": ["Delhi", "Mumbai", "Kolkata", "Chennai", "Himalayas"],
        "resource": ["water", "coal", "forests", "minerals"],
        "s1": ["देव", "इति", "तथा"],
        "s2": ["आलय", "अपि", "एव"],
        "v1": ["राजपुरुषः", "महाकविः", "नीलोत्पलम्"],
        "word": ["राम", "लता", "फल"],
        "text": ["एकदा एकः काकः तृषितः आसीत् ...", "हिमालये अनेके वृक्षाः सन्ति ..."]
    }

    sub_templates = templates.get(subject, templates["Science"]) # Default to science for others

    for i in range(count):
        template = random.choice(sub_templates)
        # Fill placeholders
        import re
        matches = re.findall(r'\{(\w+)\}', template)
        filled = template
        for m in matches:
            if m in placeholders:
                filled = filled.replace(f"{{{m}}}", random.choice(placeholders[m]))
        
        diff = random.choice(["Easy", "Medium", "Hard"])
        
        # Structure
        q = {
            "question_text": filled,
            "subject": subject,
            "grade": grade,
            "difficulty": diff,
            "chapter": f"Chapter {random.randint(1, 15)}",
            "is_rationalised": True
        }
        questions.append(q)
        
    return questions

def run_boost():
    all_q = []
    
    # Class 9 (All)
    subjects_9 = ["Maths", "Science", "Social Science", "English", "Hindi", "Sanskrit"]
    for s in subjects_9:
        all_q.extend(generate_questions(9, s, 550))
        
    # Class 10 (Maths, Science)
    for s in ["Maths", "Science"]:
        all_q.extend(generate_questions(10, s, 550))
        
    # Class 11-12 (Maths, Physics, Chemistry)
    for g in [11, 12]:
        for s in ["Maths", "Physics", "Chemistry"]:
            all_q.extend(generate_questions(g, s, 550))
            
    print(f"Generated {len(all_q)} total questions.")
    
    # Save in chunks to avoid single massive file issues
    chunk_size = 1000
    for i in range(0, len(all_q), chunk_size):
        chunk = all_q[i:i + chunk_size]
        filename = f"seed_boost_{i//chunk_size}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=4)
        print(f"  Saved {filename}")

if __name__ == "__main__":
    run_boost()
