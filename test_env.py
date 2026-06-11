from dotenv import load_dotenv
import os

load_dotenv()

print("Database:", os.getenv("POSTGRES_DB"))
print("User:", os.getenv("POSTGRES_USER"))
print("Host:", os.getenv("POSTGRES_HOST"))