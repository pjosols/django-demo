#!/usr/bin/env python3
"""
Seed MongoDB with Nobel Prize laureate data from data/laureates.json.

Usage:
    python seed_data.py
    python seed_data.py --connection mongodb://username:password@host:port/
"""

import argparse
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "laureates.json")


def create_indexes(db):
    col = db["laureates"]
    col.create_index([
        ("name",          "text"),
        ("birth_country", "text"),
        ("category",      "text"),
        ("motivation",    "text"),
    ])
    for field in ("name", "birth_country", "year", "category", "gender", "share"):
        col.create_index(field)
    print("Indexes created.")


def seed(connection_string="mongodb://localhost:27017/"):
    from pymongo import MongoClient

    if not os.path.exists(DATA_PATH):
        raise SystemExit(
            f"Data file not found: {DATA_PATH}\n"
            "Run fetch_nobel.py first to generate it."
        )

    with open(DATA_PATH, encoding="utf-8") as f:
        laureates = json.load(f)

    print(f"Loaded {len(laureates)} records from {DATA_PATH}")

    client = MongoClient(connection_string)
    db = client["nobel_demo"]

    print("Dropping existing collection...")
    db.drop_collection("laureates")

    result = db["laureates"].insert_many(laureates)
    print(f"Inserted {len(result.inserted_ids)} records")

    print("Creating indexes...")
    create_indexes(db)

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MongoDB with Nobel Prize data")
    parser.add_argument("--connection", default="mongodb://localhost:27017/",
                        help="MongoDB connection string (default: mongodb://localhost:27017/)")
    args = parser.parse_args()
    seed(args.connection)
