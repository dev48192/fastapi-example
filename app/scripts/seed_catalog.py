# scripts/seed_catalog.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))) 

from sqlalchemy.orm import Session
from datetime import datetime
from app.db import SessionLocal
from app.models import CatalogItem

def seed_catalog_items():
    db: Session = SessionLocal()

    catalog_items = [
        {
            "name": "Cement",
            "type": "Material",
            "unit": "bags",
            "description": "Standard cement used for construction."
        },
        {
            "name": "Bricks",
            "type": "Material",
            "unit": "pieces",
            "description": "Red clay bricks for building walls."
        },
        {
            "name": "Electrical Wiring",
            "type": "Material",
            "unit": "meters",
            "description": "Insulated copper wires for household or industrial use."
        },
        {
            "name": "Civil Contracting",
            "type": "Service",
            "unit": None,
            "description": "End-to-end civil engineering and construction services."
        },
        {
            "name": "Plumbing",
            "type": "Service",
            "unit": None,
            "description": "Residential and commercial plumbing services."
        },
        {
            "name": "Iron Rods",
            "type": "Material",
            "unit": "kg",
            "description": "TMT rods used for reinforcement in concrete."
        },
    ]

    for item in catalog_items:
        exists = db.query(CatalogItem).filter_by(name=item["name"], type=item["type"]).first()
        if not exists:
            db.add(CatalogItem(
                name=item["name"],
                type=item["type"],
                unit=item["unit"],
                description=item["description"],
            ))

    db.commit()
    db.close()
    print("✅ Catalog items with unit and description seeded successfully.")

if __name__ == "__main__":
    seed_catalog_items()
