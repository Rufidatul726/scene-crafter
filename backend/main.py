import asyncio
from flask import Flask
import json
from functions import analyze_project

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "status": "200",
        "body": "Hello world"
    }

@app.route("/analyze_project")
def analyze_project_endpoint():
    project_context = asyncio.run(analyze_project("E://DownloadsEdge//everrage-main//everrage-main"))

    with open("project_context.json", "w") as f:
        json.dump(project_context, f)
        
    return {"status": "Project analyzed successfully"}