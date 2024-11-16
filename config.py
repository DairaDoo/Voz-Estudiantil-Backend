import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('postgresql://postgres.auqgonswvvsvdakrwsga:voz_estudiantil_password@aws-0-us-west-1.pooler.supabase.com:6543/postgres')
