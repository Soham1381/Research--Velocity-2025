import os, json, arxiv, gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Auth Logic (GitHub Secrets or Local)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_raw = os.environ.get("GOOGLE_CREDENTIALS")
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_raw), scope)
client = gspread.authorize(creds)
sheet = client.open("Humanoid-Robotics-Data-2025").sheet1

# 2. Search Logic (Robotics Niche)
# Hustler: Update these keywords monthly
keywords = 'ti:"sim-to-real" OR ti:"humanoid" OR ti:"actuator"'
search = arxiv.Search(query=keywords, max_results=20, sort_by=arxiv.SortCriterion.SubmittedDate)

# 3. Filtering & Uploading
for paper in search.results():
    # Signal if a Big Tech/AI lab is mentioned in the summary
    labs = ["Tesla", "Figure", "Boston Dynamics", "OpenAI", "DeepMind", "NVIDIA"]
    is_corp = any(lab.lower() in paper.summary.lower() for lab in labs)
    
    row = [str(paper.published.date()), paper.title, paper.authors[0].name, str(is_corp), paper.summary[:200], paper.pdf_url]
    sheet.append_row(row)
print("Data harvest complete.")
