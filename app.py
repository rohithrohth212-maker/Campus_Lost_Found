import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-only-change-me")

# Connect to MongoDB when a URI is available.
collection = None
mongo_uri = os.environ.get("MONGO_URI", "")

if mongo_uri:
    try:
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000
        )
        client.admin.command("ping")
        collection = client["campus_lost_found"]["items"]
        print("MongoDB connected successfully!")
    except PyMongoError as error:
        print("MongoDB connection failed:", error)

# Sample records for demo mode.
demo_items = [
    {
        "item_name": "Blue Water Bottle",
        "item_type": "Found",
        "category": "Bottle",
        "location": "Library",
        "description": "Found on a reading table.",
        "contact": "Contact campus office",
        "created_at": "Sample record"
    },
    {
        "item_name": "Engineering Notebook",
        "item_type": "Lost",
        "category": "Books",
        "location": "Classroom Block",
        "description": "Notebook with class notes.",
        "contact": "Contact campus office",
        "created_at": "Sample record"
    }
]


def get_items():
    if collection is not None:
        return list(
            collection.find({}, {"_id": 0})
            .sort("_id", -1)
            .limit(100)
        )
    return demo_items


@app.route("/")
def home():
    items = get_items()
    keyword = request.args.get("q", "").strip().lower()

    if keyword:
        items = [
            item for item in items
            if keyword in " ".join(
                str(item.get(field, ""))
                for field in [
                    "item_name", "item_type", "category",
                    "location", "description"
                ]
            ).lower()
        ]

    return render_template(
        "index.html",
        items=items,
        keyword=request.args.get("q", ""),
        db_connected=collection is not None
    )


@app.route("/add", methods=["POST"])
def add_item():
    item = {
        "item_name": request.form.get("item_name", "").strip(),
        "item_type": request.form.get("item_type", "").strip(),
        "category": request.form.get("category", "").strip(),
        "location": request.form.get("location", "").strip(),
        "description": request.form.get("description", "").strip(),
        "contact": request.form.get("contact", "").strip(),
        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
    }

    required = [
        "item_name", "item_type", "category",
        "location", "description", "contact"
    ]

    if any(not item[field] for field in required):
        flash("Please fill in every field.")
        return redirect(url_for("home"))

    if item["item_type"] not in ["Lost", "Found"]:
        flash("Please select Lost or Found.")
        return redirect(url_for("home"))

    if collection is not None:
        try:
            collection.insert_one(item)
            flash("Report saved to MongoDB successfully!")
        except PyMongoError:
            flash("Database save failed. Check the connection.")
    else:
        demo_items.insert(0, item)
        flash("Demo mode: report added temporarily, not saved permanently.")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
