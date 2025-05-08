import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Add project root to path

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import CatalogItem, Brand, CatalogItemBrand

def seed_data():
    db: Session = SessionLocal()

    try:
        # Seed Brands
        brand_names = ["TATA", "Ambuja", "ACC", "Ultratech", "JSW"]
        brands = []
        for name in brand_names:
            brand = Brand(name=name)
            db.add(brand)
            brands.append(brand)

        # Seed Catalog Items
        catalog_items = [
            CatalogItem(name="Cement", description="Construction cement", unit="Bag"),
            CatalogItem(name="Steel Rod", description="High quality steel rod", unit="Kg"),
            CatalogItem(name="Sand", description="Fine river sand", unit="Cubic Feet"),
        ]
        for item in catalog_items:
            db.add(item)

        db.commit()

        # Map brands to catalog items (manually or by logic)
        cement = db.query(CatalogItem).filter_by(name="Cement").first()
        steel = db.query(CatalogItem).filter_by(name="Steel Rod").first()

        tata = db.query(Brand).filter_by(name="TATA").first()
        acc = db.query(Brand).filter_by(name="ACC").first()
        jsw = db.query(Brand).filter_by(name="JSW").first()
        ultratech = db.query(Brand).filter_by(name="Ultratech").first()

        catalog_brand_links = [
            CatalogItemBrand(catalog_item_id=cement.id, brand_id=acc.id),
            CatalogItemBrand(catalog_item_id=cement.id, brand_id=ultratech.id),
            CatalogItemBrand(catalog_item_id=steel.id, brand_id=jsw.id),
            CatalogItemBrand(catalog_item_id=steel.id, brand_id=tata.id),
        ]

        db.add_all(catalog_brand_links)
        db.commit()
        print("✅ Seed data inserted successfully.")

    except Exception as e:
        db.rollback()
        print("❌ Failed to seed data:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
