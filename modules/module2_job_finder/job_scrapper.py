import requests
from time import sleep
from datetime import datetime
from pymongo import MongoClient

# === Configuration ===
API_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Key": "5e52392064msh7bca40c300ae3b2p1f89edjsn59c83a4b877e",  # Replace this with your actual RapidAPI key
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # Adjust URI if needed
db = client["career_db"]
collection = db["jobs"]

def fetch_jobs(query, max_pages=1):
    jobs = []
    for page in range(1, max_pages + 1):
        params = {
            "query": query,
            "page": page,
            "remote_jobs_only": "false"
        }
        try:
            res = requests.get(API_URL, headers=HEADERS, params=params)
            res.raise_for_status()
            data = res.json()

            for job in data.get("data", []):
                job_doc = {
                    "title": job.get("job_title", ""),
                    "company": job.get("employer_name", ""),
                    "location": job.get("job_city", ""),
                    "url": job.get("job_apply_link", ""),
                    "job_description": job.get("job_description", "")[:500],
                    "fetched_at": datetime.utcnow()
                }
                jobs.append(job_doc)

        except Exception as e:
            print(f"❌ Error fetching '{query}' page {page}: {e}")
        sleep(1)
    return jobs

if __name__ == "__main__":
    all_jobs = []
    print("🔍 Fetching jobs from A to Z...")

    for letter in "abcdefghijklmnopqrstuvwxyz":
        print(f"📌 Query: '{letter}'")
        jobs = fetch_jobs(query=letter, max_pages=2)
        all_jobs.extend(jobs)

    # De-duplicate by URL
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        if job["url"] not in seen:
            unique_jobs.append(job)
            seen.add(job["url"])

    if unique_jobs:
        result = collection.insert_many(unique_jobs)
        print(f"✅ Inserted {len(result.inserted_ids)} unique jobs into MongoDB.")
    else:
        print("⚠️ No new jobs found.")