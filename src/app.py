"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
   "Clube de Xadrez": {
      "description": "Aprenda estratégias e participe de torneios de xadrez",
      "schedule": "Sextas, 15h30 - 17h",
      "max_participants": 12,
      "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
   },
   "Aula de Programação": {
      "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
      "schedule": "Terças e quintas, 15h30 - 16h30",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
   },
   "Educação Física": {
      "description": "Educação física e atividades esportivas",
      "schedule": "Segundas, quartas e sextas, 14h - 15h",
      "max_participants": 30,
      "participants": ["john@mergington.edu", "olivia@mergington.edu"]
   },
   "Voleibol Competitivo": {
      "description": "Treinos e jogos de voleibol para todos os níveis",
      "schedule": "Segundas e quartas, 16h - 17h30",
      "max_participants": 16,
      "participants": []
   },
   "Atletismo de Pista": {
      "description": "Corrida, salto e arremesso com foco em performance atlética",
      "schedule": "Terças e quintas, 16h - 17h",
      "max_participants": 18,
      "participants": []
   },
   "Coral Escolar": {
      "description": "Prática vocal coletiva e apresentações musicais",
      "schedule": "Terças, 17h - 18h30",
      "max_participants": 20,
      "participants": []
   },
   "Teatro e Expressão": {
      "description": "Oficina de atuação, improviso e criação de peças",
      "schedule": "Quintas, 17h - 18h30",
      "max_participants": 18,
      "participants": []
   },
   "Clube de Robótica": {
      "description": "Projetos de robótica e programação de sistemas autônomos",
      "schedule": "Segundas e sextas, 15h - 16h30",
      "max_participants": 15,
      "participants": []
   },
   "Clube de Debate": {
      "description": "Desenvolva pensamento crítico e oratória em debates temáticos",
      "schedule": "Quartas, 17h - 18h",
      "max_participants": 14,
      "participants": []
   }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate duplicate registration
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Estudante já inscrito")

    # Validate quota
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Vagas esgotadas")

    # Add student
    activity["participants"].append(email)
    return {"message": f"{email} inscrito(a) em {activity_name} com sucesso"}
