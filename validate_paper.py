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
    
    for subj_name, subj in schema["subjects"].items():
        total = sum(sec.get("total_marks", sec.get("marks_per_q", 0) * sec.get("count", 0)) for sec in subj["sections"] if "total_marks" in sec)
        if total == 0:
            # Fallback: compute from marks_per_q * count
            total = sum(sec.get("marks_per_q", 0) * sec.get("count", 0) for sec in subj["sections"])
        
        # Check total marks
        if subj_name != "English":  # English has sub-sections
            expected_marks = subj["max_marks"]
            if total != expected_marks:
                errors.append(f"  ❌ {subj_name}: Section marks sum to {total}, expected {expected_marks}")
            else:
                print(f"  ✅ {subj_name}: Marks total = {total}/{expected_marks}")
        else:
            print(f"  ✅ {subj_name}: Complex structure (sub-sections), manual check needed")
        
        # Check total questions
        total_q = sum(sec.get("count", 0) for sec in subj["sections"])
        expected_q = subj["total_questions"]
        if subj_name not in ["English", "Hindi", "Sanskrit"]:
            if total_q != expected_q:
                errors.append(f"  ❌ {subj_name}: Question count = {total_q}, expected {expected_q}")
            else:
                print(f"  ✅ {subj_name}: Question count = {total_q}/{expected_q}")
        
        # Check weightage sums
        if "weightage" in subj:
            w_total = sum(subj["weightage"].values())
            if w_total != expected_marks:
                errors.append(f"  ❌ {subj_name}: Weightage sum = {w_total}, expected {expected_marks}")
            else:
                print(f"  ✅ {subj_name}: Weightage sum = {w_total}/{expected_marks}")
    
    return errors


def validate_seed_data(schema, questions):
    """Validate that seed data has the required Verix fields."""
    print("\n" + "=" * 60)
    print("  SEED DATA VALIDATION")
    print("=" * 60)
    errors = []
    warnings = []
    
    total = len(questions)
    with_section = sum(1 for q in questions if "section" in q)
    with_marks = sum(1 for q in questions if "marks" in q)
    with_diagram = sum(1 for q in questions if "diagram_required" in q)
    with_branch = sum(1 for q in questions if "sub_branch" in q or "weightage_area" in q)
    
    print(f"  Total questions: {total}")
    print(f"  With section:    {with_section} ({100*with_section//max(total,1)}%)")
    print(f"  With marks:      {with_marks} ({100*with_marks//max(total,1)}%)")
    print(f"  With diagram:    {with_diagram} ({100*with_diagram//max(total,1)}%)")
    print(f"  With branch/area:{with_branch} ({100*with_branch//max(total,1)}%)")
    
    if with_section < total * 0.5:
        warnings.append(f"  ⚠️  Only {with_section}/{total} questions have 'section' field")
    if with_marks < total * 0.5:
        warnings.append(f"  ⚠️  Only {with_marks}/{total} questions have 'marks' field")
    
    # Per-subject breakdown
    subjects = {}
    for q in questions:
        s = q.get("subject", "Unknown")
        if s not in subjects:
            subjects[s] = {"total": 0, "sections": {}}
        subjects[s]["total"] += 1
        sec = q.get("section", "?")
        subjects[s]["sections"][sec] = subjects[s]["sections"].get(sec, 0) + 1
    
    print(f"\n  Subject Breakdown:")
    for s, data in sorted(subjects.items()):
        sec_str = ", ".join(f"{k}:{v}" for k, v in sorted(data["sections"].items()))
        print(f"    {s}: {data['total']} total | Sections: {sec_str}")
    
    # Validate Science has sub_branch
    science_q = [q for q in questions if q.get("subject") == "Science"]
    if science_q:
        with_branch_sci = sum(1 for q in science_q if "sub_branch" in q)
        if with_branch_sci < len(science_q) * 0.5:
            warnings.append(f"  ⚠️  Science: Only {with_branch_sci}/{len(science_q)} have sub_branch (Physics/Chemistry/Biology)")
        else:
            branches = {}
            for q in science_q:
                b = q.get("sub_branch", "Unknown")
                branches[b] = branches.get(b, 0) + 1
            print(f"\n  Science Sub-Branches: {branches}")
    
    # Validate diagram_required in Science Sec D
    sci_d = [q for q in science_q if q.get("section") == "D"]
    sci_d_diag = sum(1 for q in sci_d if q.get("diagram_required"))
    if sci_d and sci_d_diag < len(sci_d):
        warnings.append(f"  ⚠️  Science Sec D: {sci_d_diag}/{len(sci_d)} have diagram_required=true (expected all)")
    elif sci_d:
        print(f"  ✅ Science Sec D: All {len(sci_d)} questions require diagrams")
    
    return errors, warnings


def validate_paper_simulation(schema, questions):
    """Simulate paper generation and check it matches the blueprint."""
    print("\n" + "=" * 60)
    print("  PAPER SIMULATION VALIDATION")
    print("=" * 60)
    errors = []
    
    for subj_name in ["Science", "Maths", "Social Science"]:
        subj_schema = schema["subjects"].get(subj_name)
        if not subj_schema:
            continue
        
        subj_q = [q for q in questions if q.get("subject") == subj_name and q.get("grade", 9) == 9]
        
        if not subj_q:
            errors.append(f"  ❌ {subj_name}: No grade 9 questions found in seed data")
            continue
        
        print(f"\n  --- {subj_name} ---")
        total_marks = 0
        total_questions = 0
        
        for sec in subj_schema["sections"]:
            sec_id = sec["id"]
            count_needed = sec.get("count", 0)
            marks_per = sec.get("marks_per_q", 0)
            
            available = [q for q in subj_q if q.get("section") == sec_id]
            
            if count_needed > 0 and len(available) < count_needed:
                errors.append(f"  ❌ {subj_name} Sec {sec_id}: Need {count_needed} but only {len(available)} available")
            elif count_needed > 0:
                print(f"  ✅ Sec {sec_id}: {len(available)} available (need {count_needed}) — {marks_per}m × {count_needed} = {marks_per * count_needed}m")
                total_marks += marks_per * count_needed
                total_questions += count_needed
        
        print(f"  📊 Total: {total_questions} questions, {total_marks} marks (target: {subj_schema['max_marks']})")
    
    return errors


def main():
    print("\n🔍 VERIX AUDIT ENGINE — VALIDATION REPORT")
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
        print(f"\n  ⚠️  {len(all_warnings)} Warning(s):")
        for w in all_warnings:
            print(w)
    
    if all_errors:
        print(f"\n  ❌ {len(all_errors)} Error(s):")
        for e in all_errors:
            print(e)
        print("\n  STATUS: FAIL ❌")
        sys.exit(1)
    else:
        print(f"\n  ✅ All checks passed!")
        print("  STATUS: PASS ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
