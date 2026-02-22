
import json
import random

# ============ VERIX CHAPTER → BRANCH/AREA MAPPINGS ============

SCIENCE_BRANCH_MAP = {
    "Motion": "Physics",
    "Force and Laws of Motion": "Physics",
    "Gravitation": "Physics",
    "Work and Energy": "Physics",
    "Sound": "Physics",
    "Matter in Our Surroundings": "Chemistry",
    "Is Matter Around Us Pure": "Chemistry",
    "Atoms and Molecules": "Chemistry",
    "Structure of the Atom": "Chemistry",
    "The Fundamental Unit of Life": "Biology",
    "Tissues": "Biology",
    "Improvement in Food Resources": "Biology",
    "Natural Resources": "Biology"
}

MATHS_WEIGHTAGE_MAP = {
    "Number Systems": "Number Systems",
    "Polynomials": "Algebra",
    "Coordinate Geometry": "Coordinate Geometry",
    "Linear Equations in Two Variables": "Algebra",
    "Introduction to Euclids Geometry": "Geometry",
    "Lines and Angles": "Geometry",
    "Triangles": "Geometry",
    "Quadrilaterals": "Geometry",
    "Circles": "Geometry",
    "Constructions": "Geometry",
    "Herons Formula": "Mensuration",
    "Heron's Formula": "Mensuration",
    "Surface Areas and Volumes": "Mensuration",
    "Statistics": "Statistics & Probability",
    "Probability": "Statistics & Probability"
}

SST_WEIGHTAGE_MAP = {
    "The French Revolution": "History",
    "Socialism in Europe and the Russian Revolution": "History",
    "Nazism and the Rise of Hitler": "History",
    "Forest Society and Colonialism": "History",
    "India Size and Location": "Geography",
    "Physical Features of India": "Geography",
    "Drainage": "Geography",
    "Climate": "Geography",
    "Natural Vegetation and Wildlife": "Geography",
    "Population": "Geography",
    "What is Democracy Why Democracy": "Political Science",
    "Constitutional Design": "Political Science",
    "Electoral Politics": "Political Science",
    "Working of Institutions": "Political Science",
    "Democratic Rights": "Political Science",
    "Democracy in the Contemporary World": "Political Science",
    "The Story of Village Palampur": "Economics",
    "People as Resource": "Economics",
    "Poverty as a Challenge": "Economics",
    "Food Security in India": "Economics"
}

# ============ SECTION BLUEPRINTS (CBSE 2025-26) ============

SECTION_BLUEPRINTS = {
    "Science": [
        {"section": "A", "marks": 1, "difficulty": "Easy",   "count_weight": 20, "word_limit": None},
        {"section": "B", "marks": 2, "difficulty": "Easy",   "count_weight": 6,  "word_limit": "30-50 words"},
        {"section": "C", "marks": 3, "difficulty": "Medium", "count_weight": 7,  "word_limit": "50-80 words"},
        {"section": "D", "marks": 5, "difficulty": "Hard",   "count_weight": 3,  "word_limit": "80-120 words"},
        {"section": "E", "marks": 4, "difficulty": "Hard",   "count_weight": 3,  "word_limit": None}
    ],
    "Maths": [
        {"section": "A", "marks": 1, "difficulty": "Easy",   "count_weight": 20, "word_limit": None},
        {"section": "B", "marks": 2, "difficulty": "Easy",   "count_weight": 5,  "word_limit": None},
        {"section": "C", "marks": 3, "difficulty": "Medium", "count_weight": 6,  "word_limit": None},
        {"section": "D", "marks": 5, "difficulty": "Hard",   "count_weight": 4,  "word_limit": None},
        {"section": "E", "marks": 4, "difficulty": "Hard",   "count_weight": 3,  "word_limit": None}
    ],
    "Social Science": [
        {"section": "A", "marks": 1, "difficulty": "Easy",   "count_weight": 20, "word_limit": None},
        {"section": "B", "marks": 2, "difficulty": "Easy",   "count_weight": 4,  "word_limit": "40 words"},
        {"section": "C", "marks": 3, "difficulty": "Medium", "count_weight": 5,  "word_limit": "60 words"},
        {"section": "D", "marks": 5, "difficulty": "Hard",   "count_weight": 4,  "word_limit": "120 words"},
        {"section": "E", "marks": 4, "difficulty": "Hard",   "count_weight": 3,  "word_limit": None},
        {"section": "F", "marks": 5, "difficulty": "Medium", "count_weight": 1,  "word_limit": None}
    ],
    "English": [
        {"section": "A", "marks": 1, "difficulty": "Easy",   "count_weight": 20, "word_limit": None},
        {"section": "B", "marks": 2, "difficulty": "Medium", "count_weight": 5,  "word_limit": None},
        {"section": "C", "marks": 3, "difficulty": "Medium", "count_weight": 6,  "word_limit": "40-50 words"},
        {"section": "D", "marks": 5, "difficulty": "Hard",   "count_weight": 2,  "word_limit": "100-120 words"}
    ]
}

