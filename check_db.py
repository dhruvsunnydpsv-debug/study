import os
from supabase import create_client, Client

url = "https://wfegooasrtbhpursgcvh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"

supabase: Client = create_client(url, key)

try:
    # Test Master Table
    res = supabase.table("class9_question_bank").select("subject", count="exact").limit(1).execute()
    print(f"Master Table Rows (Sample): {res.data}")
    
    # Test a Virtual View (Directly testing Directive V3.0 logic)
    print("\nTesting View access (Directive V3.1 Audit):")
    view_res = supabase.table("view_science_1_markers").select("*").limit(5).execute()
    print(f"Science View Data: {view_res.data}")

except Exception as e:
    print(f"\n[!] ACCESS ERROR: {e}")
    if "403" in str(e) or "not found" in str(e).lower():
        print("ACTION REQUIRED: Supabase is blocking public access to Views. Run the GRANT SELECT script in SQL Editor.")
