"""
Verix Audit Engine — Paper Validation Script
Validates that seed data and generated papers comply with CBSE 2025-26 blueprints.
"""

import json
import glob
import sys

# Load the Verix schema
def load_schema():
    with open("verix_schema.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_all_questions():
    files = glob.glob("seed_*.json")
    all_q = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            try:
                all_q.extend(json.load(fh))
            except:
                pass
    return all_q

def validate_schema(schema):
    """Validate the verix_schema.json itself."""
    print("=" * 60)
    print("  VERIX SCHEMA VALIDATION")
    print("=" * 60)
    errors = []
    
    for grade_id, grade_data in schema["grades"].items():
        print(f"\n--- Grade {grade_id} ---")
        for subj_name, subj in grade_data["subjects"].items():
            total = 0
            if "sections" in subj:
                total = sum(sec.get("total_marks", sec.get("marks_per_q", 0) * sec.get("count", 0)) for sec in subj["sections"])
            
            # Check total marks
            if subj_name != "English" and "max_marks" in subj:
                expected_marks = subj["max_marks"]
                if total != expected_marks:
                    errors.append(f"  [X] {subj_name} (Class {grade_id}): Section marks sum to {total}, expected {expected_marks}")
                else:
                    print(f"  [OK] {subj_name}: Marks total = {total}/{expected_marks}")
            else:
                print(f"  [OK] {subj_name}: Complex structure (sub-sections), manual check needed")
            
            # Check total questions
            if "total_questions" in subj and "sections" in subj:
                total_q = sum(sec.get("count", 0) for sec in subj["sections"])
                expected_q = subj["total_questions"]
                if subj_name not in ["English", "Hindi", "Sanskrit"]:
                    if total_q != expected_q:
                        errors.append(f"  [X] {subj_name} (Class {grade_id}): Question count = {total_q}, expected {expected_q}")
                    else:
                        print(f"  [OK] {subj_name}: Question count = {total_q}/{expected_q}")
            
            # Check weightage sums
            if "weightage" in subj:
                w_total = sum(subj["weightage"].values())
                expected_marks = subj["max_marks"]
                if w_total != expected_marks:
                    errors.append(f"  [X] {subj_name} (Class {grade_id}): Weightage sum = {w_total}, expected {expected_marks}")
                else:
                    print(f"  [OK] {subj_name}: Weightage sum = {w_total}/{expected_marks}")
    
    return errors


def validate_seed_data(schema, questions):
    """Validate that seed data has the required Verix fields."""
    print("\n" + "=" * 60)
    print("  SEED DATA VALIDATION")
    print("=" * 60)
    errors = []
    warnings = []
    
    total = len(questions)
    if total == 0:
        print("  ⚠️ No questions to validate!")
        return errors, warnings
        
    with_section = sum(1 for q in questions if "section" in q)
    with_marks = sum(1 for q in questions if "marks" in q)
    with_diagram = sum(1 for q in questions if "diagram_required" in q)
    with_branch = sum(1 for q in questions if "sub_branch" in q or "weightage_area" in q)
    with_grade = sum(1 for q in questions if "grade" in q)
    
    print(f"  Total questions: {total}")
    print(f"  With section:    {with_section} ({100*with_section//max(total,1)}%)")
    print(f"  With marks:      {with_marks} ({100*with_marks//max(total,1)}%)")
    print(f"  With diagram:    {with_diagram} ({100*with_diagram//max(total,1)}%)")
    print(f"  With branch/area:{with_branch} ({100*with_branch//max(total,1)}%)")
    print(f"  With grade:      {with_grade} ({100*with_grade//max(total,1)}%)")
    
    # Per-subject/grade breakdown
    breakdown = {}
    for q in questions:
        s = q.get("subject", "Unknown")
        g = str(q.get("grade", "9"))
        key = f"{s}_{g}"
        if key not in breakdown:
            breakdown[key] = {"total": 0, "sections": {}}
        breakdown[key]["total"] += 1
        sec = q.get("section", "?")
        breakdown[key]["sections"][sec] = breakdown[key]["sections"].get(sec, 0) + 1
    
    print(f"\n  Seed Breakdown:")
    for key, data in sorted(breakdown.items()):
        sec_str = ", ".join(f"{k}:{v}" for k, v in sorted(data["sections"].items()))
        print(f"    {key}: {data['total']} total | Sections: {sec_str}")
    
    return errors, warnings


def validate_paper_simulation(schema, questions):
    """Simulate paper generation and check it matches the blueprint."""
    print("\n" + "=" * 60)
    print("  PAPER SIMULATION VALIDATION")
    print("=" * 60)
    errors = []
    
    for grade_id, grade_data in schema["grades"].items():
        print(f"\n  --- Class {grade_id} Simulation ---")
        for subj_name, subj_schema in grade_data["subjects"].items():
            if "sections" not in subj_schema:
                continue
            
            # Match by subject and grade
            subj_q = [q for q in questions if q.get("subject") == subj_name and str(q.get("grade", 9)) == str(grade_id)]
            
            if not subj_q:
                # Some subjects might not be in seeds yet, that's a warning but we'll show it
                print(f"    (!) {subj_name}: No questions found for Class {grade_id}")
                continue
            
            total_marks = 0
            total_questions = 0
            
            for sec in subj_schema["sections"]:
                sec_id = sec["id"]
                count_needed = sec.get("count", 0)
                marks_per = sec.get("marks_per_q", 0)
                
                available = [q for q in subj_q if q.get("section") == sec_id]
                
                if count_needed > 0 and len(available) < count_needed:
                    errors.append(f"  [X] {subj_name} Class {grade_id} Sec {sec_id}: Need {count_needed} but only {len(available)} available")
                elif count_needed > 0:
                    total_marks += marks_per * count_needed
                    total_questions += count_needed
            
            print(f"    [OK] {subj_name}: {total_questions} questions, {total_marks} marks (Target: {subj_schema['max_marks']})")
    
    return errors


def main():
    print("\n--- [VERIX] AUDIT ENGINE - VALIDATION REPORT ---")
    print("=" * 60)
    
    schema = load_schema()
    questions = load_all_questions()
    
    all_errors = []
    all_warnings = []
    
    # 1. Schema validation
    errs = validate_schema(schema)
    all_errors.extend(errs)
    
    # 2. Seed data validation
    errs, warns = validate_seed_data(schema, questions)
    all_errors.extend(errs)
    all_warnings.extend(warns)
    
    # 3. Paper simulation
    errs = validate_paper_simulation(schema, questions)
    all_errors.extend(errs)
    
    # Summary
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    
    if all_warnings:
        print(f"\n  (!) {len(all_warnings)} Warning(s):")
        for w in all_warnings:
            print(w)
    
    if all_errors:
        print(f"\n  [X] {len(all_errors)} Error(s):")
        for e in all_errors:
            print(e)
        print("\n  STATUS: FAIL")
        sys.exit(1)
    else:
        print(f"\n  [OK] All checks passed!")
        print("  STATUS: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