# ============ CHAPTER LISTS PER SUBJECT ============

CHAPTERS = {
    "Maths": [
        "Number Systems", "Polynomials", "Coordinate Geometry",
        "Linear Equations in Two Variables", "Introduction to Euclids Geometry",
        "Lines and Angles", "Triangles", "Quadrilaterals", "Circles",
        "Herons Formula", "Surface Areas and Volumes", "Statistics", "Probability"
    ],
    "Science": [
        "Matter in Our Surroundings", "Is Matter Around Us Pure",
        "Atoms and Molecules", "Structure of the Atom",
        "The Fundamental Unit of Life", "Tissues", "Motion",
        "Force and Laws of Motion", "Gravitation", "Work and Energy",
        "Sound", "Improvement in Food Resources", "Natural Resources"
    ],
    "Social Science": [
        "The French Revolution", "Socialism in Europe and the Russian Revolution",
        "Nazism and the Rise of Hitler", "Forest Society and Colonialism",
        "India Size and Location", "Physical Features of India", "Drainage",
        "Climate", "Natural Vegetation and Wildlife", "Population",
        "What is Democracy Why Democracy", "Constitutional Design",
        "Electoral Politics", "Working of Institutions", "Democratic Rights",
        "The Story of Village Palampur", "People as Resource",
        "Poverty as a Challenge", "Food Security in India"
    ],
    "English": [
        "The Fun They Had", "The Sound of Music", "The Little Girl",
        "A Truly Beautiful Mind", "The Snake and the Mirror",
        "My Childhood", "Reach for the Top", "Kathmandu",
        "If I Were You", "The Road Not Taken", "Wind", "Rain on the Roof",
        "The Lake Isle of Innisfree", "A Legend of the Northland",
        "The Lost Child", "The Adventures of Toto",
        "Iswaran the Storyteller", "In the Kingdom of Fools",
        "The Happy Prince", "Weathering the Storm in Ersama",
        "Grammar", "Reading Comprehension", "Writing Skills"
    ],
    "Hindi": [
        "Kshitij", "Sparsh", "Kritika", "Sanchayan", "Hindi Vyakaran"
    ],
    "Sanskrit": [
        "Shemushi", "Vyakaranam", "Abhyasvaani"
    ]
}

# ============ QUESTION TEMPLATES ============

