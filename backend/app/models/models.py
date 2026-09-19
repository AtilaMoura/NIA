"""
Models do banco de dados usando SQLAlchemy.
Define as tabelas: users, courses, modules, lessons, lesson_completions, progress.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DECIMAL, DateTime,
    ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# ============================================================
# 1. MODEL: USER (INALTERADO)
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

    # Papel de acesso. 'admin' = compatibilidade com o front tech (frontend/, pausado);
    # 'master'/'professor' = governança do Emaús (FASE 1/5b do front de formação bíblica):
    # master controla tudo, admin tem menos alcance, professor é tutor de cursos específicos.
    role = Column(String(20), nullable=False, default='aluno')

    # Preferências
    preferred_topics = Column(JSONB, default=[])
    learning_style = Column(String(50))  # visual, practical, theoretical
    preferred_theme = Column(String(50), default='vidro-fume')  # id do tema em docs/schema/temas.json

    # Preferências do painel (Fase 4 do front) — eixo diferente de preferred_theme
    # acima (aquele é o tema do SLIDE da lição; estes são a moldura do app).
    preferred_mood = Column(String(20), nullable=False, default='musgo')
    preferred_panel_mode = Column(String(10), nullable=False, default='light')
    preferred_panel_layout = Column(String(20), nullable=False, default='retomar')
    preferred_font_size = Column(String(4))  # 'sm' | 'md' | 'lg' | None (FASE 4 do front Emaús; default de UI = 'md')

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relacionamentos
    progress = relationship("Progress", back_populates="user")
    # lesson_completions é definido pelo backref em LessonCompletion

    # Constraints
    __table_args__ = (
        CheckConstraint('level >= 1 AND level <= 100', name='valid_level'),
        CheckConstraint("role IN ('aluno', 'admin', 'master', 'professor')", name='valid_role'),
        CheckConstraint(
            "preferred_mood IN ('musgo', 'ambar', 'mare', 'framboesa', 'lavanda')",
            name='valid_preferred_mood',
        ),
        CheckConstraint("preferred_panel_mode IN ('light', 'dark')", name='valid_preferred_panel_mode'),
        CheckConstraint(
            "preferred_panel_layout IN ('retomar', 'biblioteca', 'trilha')",
            name='valid_preferred_panel_layout',
        ),
        CheckConstraint(
            "preferred_font_size IN ('sm', 'md', 'lg')",
            name='valid_preferred_font_size',
        ),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


# ============================================================
# 2. MODEL: COURSE (INALTERADO)
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

    # Identidade visual (2026-09-11) — paleta/estilo/mood reutilizados em toda
    # imagem do curso, escrita pelo ImagemAgent. cover_image_url é preenchida à
    # mão depois de rodar scripts/gerar_imagem_gemini.py (o agente só escreve o
    # prompt, quem gera a imagem de verdade é o script existente).
    identidade_visual = Column(JSONB)
    cover_image_url = Column(String(500))

    # Status
    status = Column(String(50), default='draft')
    is_public = Column(Boolean, default=False)

    # Governança de publicação (FASE 5b do front Emaús) — quem precisa aprovar antes de
    # `status` virar 'published'. Ver routers/governanca.py pra regra de cálculo.
    aprovacao_master_basta = Column(Boolean, nullable=False, default=False)
    aprovacao_exige_todos_tutores = Column(Boolean, nullable=False, default=False)

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
        CheckConstraint("level IN ('básico', 'intermediário', 'avançado', 'especialista')", name='valid_level'),
        CheckConstraint("status IN ('draft', 'published', 'archived')", name='valid_status'),
        CheckConstraint('duration_hours > 0', name='valid_duration'),
        CheckConstraint('ai_quality_score >= 0 AND ai_quality_score <= 10', name='valid_quality_score'),
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}')>"


# ============================================================
# 3. MODEL: MODULE (ATUALIZADO!)
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

    # Status de Geração (NOVOS CAMPOS)
    content_generated = Column(Boolean, default=False) # As aulas deste módulo já foram geradas? [cite: 3]
    exam_generated = Column(Boolean, default=False)    # A prova deste módulo já foi criada? [cite: 4]
    lessons_count = Column(Integer, default=0)         # Quantas aulas este módulo tem [cite: 5]

    # Conteúdo (Removido do Module para Lesson, mas mantido o Quiz para gabarito/metadados)
    quiz = Column(JSONB, nullable=True) # Mantido, mas agora armazena gabarito/metadados do quiz do módulo.

    # Recursos
    examples = Column(JSONB, default=[])
    exercises = Column(JSONB, default=[])
    resources = Column(JSONB, default={})

    # Capa do módulo (2026-09-11) — mesmo fluxo de Course.cover_image_url.
    cover_image_url = Column(String(500))

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
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan") # Relacionamento com nova tabela Lesson

    # Constraints
    __table_args__ = (
        CheckConstraint('duration_hours > 0', name='valid_module_duration'),
        CheckConstraint('review_score >= 0 AND review_score <= 10', name='valid_review_score'),
        CheckConstraint('module_index > 0', name='valid_module_index'),
    )

    def __repr__(self):
        return f"<Module(id={self.id}, title='{self.title}', course_id={self.course_id})>"


# ------------------------------------------------------------
# 3.1. MODEL: LESSON (NOVA!)
# ------------------------------------------------------------

class Lesson(Base):
    __tablename__ = "lessons"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, index=True)
    lesson_index = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)

    # Conteúdo e Metadados
    content = Column(Text) # O conteúdo completo da aula em Markdown [cite: 6]
    generated_by = Column(String(100)) # Nome do agent que gerou [cite: 6]
    reviewed_by = Column(String(100))  # Nome do agent que revisou [cite: 6]
    review_feedback = Column(JSONB)    # Feedback da revisão [cite: 6]
    is_approved = Column(Boolean, default=False) # Passou na revisão? [cite: 6]
    estimated_read_time_minutes = Column(Integer) # Tempo estimado de leitura [cite: 7]

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    module = relationship("Module", back_populates="lessons")
    completions = relationship("LessonCompletion", back_populates="lesson", cascade="all, delete-orphan") # NOVO
    topicos = relationship("Topico", back_populates="lesson", cascade="all, delete-orphan", order_by="Topico.topico_index")

    # Constraints
    __table_args__ = (
        CheckConstraint('lesson_index > 0', name='valid_lesson_index'),
    )

    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}', module_id={self.module_id})>"


# ------------------------------------------------------------
# 3.2. MODEL: TOPICO (NOVA! — 2026-08-26, nível Módulo→Aula→Tópicos)
# ------------------------------------------------------------
# Uma Lesson passa a representar a AULA (título, foco); cada Aula pode ter
# vários Tópicos, cada um com conteúdo/geração/revisão próprios (mesmo
# schema de slide que Lesson.content já usava quando 1 aula = 1 tópico só).
# Lesson.content não é apagado nem deixa de funcionar — fica como está pras
# aulas que não precisam desse nível extra (ex: cursos de tech já existentes).

class Topico(Base):
    __tablename__ = "topicos"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False, index=True)
    topico_index = Column(Integer, nullable=False)
    titulo = Column(String(255), nullable=False)
    referencia_biblica = Column(String(255))  # ex: "Rm 12:6-8" — nulo em domínios não-bíblicos

    # Conteúdo e Metadados (mesmo padrão de Lesson)
    content = Column(Text)
    generated_by = Column(String(100))
    reviewed_by = Column(String(100))
    review_feedback = Column(JSONB)
    is_approved = Column(Boolean, default=False)
    estimated_read_time_minutes = Column(Integer)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    lesson = relationship("Lesson", back_populates="topicos")

    # Constraints
    __table_args__ = (
        CheckConstraint('topico_index > 0', name='valid_topico_index'),
    )

    def __repr__(self):
        return f"<Topico(id={self.id}, titulo='{self.titulo}', lesson_id={self.lesson_id})>"


# ============================================================
# 4. MODEL: PROGRESS (ATUALIZADO!)
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

    # NOVOS CAMPOS DE PROGRESSO
    current_lesson_index = Column(Integer, default=1) # Qual aula está estudando [cite: 8]
    can_advance = Column(Boolean, default=False)      # Pode avançar para próximo módulo? [cite: 10]

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
        CheckConstraint('current_lesson_index >= 1', name='valid_current_lesson_index'), # NOVA
    )

    def __repr__(self):
        return f"<Progress(id={self.id}, user_id='{self.user_id}', status='{self.status}')>"


# ------------------------------------------------------------
# 5. MODEL: LESSON_COMPLETION (NOVA!)
# ------------------------------------------------------------

class LessonCompletion(Base):
    __tablename__ = "lesson_completions"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True) # ID do aluno
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False, index=True) # ID da aula

    # Status
    completed = Column(Boolean, default=False) # Completou?
    time_spent_minutes = Column(Integer, default=0) # Tempo gasto

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Relacionamentos
    user = relationship("User", backref="lesson_completions")
    lesson = relationship("Lesson", back_populates="completions")

    # Constraints
    __table_args__ = (
        CheckConstraint('time_spent_minutes >= 0', name='valid_time_spent'),
    )

    def __repr__(self):
        return f"<LessonCompletion(id={self.id}, user_id={self.user_id}, lesson_id={self.lesson_id})>"


# ------------------------------------------------------------
# 6. MODEL: TOPICO_PROGRESS (NOVA! — FASE 2 do front Emaús)
# ------------------------------------------------------------
# Progresso por TÓPICO. O model Progress existente é por MÓDULO e não serve
# pra granularidade de tópico que o front de formação bíblica precisa.
# Só upsert de status — nunca deleta (soft, padrão do projeto).

class TopicoProgress(Base):
    __tablename__ = "topico_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)

    status = Column(String(20), nullable=False, default='nao_iniciado')

    iniciado_em = Column(DateTime(timezone=True))    # 1ª vez que virou 'em_andamento'
    concluido_em = Column(DateTime(timezone=True))   # quando virou 'concluido' (não é limpo depois)
    time_spent_s = Column(Integer, default=0)        # reservado (FASE 3 popula)

    # Avaliação do Tutor por tópico (FASE 4 do front Emaús). É o análogo, por
    # TÓPICO, do Progress.tutor_analysis por MÓDULO — o Emaús navega por tópico e
    # não usa a gamificação que o fluxo de lição dispara.
    tutor_veredito = Column(String(10))              # 'dominado' | 'reforco' | None
    tutor_analise = Column(JSONB)                    # { ultima_avaliacao: {...}, historico: [...] }
    avaliado_em = Column(DateTime(timezone=True))    # última vez que o Tutor avaliou

    ultimo_slide = Column(Integer)  # índice do slide onde o aluno parou (2026-09-15)

    # "Rodada" de exercícios do tópico (2026-09-15) — separa avaliação real de
    # tentativa de teste/preview. Reiniciar incrementa isto; TopicoResposta
    # velho (rodada anterior) nunca é apagado, só some da tela por não ser mais
    # a rodada corrente. Ver POST /topico-progress/{id}/reiniciar.
    rodada_atual = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="topico_progress")
    topico = relationship("Topico", backref="progresso")

    __table_args__ = (
        CheckConstraint(
            "status IN ('nao_iniciado', 'em_andamento', 'concluido')",
            name='valid_topico_progress_status',
        ),
        CheckConstraint('time_spent_s >= 0', name='valid_topico_time_spent'),
        UniqueConstraint('user_id', 'topico_id', name='uq_topico_progress_user_topico'),
    )

    def __repr__(self):
        return f"<TopicoProgress(id={self.id}, user_id={self.user_id}, topico_id={self.topico_id}, status='{self.status}')>"


# ------------------------------------------------------------
# 7. MODEL: TOPICO_COMMENT (NOVA! — FASE 5a do front Emaús)
# ------------------------------------------------------------
# Anotação do revisor (master/admin/professor) por SLIDE do tópico — sincronizado
# com o <iframe> do render via postMessage. slide_index nulo = comentário geral do
# tópico, não de um slide específico. Sem DELETE (soft — padrão do projeto).

class TopicoComment(Base):
    __tablename__ = "topico_comments"

    id = Column(Integer, primary_key=True, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    slide_index = Column(Integer)              # null = comentário geral do tópico
    reacao = Column(String(10))                # 'positivo' | 'negativo' | None
    imagem_sugerida = Column(String(10))       # 'antes' | 'depois' | None — pedido de imagem nova
    sobre_imagem = Column(Boolean, default=False)  # comentário é sobre a imagem já presente no slide
    texto = Column(Text)                       # pode ser só reação, sem texto
    resolvido = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    topico = relationship("Topico", backref="comentarios")
    user = relationship("User", backref="comentarios_topico")

    __table_args__ = (
        CheckConstraint("reacao IN ('positivo', 'negativo')", name='valid_comment_reacao'),
        CheckConstraint("imagem_sugerida IN ('antes', 'depois')", name='valid_comment_imagem_sugerida'),
    )

    def __repr__(self):
        return f"<TopicoComment(id={self.id}, topico_id={self.topico_id}, user_id={self.user_id}, slide={self.slide_index})>"


# ------------------------------------------------------------
# 8. MODEL: TOPICO_CHECKLIST (NOVA! — FASE 5a do front Emaús)
# ------------------------------------------------------------
# O ato de aprovar/reprovar um tópico. 1 checklist por (tópico, revisor) — upsert,
# igual ao padrão do TopicoProgress. Topico.is_approved é recalculado a cada save
# (ver routers/revisao.py) — nesta fase, 1 aprovação de papel elevado já libera; a
# regra de quórum por curso (vários tutores, todos vs. um) é a FASE 5b.

class TopicoChecklist(Base):
    __tablename__ = "topico_checklists"

    id = Column(Integer, primary_key=True, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    profundidade = Column(String(20), nullable=False)     # 'raso' | 'adequado' | 'aprofundado'
    clareza = Column(String(20), nullable=False)           # 'confuso' | 'parcialmente_claro' | 'claro'
    qualidade_geral = Column(String(20), nullable=False)   # 'fraca' | 'regular' | 'boa' | 'excelente'
    observacao_final = Column(Text)
    aprovado = Column(Boolean, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    topico = relationship("Topico", backref="checklists")
    user = relationship("User", backref="checklists_topico")

    __table_args__ = (
        CheckConstraint(
            "profundidade IN ('raso', 'adequado', 'aprofundado')", name='valid_checklist_profundidade'
        ),
        CheckConstraint(
            "clareza IN ('confuso', 'parcialmente_claro', 'claro')", name='valid_checklist_clareza'
        ),
        CheckConstraint(
            "qualidade_geral IN ('fraca', 'regular', 'boa', 'excelente')",
            name='valid_checklist_qualidade',
        ),
        UniqueConstraint('topico_id', 'user_id', name='uq_topico_checklist_user_topico'),
    )

    def __repr__(self):
        return f"<TopicoChecklist(id={self.id}, topico_id={self.topico_id}, user_id={self.user_id}, aprovado={self.aprovado})>"


# ------------------------------------------------------------
# 9. MODEL: COURSE_TUTOR (NOVA! — FASE 5b do front Emaús)
# ------------------------------------------------------------
# Quais professores são tutores DESTE curso (de um pool de N professores
# cadastrados) — quem o master/admin atribui na tela de governança do curso.

class CourseTutor(Base):
    __tablename__ = "course_tutors"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", backref="tutores")
    user = relationship("User", backref="cursos_como_tutor")

    __table_args__ = (
        UniqueConstraint('course_id', 'user_id', name='uq_course_tutor'),
    )

    def __repr__(self):
        return f"<CourseTutor(course_id={self.course_id}, user_id={self.user_id})>"


# ------------------------------------------------------------
# 10. MODEL: COURSE_APROVACAO (NOVA! — FASE 5b do front Emaús)
# ------------------------------------------------------------
# O ato de aprovar/reprovar a PUBLICAÇÃO do curso inteiro — diferente de
# TopicoChecklist (aprova um tópico). 1 registro por (curso, revisor) — upsert.
# Quem pode registrar aqui: master, admin, ou professor que seja CourseTutor
# deste curso (ver routers/governanca.py).

class CourseAprovacao(Base):
    __tablename__ = "course_aprovacoes"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    papel_no_momento = Column(String(20), nullable=False)  # snapshot do role na hora de aprovar
    aprovado = Column(Boolean, nullable=False)
    observacao = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course = relationship("Course", backref="aprovacoes_publicacao")
    user = relationship("User", backref="aprovacoes_curso")

    __table_args__ = (
        UniqueConstraint('course_id', 'user_id', name='uq_course_aprovacao'),
    )

    def __repr__(self):
        return f"<CourseAprovacao(course_id={self.course_id}, user_id={self.user_id}, aprovado={self.aprovado})>"


# ------------------------------------------------------------
# 11b. MODEL: TOPICO_ANOTACAO (NOVA! — 2026-09-10)
# ------------------------------------------------------------
# Anotação PESSOAL do próprio aluno, por slide — diferente de TopicoComment
# (ferramenta do revisor/professor, FASE 5a). 1 anotação editável por
# (usuário, tópico, slide) — upsert, sem DELETE (padrão do projeto): esvaziar
# o texto some da UI (a lista ignora anotação com texto vazio), a linha fica.

class TopicoAnotacao(Base):
    __tablename__ = "topico_anotacoes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)
    slide_index = Column(Integer, nullable=False)

    texto = Column(Text, nullable=False, default='')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="anotacoes_topico")
    topico = relationship("Topico", backref="anotacoes")

    __table_args__ = (
        UniqueConstraint('user_id', 'topico_id', 'slide_index', name='uq_topico_anotacao_user_topico_slide'),
    )

    def __repr__(self):
        return f"<TopicoAnotacao(topico_id={self.topico_id}, user_id={self.user_id}, slide_index={self.slide_index})>"


# ------------------------------------------------------------
# 11. MODEL: TOPICO_RESPOSTA (NOVA! — 2026-09-09)
# ------------------------------------------------------------
# Resposta do ALUNO a 1 exercício (checkpoint/avaliação) dentro do render do
# tópico — hoje isso vivia só em JS na página e sumia ao recarregar. 1 linha
# por (usuário, tópico, pergunta) — upsert, sem DELETE (padrão do projeto).
# Granularidade por pergunta (não por gate/checkpoint inteiro) porque um
# checkpoint 'classify'/'associar' tem vários itens com id próprio.

class TopicoResposta(Base):
    __tablename__ = "topico_respostas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)

    gate_id = Column(String(50), nullable=False)      # ex: 'ck1', 'ef3' — agrupa pro checkGate()
    question_id = Column(String(50), nullable=False)  # ex: 'ck1_1', 'ef3_1_2' (item de classify)
    tipo = Column(String(20), nullable=False)          # mc|tf|classify|associar|lacuna|open|ditado

    resposta_dada = Column(JSONB, nullable=False)  # formato varia por tipo (índice, texto, bool...)
    correta = Column(Boolean)                       # null pra 'open' (sem gabarito automático)
    tentativas = Column(Integer, nullable=False, default=1)

    # Rodada do TopicoProgress.rodada_atual no momento em que foi respondida
    # (2026-09-15) — reiniciar o tópico incrementa a rodada corrente e essa
    # resposta antiga fica pra trás (nunca apagada, só não é mais a exibida).
    rodada = Column(Integer, nullable=False, default=1)

    respondido_em = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="respostas_topico")
    topico = relationship("Topico", backref="respostas")

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('mc', 'tf', 'classify', 'associar', 'lacuna', 'open', 'ditado')",
            name='valid_topico_resposta_tipo',
        ),
        UniqueConstraint(
            'user_id', 'topico_id', 'question_id', 'rodada',
            name='uq_topico_resposta_user_topico_question_rodada',
        ),
    )

    def __repr__(self):
        return f"<TopicoResposta(topico_id={self.topico_id}, user_id={self.user_id}, question_id='{self.question_id}', correta={self.correta})>"


# ------------------------------------------------------------
# 11b. MODEL: TOPICO_DUVIDA (NOVA! — 2026-09-19)
# ------------------------------------------------------------
# Pergunta que o aluno tira ao vivo, dentro do render do tópico, sobre um
# ponto específico (slide ou pergunta de exercício) — separada de propósito
# de TopicoAnotacao (anotação é o aluno anotando algo por conta própria;
# aqui é o aluno perguntando e a IA respondendo na hora). Ver
# [[nia-correcao-ia-avaliacoes]] na memória do projeto pro desenho completo.

class TopicoDuvida(Base):
    __tablename__ = "topico_duvidas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)
    slide_index = Column(Integer, nullable=False)
    question_id = Column(String(50))  # opcional — se a dúvida foi tirada em cima de um exercício específico

    pergunta_aluno = Column(Text, nullable=False)
    resposta_ia = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="duvidas_topico")
    topico = relationship("Topico", backref="duvidas")

    def __repr__(self):
        return f"<TopicoDuvida(topico_id={self.topico_id}, user_id={self.user_id}, slide_index={self.slide_index})>"


# ------------------------------------------------------------
# 11c. MODEL: TOPICO_REFORCO (NOVA! — 2026-09-19)
# ------------------------------------------------------------
# Pergunta NOVA gerada pela IA quando o aluno erra um exercício — mesmo
# schema de "Pergunta" (docs/schema/schema-conteudo-topico.md), guardado como
# JSONB porque o tipo (mc/tf/lacuna/etc.) varia. 1 linha por tentativa de
# reforço, nunca sobrescreve — permite reforço em cadeia (errou nova, gera
# outra) e dá material pro mapeamento de "onde o aluno mais errou" depois.

class TopicoReforco(Base):
    __tablename__ = "topico_reforcos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    topico_id = Column(Integer, ForeignKey('topicos.id', ondelete='CASCADE'), nullable=False, index=True)
    question_id_origem = Column(String(50), nullable=False)  # a pergunta original que o aluno errou

    correcao_personalizada = Column(Text, nullable=False)
    pergunta_gerada = Column(JSONB, nullable=False)  # mesmo schema de "Pergunta"

    resposta_dada = Column(JSONB)
    correta = Column(Boolean)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    respondido_em = Column(DateTime(timezone=True))

    user = relationship("User", backref="reforcos_topico")
    topico = relationship("Topico", backref="reforcos")

    def __repr__(self):
        return f"<TopicoReforco(topico_id={self.topico_id}, user_id={self.user_id}, question_id_origem='{self.question_id_origem}', correta={self.correta})>"
