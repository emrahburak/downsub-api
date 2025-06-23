# config.py
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()

if ENVIRONMENT == "docker":
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
else:
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


print(f"[config] Environment: {ENVIRONMENT}, OUTPUT_DIR: {OUTPUT_DIR}")