TEMPLATES = {
    "Maths": {
        "A": [
            "The value of {expr} is: (A) {a} (B) {b} (C) {c} (D) {d}",
            "If {cond}, then {var} is: (A) {a} (B) {b} (C) {c} (D) {d}",
            "Which of the following is {prop}? (A) {a} (B) {b} (C) {c} (D) {d}",
            "The number of {item} is: (A) {a} (B) {b} (C) {c} (D) {d}"
        ],
        "B": [
            "Find the value of {expr}.",
            "If {cond}, find {var}.",
            "Write {item} in simplest form."
        ],
        "C": [
            "Prove that {statement}.",
            "Find the area of {shape} with {dimensions}. Show all steps.",
            "Solve for x and y: {eq1} and {eq2}."
        ],
        "D": [
            "Prove the {theorem}. [Image: https://dummyimage.com/600x400/000/fff&text=Geometry_Proof]",
            "A {shape} has {property}. Find (a) {part1} [2] (b) {part2} [3]. Draw a neat diagram.",
            "State and prove {theorem}. Also find {application}."
        ],
        "E": [
            "A school is planning a garden in the shape of a {shape}. {context} Based on the above: (i) Find {q1} [1] (ii) Find {q2} [1] (iii) Find {q3} [2]",
            "The following data shows {data_desc}. {context} Answer: (i) {q1} [1] (ii) {q2} [1] (iii) {q3} [2]"
        ]
    },
    "Science": {
        "A": [
            "The {property} of {substance} is: (A) {a} (B) {b} (C) {c} (D) {d}",
            "Which of the following is {classification}? (A) {a} (B) {b} (C) {c} (D) {d}",
            "The SI unit of {quantity} is: (A) {a} (B) {b} (C) {c} (D) {d}"
        ],
        "B": [
            "Define {term}. Give one example.",
            "Differentiate between {term1} and {term2}.",
            "State {law} in your own words."
        ],
        "C": [
            "Explain the process of {process} with a suitable example.",
            "Derive the relation {formula}. State the assumptions.",
            "What happens when {condition}? Explain with reasons."
        ],
        "D": [
            "Draw a neat labelled diagram of {structure} and explain its function. [Image: https://dummyimage.com/600x400/000/fff&text={slug}]",
            "Explain {concept} in detail. Draw a diagram to support your answer. [Image: https://dummyimage.com/600x400/000/fff&text={slug}]",
            "State {law}. Derive {formula}. Draw the relevant force diagram. [Image: https://dummyimage.com/600x400/000/fff&text=Force_Diagram]"
        ],
        "E": [
            "{passage} Based on the above passage, answer: (i) {q1} [1] (ii) {q2} [1] (iii) {q3} [2]"
        ]
    },
    "Social Science": {
        "A": [
            "The {event} occurred in the year: (A) {a} (B) {b} (C) {c} (D) {d}",
            "Which of the following is {classification}? (A) {a} (B) {b} (C) {c} (D) {d}",
            "{person} is associated with: (A) {a} (B) {b} (C) {c} (D) {d}"
        ],
        "B": [
            "Define {term} in about 40 words.",
            "What is the significance of {event}?",
            "Name two {category}."
        ],
        "C": [
            "Explain the causes of {event}. Write in about 60 words.",
            "Describe the role of {factor} in {context}.",
            "Compare {topic1} and {topic2}."
        ],
        "D": [
            "Critically examine {concept}. (a) {part1} [2] (b) {part2} [2] (c) {part3} [1]",
            "Discuss the impact of {event} on {area}. Write in about 120 words.",
            "Explain {policy} with examples."
        ],
        "E": [
            "{passage} Based on the above passage, answer: (i) {q1} [1] (ii) {q2} [1] (iii) {q3} [2]"
        ],
        "F": [
            "On the given outline map of India, identify and mark:\nA. {history_item1} (History) [1]\nB. {history_item2} (History) [1]\nC. {geo_item1} (Geography) [1]\nD. {geo_item2} (Geography) [1]\nE. {geo_item3} (Geography) [1]\n[Image: https://dummyimage.com/600x400/000/fff&text=India_Outline_Map]"
        ]
    }
}

# ============ PLACEHOLDER VALUES ============

