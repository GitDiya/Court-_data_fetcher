from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)

# ======================
# DATABASE INITIALIZATION
# ======================
conn = sqlite3.connect("court_cases.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS case_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_type TEXT,
    case_number TEXT,
    filing_year TEXT,
    raw_html TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()


# ======================
# SCRAPER FUNCTION
# ======================
def fetch_case_details(case_type, case_number, filing_year):
    base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
    session = requests.Session()

    try:
        search_url = base_url + "casestatus/case_number.php"
        payload = {
            "case_type": case_type,
            "case_number": case_number,
            "case_year": filing_year,
            "state_code": "6",  # Haryana state
            "dist_code": "2",   # Faridabad district
            "court_code": "1"   # Example court code
        }

        response = session.post(search_url, data=payload, timeout=15)

        if response.status_code != 200:
            return {"error": "Court server is not reachable. Try again later."}

        cursor.execute("INSERT INTO case_logs (case_type, case_number, filing_year, raw_html) VALUES (?, ?, ?, ?)",
                       (case_type, case_number, filing_year, response.text))
        conn.commit()

        soup = BeautifulSoup(response.text, "html.parser")

        parties = soup.find("div", {"id": "partyDetails"}).text.strip() if soup.find("div", {"id": "partyDetails"}) else "Not Available"
        filing_date = soup.find("span", {"id": "filingDate"}).text.strip() if soup.find("span", {"id": "filingDate"}) else "Not Available"
        next_hearing = soup.find("span", {"id": "nextHearing"}).text.strip() if soup.find("span", {"id": "nextHearing"}) else "Not Available"

        pdf_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".pdf")]
        if not pdf_links:
            pdf_links = []

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "pdf_links": pdf_links
        }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


# ======================
# FLASK ROUTES
# ======================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_number = request.form["case_number"]
        filing_year = request.form["filing_year"]

        result = fetch_case_details(case_type, case_number, filing_year)

        return render_template("result.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
