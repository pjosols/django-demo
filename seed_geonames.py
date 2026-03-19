#!/usr/bin/env python3
"""
Download and seed MongoDB with GeoNames allCountries data (~12M records).

Usage:
    python seed_geonames.py                           # seed from existing allCountries.txt
    python seed_geonames.py --download                # download first, then seed
    python seed_geonames.py --connection mongodb://username:password@host:port/
"""

import argparse
import os
import urllib.request
import zipfile

DATA_DIR  = os.path.join(os.path.dirname(__file__), "data")
ZIP_PATH  = os.path.join(DATA_DIR, "allCountries.zip")
TXT_PATH  = os.path.join(DATA_DIR, "allCountries.txt")
ZIP_URL   = "https://download.geonames.org/export/dump/allCountries.zip"
BATCH     = 10_000

# Columns in the TSV (0-indexed)
# 0  geonameid
# 1  name
# 2  asciiname          <- skip
# 3  alternatenames     <- skip (large)
# 4  latitude
# 5  longitude
# 6  feature_class      <- skip
# 7  feature_code
# 8  country_code
# 9  cc2                <- skip
# 10 admin1_code
# 11 admin2_code        <- skip
# 12 admin3_code        <- skip
# 13 admin4_code        <- skip
# 14 population
# 15 elevation          <- skip
# 16 dem                <- skip
# 17 timezone
# 18 modification_date  <- skip


def _progress(count, block_size, total):
    mb_done  = count * block_size / 1_048_576
    mb_total = total / 1_048_576
    print(f"\r  {mb_done:.0f} / {mb_total:.0f} MB", end="", flush=True)


def download(skip=False):
    os.makedirs(DATA_DIR, exist_ok=True)
    if skip and os.path.exists(TXT_PATH):
        print(f"Using existing {TXT_PATH}")
        return
    if not os.path.exists(ZIP_PATH):
        print(f"Downloading {ZIP_URL} ...")
        urllib.request.urlretrieve(ZIP_URL, ZIP_PATH, reporthook=_progress)
        print()
    if not os.path.exists(TXT_PATH):
        print("Extracting zip ...")
        with zipfile.ZipFile(ZIP_PATH) as z:
            z.extract("allCountries.txt", DATA_DIR)
        print("Extracted.")


def parse_row(parts):
    def _int(v):
        try:
            return int(v)
        except (ValueError, TypeError):
            return None

    def _float(v):
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    return {
        "geonameid":    _int(parts[0]),
        "name":         parts[1],
        "latitude":     _float(parts[4]),
        "longitude":    _float(parts[5]),
        "feature_code": parts[7],
        "country_code": parts[8],
        "admin1_code":  parts[10] or None,
        "population":   _int(parts[14]),
        "timezone":     parts[17] or None,
    }


def create_indexes(col):
    from pymongo import TEXT, ASCENDING
    col.create_index(
        [("name", TEXT), ("feature_code", TEXT), ("timezone", TEXT)],
        weights={"name": 10, "feature_code": 3, "timezone": 1},
        name="name_text",
    )
    for field in ("name", "country_code", "feature_code",
                  "population", "timezone", "admin1_code"):
        col.create_index(field)
    print("Indexes created.")


def seed(connection_string="mongodb://localhost:27017/", do_download=False):
    from pymongo import MongoClient

    download(skip=not do_download)

    client = MongoClient(connection_string)
    col = client["geonames_demo"]["places"]

    print("Dropping existing collection ...")
    col.drop()

    total = 0
    batch = []

    print("Inserting records (population > 0 only) ...")
    with open(TXT_PATH, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 19:
                continue
            try:
                if int(parts[14]) <= 0:
                    continue
            except (ValueError, TypeError):
                continue
            batch.append(parse_row(parts))
            if len(batch) >= BATCH:
                col.insert_many(batch, ordered=False)
                total += len(batch)
                batch = []
                print(f"\r  {total:,} records inserted", end="", flush=True)

    if batch:
        col.insert_many(batch, ordered=False)
        total += len(batch)

    print(f"\r  {total:,} records inserted")
    print("Creating indexes ...")
    create_indexes(col)
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MongoDB with GeoNames data")
    parser.add_argument("--connection",     default="mongodb://localhost:27017/",
                        help="MongoDB connection string")
    parser.add_argument("--download", action="store_true",
                        help="Download allCountries.zip before seeding")
    args = parser.parse_args()
    seed(args.connection, do_download=args.download)