PLACEHOLDERS = {
    "expr": ["√2 + √3", "(27)^(1/3)", "x² - 9 when x=3", "sin 30° + cos 60°"],
    "cond": ["x + y = 10 and x - y = 4", "the angles of a triangle are in ratio 1:2:3", "AB ∥ CD"],
    "var": ["x", "y", "the angle", "the length"],
    "prop": ["a rational number", "an irrational number", "a polynomial", "a linear equation"],
    "item": ["diagonals of a rectangle", "solutions", "zeroes of the polynomial", "vertices"],
    "a": ["1", "2", "3", "4", "9", "16", "25", "36"],
    "b": ["5", "6", "7", "8", "27", "64", "81", "100"],
    "c": ["9", "10", "11", "12", "0", "√2", "π", "∞"],
    "d": ["13", "14", "15", "16", "None of these", "-1", "1/2", "2√3"],
    "statement": ["the sum of angles of a triangle is 180°", "vertically opposite angles are equal"],
    "shape": ["triangle", "parallelogram", "circle", "trapezium", "rhombus"],
    "dimensions": ["sides 5cm, 12cm, 13cm", "radius 7cm", "base 10cm and height 8cm"],
    "eq1": ["2x + 3y = 12", "x + y = 7"],
    "eq2": ["x - y = 2", "3x - 2y = 4"],
    "theorem": ["Mid-point Theorem", "Pythagoras Theorem", "Isosceles Triangle Theorem", "Angle Bisector Theorem"],
    "property": ["boiling point", "atomic number", "SI unit", "chemical formula", "molecular mass"],
    "substance": ["water", "iron", "carbon dioxide", "sodium chloride", "ethanol"],
    "classification": ["an element", "a compound", "a mixture", "a Kharif crop", "a tissue"],
    "quantity": ["force", "energy", "work", "power", "pressure", "momentum"],
    "term": ["osmosis", "force", "inertia", "acceleration", "valency", "isotope", "tissue"],
    "term1": ["compound and mixture", "element and compound", "distance and displacement"],
    "term2": ["", "", ""],
    "law": ["Newton's First Law", "Law of Conservation of Mass", "Archimedes' Principle"],
    "process": ["photosynthesis", "evaporation", "distillation", "chromatography", "osmosis"],
    "formula": ["v = u + at", "s = ut + ½at²", "F = ma", "KE = ½mv²"],
    "condition": ["ice is heated", "a force is applied to a stationary body", "two solutions are mixed"],
    "structure": ["Animal Cell", "Plant Cell", "Nephron", "Atom (Bohr Model)", "Neuron"],
    "slug": ["Animal_Cell", "Plant_Cell", "Nephron", "Bohr_Model", "Neuron"],
    "concept": ["Newton's Third Law", "Law of Conservation of Energy", "Structure of Atom"],
    "passage": ["Read the following passage carefully and answer the questions that follow."],
    "q1": ["What is the main idea?", "Identify the key term.", "Define the concept."],
    "q2": ["Why is this significant?", "Name the process.", "What is the unit?"],
    "q3": ["Explain in detail with reasons.", "Draw and label.", "Calculate and show working."],
    "event": ["French Revolution", "Russian Revolution", "Green Revolution", "Industrial Revolution"],
    "person": ["Napoleon", "Robespierre", "Lenin", "Mahatma Gandhi", "Nelson Mandela"],
    "factor": ["geography", "climate", "trade", "agriculture"],
    "context": ["Indian economy", "European history", "democratic governance"],
    "topic1": ["Himalayan rivers", "democracy", "constitutional design"],
    "topic2": ["Peninsular rivers", "dictatorship", "unwritten constitution"],
    "policy": ["NREGA", "Public Distribution System", "Right to Education"],
    "area": ["society", "economy", "politics", "governance"],
    "part1": ["Causes [2]", "Who led this? [1]"],
    "part2": ["Effects [2]", "What policies? [2]"],
    "part3": ["Significance [1]", "Impact [1]"],
    "category": ["Fundamental Rights", "types of democracy", "river systems of India"],
    "history_item1": ["Location where the Bastille was stormed", "Centre of the Russian Revolution"],
    "history_item2": ["Route of Napoleon's army", "City where the Bolsheviks seized power"],
    "geo_item1": ["River Ganga", "Western Ghats", "Thar Desert"],
    "geo_item2": ["River Krishna", "Chilika Lake", "Sundarbans Delta"],
    "geo_item3": ["Tropic of Cancer", "Standard Meridian", "Highest rainfall area"],
    "data_desc": ["marks obtained by students", "rainfall in different cities"],
    "part1": ["the perimeter", "the area", "the volume"],
    "part2": ["the diagonal", "the height", "the surface area"]
}


