from sqlalchemy import Column, ForeignKey, Integer, String, Text

from backend.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    target_country = Column(String, nullable=False)
    major = Column(String, nullable=False)
    basic_info = Column(Text, nullable=False)


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic = Column(String, nullable=False)
    transcription = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
