"""
Models do banco de dados usando SQLAlchemy.
Define as tabelas: users, courses, modules, progress.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DECIMAL, DateTime,
    ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# ============================================================
# 1. MODEL: USER
# ============================================================

class User(Base):
    __tablename__ = "users"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    password_hash = Column(String(255))
    avatar_url = Column(Text)

    # OAuth
    google_id = Column(String(255), unique=True)
    linkedin_id = Column(String(255), unique=True)

    # Gamificação
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    badges = Column(JSONB, default=[])
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True))

    # Preferências
    preferred_topics = Column(JSONB, default=[])
    learning_style = Column(String(50))  # visual, practical, theoretical

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relacionamentos
    progress = relationship("Progress", back_populates="user")

    # Constraints
    __table_args__ = (
        CheckConstraint('level >= 1 AND level <= 100', name='valid_level'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


# ============================================================
# 2. MODEL: COURSE
# ============================================================

class Course(Base):
    __tablename__ = "courses"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)

    # Classificação
    level = Column(String(50), nullable=False)
    category = Column(String(100))
    tags = Column(JSONB, default=[])

    # Informações do curso
    duration_hours = Column(Integer, nullable=False)
    modules_count = Column(Integer, default=0)
    prerequisites = Column(JSONB, default=[])
    learning_outcomes = Column(JSONB, default=[])

    # Estrutura IA
    structure = Column(JSONB, nullable=False)

    # Status
    status = Column(String(50), default='draft')
    is_public = Column(Boolean, default=False)

    # Autoria
    created_by = Column(String(255))

    # Metadados IA
    generated_by = Column(JSONB)
    generation_time_seconds = Column(Integer)
    ai_quality_score = Column(DECIMAL(3, 1))

    # Estatísticas
    total_enrollments = Column(Integer, default=0)
    average_completion_rate = Column(DECIMAL(5, 2), default=0.0)
    average_rating = Column(DECIMAL(3, 2), default=0.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))

    # Relacionamentos
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="course")

    # Constraints
    __table_args__ = (
        CheckConstraint("level IN ('basic', 'intermediate', 'advanced')", name='valid_level'),
        CheckConstraint("status IN ('draft', 'published', 'archived')", name='valid_status'),
        CheckConstraint('duration_hours > 0', name='valid_duration'),
        CheckConstraint('ai_quality_score >= 0 AND ai_quality_score <= 10', name='valid_quality_score'),
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}')>"


# ============================================================
# 3. MODEL: MODULE
# ============================================================

class Module(Base):
    __tablename__ = "modules"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    module_index = Column(Integer, nullable=False)

    # Infos básicas
    title = Column(String(255), nullable=False)
    description = Column(Text)
    duration_hours = Column(Integer, nullable=False)

    # Conteúdo
    content = Column(Text, nullable=False)

    # Recursos
    examples = Column(JSONB, default=[])
    exercises = Column(JSONB, default=[])
    resources = Column(JSONB, default={})

    # Quiz
    quiz = Column(JSONB, nullable=False)

    # Revisão IA
    review_score = Column(DECIMAL(3, 1))
    review_feedback = Column(JSONB)
    reviewed_by = Column(String(100))

    # Metadados IA
    generated_by = Column(String(100))
    generation_prompt = Column(Text)
    ai_model_used = Column(String(100))

    # Status
    is_published = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    course = relationship("Course", back_populates="modules")
    progress = relationship("Progress", back_populates="module")

    # Constraints
    __table_args__ = (
        CheckConstraint('duration_hours > 0', name='valid_module_duration'),
        CheckConstraint('review_score >= 0 AND review_score <= 10', name='valid_review_score'),
        CheckConstraint('module_index > 0', name='valid_module_index'),
    )

    def __repr__(self):
        return f"<Module(id={self.id}, title='{self.title}', course_id={self.course_id})>"


# ============================================================
# 4. MODEL: PROGRESS
# ============================================================

class Progress(Base):
    __tablename__ = "progress"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)

    # Status
    status = Column(String(50), default='not_started')

    # Tempo e datas
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    last_accessed_at = Column(DateTime(timezone=True))

    # Quiz
    quiz_attempts = Column(Integer, default=0)
    quiz_score = Column(Integer)
    quiz_passed = Column(Boolean, default=False)
    quiz_answers = Column(JSONB)
    quiz_completed_at = Column(DateTime(timezone=True))

    # Tutor IA
    tutor_analysis = Column(JSONB)

    # Tempo de estudo
    time_spent_minutes = Column(Integer, default=0)

    # Gamificação
    points_earned = Column(Integer, default=0)
    badges = Column(JSONB, default=[])

    # Exercícios
    exercises_completed = Column(Integer, default=0)
    exercises_total = Column(Integer, default=0)

    # Relacionamentos
    user = relationship("User", back_populates="progress")
    course = relationship("Course", back_populates="progress")
    module = relationship("Module", back_populates="progress")

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('not_started', 'in_progress', 'completed', 'failed')", name='valid_status'),
        CheckConstraint('quiz_score >= 0 AND quiz_score <= 100', name='valid_quiz_score'),
        CheckConstraint('quiz_attempts >= 0', name='valid_quiz_attempts'),
    )

    def __repr__(self):
        return f"<Progress(id={self.id}, user_id='{self.user_id}', status='{self.status}')>"
