import os
import json
import time
from openai import OpenAI

# Verify OpenAI API Key is present
if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: Please set your OPENAI_API_KEY environment variable.")
    exit(1)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Blueprint to guide the AI
BLUEPRINTS = {
    "Science": {
        "chapters": ["Chemical Reactions and Equations", "Acids Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds", "Life Processes", "Control and Coordination", "How do Organisms Reproduce", "Heredity", "Our Environment", "Light Reflection and Refraction", "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current"],
        "sections": [
            {"section": "A", "marks": 1, "type": "Multiple Choice Questions", "difficulty": "Easy/Medium"},
            {"section": "B", "marks": 2, "type": "Very Short Answer (30-50 words)", "difficulty": "Medium"},
            {"section": "C", "marks": 3, "type": "Short Answer (50-80 words)", "difficulty": "Medium/Hard"},
            {"section": "D", "marks": 5, "type": "Long Answer (100-120 words)", "difficulty": "Hard", "diagram_required": True},
            {"section": "E", "marks": 4, "type": "Case Study Based", "difficulty": "Hard"}
        ]
    },
    "Maths": {
        "chapters": ["Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions", "Triangles", "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry", "Circles", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"],
        "sections": [
            {"section": "A", "marks": 1, "type": "Multiple Choice Questions", "difficulty": "Easy/Medium"},
            {"section": "B", "marks": 2, "type": "Very Short Answer", "difficulty": "Medium"},
            {"section": "C", "marks": 3, "type": "Short Answer", "difficulty": "Medium/Hard"},
            {"section": "D", "marks": 5, "type": "Long Answer", "difficulty": "Hard", "diagram_required": True},
            {"section": "E", "marks": 4, "type": "Case Study Based", "difficulty": "Hard"}
        ]
    }
}

SYSTEM_PROMPT = """You are an expert CBSE Class 10 exam setter.
I need you to generate highly accurate, real Board-level (PYQ style) questions.
You must return the output STRICTLY as a raw JSON array of objects. Do not include markdown blocks like ```json.
Each question object MUST precisely follow this schema:
{
    "question_text": "The full text of the question (Include MCQ options as (A) ... (B) ... (C) ... (D) ... inline if it's 1 mark. For physics/biology diagrams use [Image: https://dummyimage.com/600x400/000/fff&text=Topic_Name])",
    "subject": "Maths or Science",
    "grade": 10,
    "chapter": "Exact chapter name",
    "difficulty": "Easy, Medium, or Hard",
    "section": "A, B, C, D, or E",
    "marks": integer,
    "is_rationalised": true,
    "diagram_required": boolean,
    "weightage_area": "Physics, Chemistry, Biology, Algebra, Geometry, Trigonometry, etc. (Depending on the chapter)",
    "answer": "A short answer key or hint."
}
Make the questions realistic, challenging, and varied."""

def generate_questions_for_chapter(subject, chapter, section_info):
    prompt = f"Generate 5 unique, real CBSE-level Class 10 {subject} questions for the chapter '{chapter}'.\n"
    prompt += f"Target Section: {section_info['section']} ({section_info['marks']} marks). Question Type: {section_info['type']}.\n"
    prompt += "Provide real scenarios, numericals, or theoretical questions as appropriate."
    
    print(f"  -> Requesting {subject} | {chapter} | Section {section_info['section']}...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        
        # Clean up potential markdown formatting if the AI disobeys
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"     [!] Failed to generate/parse for {chapter}: {e}")
        return []

def main():
    print("=============================================")
    print(" VERIX AI QUESTION HUNTER (CBSE Class 10)")
    print("=============================================\n")
    
    all_generated_questions = []
    
    total_subjects = list(BLUEPRINTS.keys())
    
    for subject in total_subjects:
        print(f"\n--- Processing Subject: {subject} ---")
        chapters = BLUEPRINTS[subject]["chapters"]
        sections = BLUEPRINTS[subject]["sections"]
        
        # For demonstration and speed, we will pick 3 random chapters per subject
        # To scale up, you can loop through all chapters.
        # This will quickly generate 30 high-quality questions for now.
        import random
        sample_chapters = random.sample(chapters, min(3, len(chapters)))
        
        for chapter in sample_chapters:
            print(f"\n[Chapter: {chapter}]")
            for section in sections:
                # Ask AI for questions in this section for this chapter
                questions = generate_questions_for_chapter(subject, chapter, section)
                all_generated_questions.extend(questions)
                time.sleep(1) # Protect against rate limits
                
    output_filename = "seed_ai_generated.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_generated_questions, f, indent=4)
        
    print(f"\n✅ Successfully generated {len(all_generated_questions)} hyper-realistic questions!")
    print(f"📂 Saved to {output_filename}")
    print(f"\nTo sync these to your live database, run:")
    print(f"  py sync_to_supabase.py")

if __name__ == "__main__":
    main()
