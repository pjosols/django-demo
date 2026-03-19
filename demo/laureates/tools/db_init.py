from pymongo import MongoClient


def create_indexes(db):
    try:
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

    except Exception as e:
        import traceback
        print(f"Error creating indexes: {e}")
        print(traceback.format_exc())


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", default="mongodb://localhost:27017/")
    args = parser.parse_args()
    client = MongoClient(args.uri)
    create_indexes(client['nobel_demo'])


if __name__ == "__main__":
    main()