def get_branch_or_area(subject, chapter):
    """Get the sub_branch or weightage_area for a chapter."""
    if subject == "Science":
        return SCIENCE_BRANCH_MAP.get(chapter, random.choice(["Physics", "Chemistry", "Biology"]))
    elif subject == "Maths":
        return MATHS_WEIGHTAGE_MAP.get(chapter, random.choice(list(MATHS_WEIGHTAGE_MAP.values())))
    elif subject == "Social Science":
        return SST_WEIGHTAGE_MAP.get(chapter, random.choice(["History", "Geography", "Political Science", "Economics"]))
    return None


def should_require_diagram(subject, section, chapter):
    """Determine if a question should have diagram_required based on Verix constraints."""
    if subject == "Science" and section == "D":
        return True
    if subject == "Maths" and section == "D":
        area = MATHS_WEIGHTAGE_MAP.get(chapter, "")
        return area in ["Geometry", "Mensuration"]
    if subject == "Social Science" and section == "F":
        return True
    return False


def fill_template(template):
    """Fill placeholders in a template with random values."""
    import re
    matches = re.findall(r'\{(\w+)\}', template)
    filled = template
    for m in matches:
        if m in PLACEHOLDERS:
            filled = filled.replace(f"{{{m}}}", random.choice(PLACEHOLDERS[m]), 1)
    return filled


def generate_questions(grade, subject, count=500):
    questions = []
    chapters = CHAPTERS.get(subject, ["General"])
    blueprints = SECTION_BLUEPRINTS.get(subject, SECTION_BLUEPRINTS["Science"])
    subject_templates = TEMPLATES.get(subject, {})

    # Calculate weights for section distribution
    total_weight = sum(bp["count_weight"] for bp in blueprints)

    for i in range(count):
        # Pick section based on weighted distribution
        bp = random.choices(blueprints, weights=[bp["count_weight"] for bp in blueprints], k=1)[0]
        section = bp["section"]
        marks = bp["marks"]
        difficulty = bp["difficulty"]
        word_limit = bp["word_limit"]

        # Pick chapter
        chapter = random.choice(chapters)

        # Get branch/area
        branch_or_area = get_branch_or_area(subject, chapter)

        # Diagram check
        diagram_required = should_require_diagram(subject, section, chapter)

        # Generate question text from templates
        section_templates = subject_templates.get(section, None)
        if section_templates:
            template = random.choice(section_templates)
            question_text = fill_template(template)
        else:
            # Fallback for subjects without full templates
            question_text = f"[{subject}] [{chapter}] Section {section} question worth {marks} mark(s)."

        # Build the question object with Verix audit fields
        q = {
            "question_text": question_text,
            "subject": subject,
            "grade": grade,
            "chapter": chapter,
            "difficulty": difficulty,
            "section": section,
            "marks": marks,
            "is_rationalised": True,
            "diagram_required": diagram_required
        }

        # Add optional Verix fields
        if word_limit:
            q["word_limit"] = word_limit

        if subject == "Science":
            q["sub_branch"] = branch_or_area
        elif subject in ["Maths", "Social Science"]:
            q["weightage_area"] = branch_or_area

        questions.append(q)

    return questions


def run_boost():
    all_q = []

    # Class 9 — All subjects
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

    # Save in chunks
    chunk_size = 1000
    for i in range(0, len(all_q), chunk_size):
        chunk = all_q[i:i + chunk_size]
        filename = f"seed_boost_{i // chunk_size}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=4, ensure_ascii=False)
        print(f"  Saved {filename}")


if __name__ == "__main__":
    run_boost()
