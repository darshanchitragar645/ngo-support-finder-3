from flask import Flask, render_template, request, jsonify, g
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ngo_support_finder.db"

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g._database = db
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ngos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            cause TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            description TEXT NOT NULL,
            website TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            ngo TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    ngo_count = conn.execute("SELECT COUNT(*) FROM ngos").fetchone()[0]
    if ngo_count == 0:
        sample_ngos = [
            (
                "Hope for Children Foundation",
                "Education",
                "School kits and mentoring support",
                "Bengaluru, India",
                "Mr. Arun Nair",
                "hello@hopechildren.org",
                "+91 98765 43210",
                "Empowers children from underserved communities through education, mentoring, and digital access.",
                "https://hopechildren.org",
            ),
            (
                "GreenEarth Care",
                "Environment",
                "Tree plantation and waste management",
                "Pune, India",
                "Ms. Riya Sharma",
                "care@greenearth.org",
                "+91 99887 66554",
                "Supports climate action projects, urban gardening, and community recycling programs.",
                "https://greenearth.org",
            ),
            (
                "Women Rise Collective",
                "Women Empowerment",
                "Skill development and livelihood aid",
                "Delhi, India",
                "Ms. Nisha Verma",
                "support@womenrise.org",
                "+91 98111 22334",
                "Helps women entrepreneurs and rural women access training, micro-credit, and safe workplaces.",
                "https://womenrise.org",
            ),
            (
                "CareBridge Health Network",
                "Healthcare",
                "Medical outreach and health camps",
                "Hyderabad, India",
                "Dr. S. Kumar",
                "info@carebridgehealth.org",
                "+91 97654 11223",
                "Provides primary care, medicine support, and mobile health services for vulnerable families.",
                "https://carebridgehealth.org",
            ),
            (
                "Nourish Nation",
                "Food Security",
                "Emergency food support and nutrition",
                "Lucknow, India",
                "Mr. Amit Singh",
                "donate@nourishnation.org",
                "+91 98900 77445",
                "Delivers food packages, nutrition assistance, and community kitchen support to families in need.",
                "https://nourishnation.org",
            ),
            (
                "Shelter and Safe Homes",
                "Housing",
                "Temporary shelter and rehabilitation",
                "Mumbai, India",
                "Ms. Seema Iyer",
                "hello@shelterandsafehomes.org",
                "+91 98222 33110",
                "Provides emergency shelter, rehabilitation support, and essential household assistance to displaced families.",
                "https://shelterandsafehomes.org",
            ),
        ]

        conn.executemany(
            """
            INSERT INTO ngos (
                name, category, cause, location, contact, email, phone, description, website
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_ngos,
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/ngos")
def list_ngos():
    category = request.args.get("category", "All")
    search = (request.args.get("q", "") or "").strip()

    query = "SELECT * FROM ngos WHERE 1=1"
    params = []

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (name LIKE ? OR cause LIKE ? OR location LIKE ? OR category LIKE ?)"
        like_term = f"%{search}%"
        params.extend([like_term, like_term, like_term, like_term])

    query += " ORDER BY name ASC"

    rows = get_db().execute(query, params).fetchall()
    return jsonify({"ngos": [dict(row) for row in rows], "count": len(rows)})


@app.route("/api/requests", methods=["POST"])
def submit_support_request():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    ngo = (data.get("ngo") or "").strip()
    category = (data.get("category") or "").strip()
    message = (data.get("message") or "").strip()

    if not all([name, email, ngo, category, message]):
        return jsonify({"success": False, "message": "Please fill in all fields before submitting."}), 400

    db = get_db()
    db.execute(
        "INSERT INTO support_requests (name, email, ngo, category, message) VALUES (?, ?, ?, ?, ?)",
        (name, email, ngo, category, message),
    )
    db.commit()

    return jsonify({"success": True, "message": "Your support request has been submitted successfully."})


@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})


init_db()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)





















