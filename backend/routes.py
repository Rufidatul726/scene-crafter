from fastapi import FastAPI
import json
from functions import analyze_project

app = FastAPI()

@app.get("/analyze_project")
async def analyze_project_endpoint():
    project_context = analyze_project("E:\DownloadsEdge\everrage-main\everrage-main")
    # Store context for future API calls
    with open("project_context.json", "w") as f:
        json.dump(project_context, f)
    return {"status": "Project analyzed successfully"}