from sqlalchemy import Column, Integer, String, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Tabela de Cursos
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    level = Column(String(50))
    structure = Column(JSON)  # módulos serão armazenados em JSON

    modules = relationship("Module", back_populates="course")


# Tabela de Módulos
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    title = Column(String(255))
    content = Column(Text)            # conteúdo do módulo
    resources = Column(JSON)          # imagens, pdfs, links etc
    quiz = Column(JSON)               # questões geradas pela IA

    course = relationship("Course", back_populates="modules")


# Tabela de Progresso do Aluno
class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    course_id = Column(Integer)
    module_index = Column(Integer, default=0)
    score = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
