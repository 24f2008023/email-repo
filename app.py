from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

students = []
with open(r'C:\Users\zahbi\Downloads\q-fastapi.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        students.append({"studentId": int(row["studentId"]), "class": row["class"]})

@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    if class_:
        return {"students": [s for s in students if s["class"] in class_]}
    return {"students": students}

