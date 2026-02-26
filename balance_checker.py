"""
VERIX BALANCE CHECKER
Prints a full inventory of the class9_question_bank and flags
which question types need more questions for blueprint compliance.
"""
import os
import logging
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger("BalanceChecker")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_KEY"]

# Minimum required counts per (subject_keyword, marks, question_type_keyword)
# Based on CBSE blueprint * 10x buffer for randomisation
TARGETS = {
    # Science
    ("science", 1, None):           300,  # Section A MCQs
    ("science", 2, None):            90,  # Section B
    ("science", 3, None):           105,  # Section C
    ("science", 5, None):            45,  # Section D
    ("science", 4, "case"):          45,  # Section E
    # Math
    ("math", 1, None):              300,
    ("math", 2, None):               90,
    ("math", 3, None):               90,
    ("math", 5, None):               60,
    ("math", 4, "case"):             45,
    # SST
    ("social", 1, None):            300,
    ("social", 3, None):             60,
    ("social", 5, None):             45,
    ("social", 4, "case"):           45,
    ("social", None, "map"):         15,
    # English
    ("english", None, "reading"):    30,
    ("english", None, "writing"):    20,
    ("english", None, "grammar"):    50,
    ("english", None, "literature"): 40,
}


def get_count(sb: Client, subject: str, marks=None, qtype=None) -> int:
    q = sb.table("class9_question_bank").select("id", count="exact")
    q = q.ilike("subject", f"%{subject}%")
    if marks is not None:
        q = q.eq("marks", marks)
    if qtype is not None:
        q = q.ilike("question_type", f"%{qtype}%")
    res = q.execute()
    return res.count or 0


def main():
    sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("\n" + "=" * 70)
    print("  VERIX DATABASE INVENTORY REPORT")
    print("=" * 70)
    print(f"{'BUCKET':<45} {'HAVE':>6} {'NEED':>6} {'STATUS':>10}")
    print("-" * 70)

    needs = []
    for (subject, marks, qtype), target in TARGETS.items():
        count = get_count(sb, subject, marks, qtype)
        label_parts = [subject.upper()]
        if marks:
            label_parts.append(f"{marks}-mark")
        if qtype:
            label_parts.append(qtype)
        label = " ".join(label_parts)
        status = "✅ OK" if count >= target else "🚨 LOW"
        if count < target:
            needs.append((subject, marks, qtype, count, target))
        print(f"  {label:<43} {count:>6} {target:>6} {status:>10}")

    print("=" * 70)
    if needs:
        print("\n⚠️  PRIORITY HUNTING LIST (sorted by deficit):")
        needs.sort(key=lambda x: x[3] - x[4])  # sort by deficit ascending
        for subject, marks, qtype, have, need in needs:
            deficit = need - have
            marks_str = f"{marks}-mark " if marks else ""
            qtype_str = qtype or "any-type"
            print(f"   → {subject.upper()} {marks_str}{qtype_str}: need {deficit} more (have {have}/{need})")
        print("\nRun pdf_shredder.py targeting the above subjects to fix imbalances.\n")
    else:
        print("\n✅ All buckets are at or above target. Database is balanced!\n")

    # Log counts as JSON for CI parsing
    log.info("Balance check complete. %d buckets below target.", len(needs))


if __name__ == "__main__":
    main()
