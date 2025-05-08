# create_table.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add project root to path

from app.db import engine, Base  # Adjusted to the correct import path
import app.models  # Import models to register them

def init():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init()
