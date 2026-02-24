import os
from supabase import create_client, Client

url = "https://wfegooasrtbhpursgcvh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s"

supabase: Client = create_client(url, key)

try:
    res = supabase.table("class9_question_bank").select("subject", count="exact").execute()
    print(f"Total Rows: {res.count}")
    
    subjects = {}
    for row in res.data:
        s = row.get("subject")
        subjects[s] = subjects.get(s, 0) + 1
    print(f"Subjects: {subjects}")

except Exception as e:
    print(f"Error: {e}")
