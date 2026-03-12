from pathlib import Path
import shutil

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.ai_service import summarize_interview
from backend.database import SessionLocal, engine
from backend.models import Base, Interview, Student
from backend.speech_service import transcribe_audio
from backend.vector_store import add_memory

app = FastAPI(title="AI College Admissions Assistant MVP")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    frontend_file = Path("frontend/index.html")
    if frontend_file.exists():
        return FileResponse(frontend_file)
    return {"status": "ok", "message": "Frontend not found"}


@app.post("/student")
def create_student(
    name: str = Form(...),
    grade: str = Form(...),
    target_country: str = Form(...),
    major: str = Form(...),
    basic_info: str = Form(...),
):
    db: Session = SessionLocal()
    try:
        student = Student(
            name=name,
            grade=grade,
            target_country=target_country,
            major=major,
            basic_info=basic_info,
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        add_memory(student.id, basic_info)
        return {"status": "ok", "student_id": student.id}
    finally:
        db.close()


@app.post("/interview")
async def upload_interview(
    student_id: int = Form(...),
    topic: str = Form(...),
    audio: UploadFile = File(...),
):
    path = Path(f"temp_{audio.filename}")

    with path.open("wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    transcription = transcribe_audio(str(path))
    summary = summarize_interview(transcription)

    db = SessionLocal()
    try:
        interview = Interview(
            student_id=student_id,
            topic=topic,
            transcription=transcription,
            summary=summary,
        )

        db.add(interview)
        db.commit()

        add_memory(student_id, summary)

        return {"transcription": transcription, "summary": summary}
    finally:
        db.close()
        if path.exists():
            path.unlink()
