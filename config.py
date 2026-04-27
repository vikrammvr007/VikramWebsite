import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY   = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-production")
ADMIN_EMAIL  = os.getenv("ADMIN_EMAIL", "vhbrosis@gmail.com")
