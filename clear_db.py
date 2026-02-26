import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: Supabase URL or Key not found in environment variables.")
    print("Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in your .env file or environment.")
    exit(1)

client = create_client(url, key)

print("Connecting to Supabase...")
try:
    # Delete everything where ID is not a dummy UUID (which means it targets all rows)
    response = client.table("class9_question_bank").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"Successfully wiped {len(response.data)} rows from 'class9_question_bank'.")
except Exception as e:
    print(f"Failed to clear database: {e}")
