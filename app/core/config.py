from dotenv import load_dotenv
import os

load_dotenv()

class Settings: 
    app_name = os.getenv("APP_NAME")
    database_url = os.getenv("DATABASE_URL","sqlite:///./user.db" )
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    cache_timeout = int(os.getenv("CACHE_TIMEOUT", 300))

settings = Settings()