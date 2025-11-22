# 🗄️ NIA Platform - Documentação do Banco de Dados

**Versão:** 2.0  
**Database:** PostgreSQL 15  
**ORM:** SQLAlchemy  

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Diagrama ER](#diagrama-er)
3. [Tabelas](#tabelas)
4. [Relacionamentos](#relacionamentos)
5. [Índices e Performance](#índices-e-performance)
6. [Migrations](#migrations)
7. [Queries Comuns](#queries-comuns)

---

## 🎯 Visão Geral

O banco de dados da plataforma NIA é estruturado para suportar:

- ✅ Geração e armazenamento de cursos
- ✅ Módulos com conteúdo rico (texto, código, exemplos)
- ✅ Sistema de quizzes com múltiplas questões
- ✅ Acompanhamento de progresso individual
- ✅ Gamificação (pontos, badges, níveis)
- ✅ Metadados de geração por IA

### Tecnologias

- **PostgreSQL 15** - Banco relacional
- **SQLAlchemy** - ORM Python
- **Alembic** - Migrations
- **JSONB** - Dados semi-estruturados

---

## 📊 Diagrama ER (Entidade-Relacionamento)

```
┌─────────────────────┐
│       users         │
│─────────────────────│
│ id (PK)             │
│ email               │
│ name                │
│ google_id           │
│ linkedin_id         │
│ total_points        │
│ level               │
│ badges (JSONB)      │
│ created_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
┌──────────▼──────────┐         ┌─────────────────────┐
│      courses        │         │      modules        │
│─────────────────────│         │─────────────────────│
│ id (PK)             │ 1:N     │ id (PK)             │
│ title               │◄────────┤ course_id (FK)      │
│ description         │         │ module_index        │
│ level               │         │ title               │
│ duration_hours      │         │ description         │
│ prerequisites       │         │ duration_hours      │
│ structure (JSONB)   │         │ content (TEXT)      │
│ status              │         │ examples (JSONB)    │
│ created_by          │         │ exercises (JSONB)   │
│ generated_by (JSON) │         │ resources (JSONB)   │
│ created_at          │         │ quiz (JSONB)        │
└──────────┬──────────┘         │ review_score        │
           │                    │ reviewed_by         │
           │                    │ generated_by        │
           │ 1:N                │ created_at          │
           │                    └──────────┬──────────┘
           │                               │
           │                               │ 1:N
           │                               │
           └───────────────┬───────────────┘
                          │
                          │
                   ┌──────▼──────────┐
                   │    progress     │
                   │─────────────────│
                   │ id (PK)         │
                   │ user_id (FK)    │
                   │ course_id (FK)  │
                   │ module_id (FK)  │
                   │ status          │
                   │ started_at      │
                   │ completed_at    │
                   │ quiz_attempts   │
                   │ quiz_score      │
                   │ quiz_passed     │
                   │ quiz_answers    │
                   │ tutor_analysis  │
                   │ points_earned   │
                   │ badges (JSONB)  │
                   └─────────────────┘
```

---

## 📚 Tabelas Detalhadas

### 1. **users** - Usuários da Plataforma

Armazena informações dos usuários e gamificação.

```sql
CREATE TABLE users (
    -- Identificação
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    
    -- OAuth (Autenticação)
    google_id VARCHAR(255) UNIQUE,
    linkedin_id VARCHAR(255) UNIQUE,
    
    -- Gamificação
    total_points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    badges JSONB DEFAULT '[]'::jsonb,
    streak_days INTEGER DEFAULT 0,
    last_activity_date DATE,
    
    -- Preferências
    preferred_topics JSONB DEFAULT '[]'::jsonb,
    learning_style VARCHAR(50), -- visual, practical, theoretical
    notification_settings JSONB DEFAULT '{}'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    CONSTRAINT valid_level CHECK (level >= 1 AND level <= 100)
);

-- Índices
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_google_id ON users(google_id);
CREATE INDEX idx_users_total_points ON users(total_points DESC);
```

#### Campos JSONB

**badges** - Lista de conquistas
```json
[
  {
    "id": "first_steps",
    "name": "First Steps",
    "description": "Completou primeiro módulo",
    "earned_at": "2025-11-22T10:30:00Z",
    "icon": "🎓"
  }
]
```

**preferred_topics** - Temas de interesse
```json
["Python", "DevOps", "Machine Learning"]
```

---

### 2. **courses** - Cursos Gerados

Armazena a estrutura completa dos cursos.

```sql
CREATE TABLE courses (
    -- Identificação
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Classificação
    level VARCHAR(50) NOT NULL, -- basic, intermediate, advanced
    category VARCHAR(100),
    tags JSONB DEFAULT '[]'::jsonb,
    
    -- Informações do Curso
    duration_hours INTEGER NOT NULL,
    modules_count INTEGER DEFAULT 0,
    prerequisites JSONB DEFAULT '[]'::jsonb,
    learning_outcomes JSONB DEFAULT '[]'::jsonb,
    
    -- Estrutura (Gerada pela IA)
    structure JSONB NOT NULL,
    
    -- Status e Controle
    status VARCHAR(50) DEFAULT 'draft', -- draft, published, archived
    is_public BOOLEAN DEFAULT false,
    
    -- Autoria
    created_by VARCHAR(255), -- user_id (futuro: FK)
    
    -- Metadados de Geração IA
    generated_by JSONB,
    generation_time_seconds INTEGER,
    ai_quality_score DECIMAL(3,1),
    
    -- Estatísticas
    total_enrollments INTEGER DEFAULT 0,
    average_completion_rate DECIMAL(5,2) DEFAULT 0.0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_level CHECK (level IN ('basic', 'intermediate', 'advanced')),
    CONSTRAINT valid_status CHECK (status IN ('draft', 'published', 'archived')),
    CONSTRAINT valid_duration CHECK (duration_hours > 0),
    CONSTRAINT valid_quality_score CHECK (ai_quality_score >= 0 AND ai_quality_score <= 10)
);

-- Índices
CREATE INDEX idx_courses_status ON courses(status);
CREATE INDEX idx_courses_level ON courses(level);
CREATE INDEX idx_courses_created_by ON courses(created_by);
CREATE INDEX idx_courses_created_at ON courses(created_at DESC);
CREATE INDEX idx_courses_tags ON courses USING gin(tags);
```

#### Campos JSONB

**structure** - Estrutura completa do curso
```json
{
  "modules": [
    {
      "index": 1,
      "title": "Introdução ao Python",
      "duration_hours": 4,
      "topics": ["Sintaxe básica", "Variáveis", "Tipos de dados"],
      "learning_objectives": ["Entender sintaxe", "Criar variáveis"]
    }
  ],
  "syllabus": "Descrição completa...",
  "target_audience": "Iniciantes em programação",
  "certification_criteria": {
    "min_score": 70,
    "required_modules": 8
  }
}
```

**prerequisites** - Pré-requisitos
```json
["Lógica de programação", "Matemática básica"]
```

**learning_outcomes** - Objetivos de aprendizado
```json
[
  "Dominar sintaxe Python",
  "Criar aplicações CLI",
  "Entender POO"
]
```

**generated_by** - Metadados de geração
```json
{
  "orchestrator": "gemini-pro",
  "specialist": "llama-3.3-70b",
  "timestamp": "2025-11-22T10:00:00Z",
  "version": "2.0"
}
```

---

### 3. **modules** - Módulos dos Cursos

Armazena o conteúdo detalhado de cada módulo.

```sql
CREATE TABLE modules (
    -- Identificação
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    module_index INTEGER NOT NULL,
    
    -- Informações Básicas
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration_hours INTEGER NOT NULL,
    
    -- Conteúdo Principal
    content TEXT NOT NULL, -- Markdown com teoria completa
    
    -- Recursos Educacionais (JSONB)
    examples JSONB DEFAULT '[]'::jsonb,
    exercises JSONB DEFAULT '[]'::jsonb,
    resources JSONB DEFAULT '{}'::jsonb,
    
    -- Quiz/Avaliação
    quiz JSONB NOT NULL,
    
    -- Validação pela IA
    review_score DECIMAL(3,1),
    review_feedback JSONB,
    reviewed_by VARCHAR(100), -- Nome do agent reviewer
    
    -- Metadados de Geração
    generated_by VARCHAR(100), -- Nome do agent specialist
    generation_prompt TEXT,
    ai_model_used VARCHAR(100),
    
    -- Status
    is_published BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT unique_course_module_index UNIQUE(course_id, module_index),
    CONSTRAINT valid_duration CHECK (duration_hours > 0),
    CONSTRAINT valid_review_score CHECK (review_score >= 0 AND review_score <= 10),
    CONSTRAINT valid_module_index CHECK (module_index > 0)
);

-- Índices
CREATE INDEX idx_modules_course_id ON modules(course_id);
CREATE INDEX idx_modules_course_module ON modules(course_id, module_index);
CREATE INDEX idx_modules_review_score ON modules(review_score DESC);
```

#### Campos JSONB

**examples** - Exemplos práticos de código
```json
[
  {
    "title": "Hello World",
    "description": "Primeiro programa em Python",
    "language": "python",
    "code": "print('Hello, World!')",
    "output": "Hello, World!",
    "explanation": "A função print() exibe texto no console"
  }
]
```

**exercises** - Exercícios práticos
```json
[
  {
    "id": 1,
    "title": "Calculadora Simples",
    "description": "Crie uma calculadora que some dois números",
    "difficulty": "easy",
    "hints": [
      "Use a função input() para receber dados",
      "Converta strings para números com int()"
    ],
    "starter_code": "# Seu código aqui\n",
    "test_cases": [
      {"input": "2 3", "expected": "5"}
    ]
  }
]
```

**resources** - Recursos adicionais
```json
{
  "videos": [
    {
      "title": "Python Basics",
      "url": "https://youtube.com/...",
      "duration": "15:30"
    }
  ],
  "articles": [
    {
      "title": "PEP 8 Style Guide",
      "url": "https://pep8.org",
      "type": "documentation"
    }
  ],
  "books": ["Python Crash Course"],
  "external_links": []
}
```

**quiz** - Avaliação do módulo
```json
{
  "quiz_title": "Avaliação: Introdução ao Python",
  "total_points": 100,
  "passing_score": 70,
  "time_limit_minutes": 30,
  "questions": [
    {
      "id": 1,
      "type": "multiple_choice",
      "question": "O que a função print() faz?",
      "options": {
        "A": "Lê dados do usuário",
        "B": "Exibe texto no console",
        "C": "Cria variáveis",
        "D": "Importa bibliotecas"
      },
      "correct_answer": "B",
      "explanation": "print() exibe (imprime) texto no console/terminal",
      "difficulty": "easy",
      "points": 10,
      "tags": ["syntax", "basics"]
    },
    {
      "id": 2,
      "type": "code_completion",
      "question": "Complete o código para somar dois números:",
      "code_template": "a = 5\nb = 3\nresult = ___",
      "correct_answer": "a + b",
      "explanation": "O operador + realiza adição numérica",
      "difficulty": "medium",
      "points": 15
    }
  ]
}
```

**review_feedback** - Feedback do Reviewer Agent
```json
{
  "score": 8.5,
  "strengths": [
    "Exemplos práticos excelentes",
    "Progressão didática clara"
  ],
  "weaknesses": [
    "Falta exemplo de erro comum"
  ],
  "missing_topics": [
    "Type hints não foi abordado"
  ],
  "improvements": [
    "Adicionar seção sobre debugging",
    "Incluir mais exercícios práticos"
  ],
  "recommendation": "approved",
  "reviewed_at": "2025-11-22T11:00:00Z"
}
```

---

### 4. **progress** - Progresso dos Alunos

Rastreia o progresso individual em cada módulo.

```sql
CREATE TABLE progress (
    -- Identificação
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL, -- Futuro: FK para users(id)
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    
    -- Status do Módulo
    status VARCHAR(50) DEFAULT 'not_started',
    -- not_started, in_progress, completed, failed
    
    -- Timestamps de Progresso
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    last_accessed_at TIMESTAMP,
    
    -- Quiz/Avaliação
    quiz_attempts INTEGER DEFAULT 0,
    quiz_score INTEGER, -- 0-100
    quiz_passed BOOLEAN DEFAULT false,
    quiz_answers JSONB, -- Respostas do aluno
    quiz_completed_at TIMESTAMP,
    
    -- Análise Personalizada (Tutor Agent)
    tutor_analysis JSONB,
    
    -- Tempo de Estudo
    time_spent_minutes INTEGER DEFAULT 0,
    
    -- Gamificação
    points_earned INTEGER DEFAULT 0,
    badges JSONB DEFAULT '[]'::jsonb,
    
    -- Performance
    exercises_completed INTEGER DEFAULT 0,
    exercises_total INTEGER DEFAULT 0,
    
    -- Constraints
    CONSTRAINT unique_user_module UNIQUE(user_id, module_id),
    CONSTRAINT valid_status CHECK (status IN ('not_started', 'in_progress', 'completed', 'failed')),
    CONSTRAINT valid_quiz_score CHECK (quiz_score >= 0 AND quiz_score <= 100),
    CONSTRAINT valid_quiz_attempts CHECK (quiz_attempts >= 0)
);

-- Índices
CREATE INDEX idx_progress_user_id ON progress(user_id);
CREATE INDEX idx_progress_course_id ON progress(course_id);
CREATE INDEX idx_progress_module_id ON progress(module_id);
CREATE INDEX idx_progress_user_course ON progress(user_id, course_id);
CREATE INDEX idx_progress_status ON progress(status);
```

#### Campos JSONB

**quiz_answers** - Respostas do aluno
```json
[
  {
    "question_id": 1,
    "user_answer": "B",
    "correct_answer": "B",
    "is_correct": true,
    "points_earned": 10,
    "time_taken_seconds": 15
  },
  {
    "question_id": 2,
    "user_answer": "a - b",
    "correct_answer": "a + b",
    "is_correct": false,
    "points_earned": 0,
    "time_taken_seconds": 45
  }
]
```

**tutor_analysis** - Análise do Tutor Agent
```json
{
  "overall_performance": "good",
  "score_percentage": 75,
  "strengths": [
    "Domina conceitos básicos de sintaxe",
    "Boa compreensão de variáveis"
  ],
  "weaknesses": [
    "Dificuldade com operadores matemáticos",
    "Confunde + e -"
  ],
  "recommendations": [
    "Revisar seção 2.3 sobre operadores",
    "Praticar exercícios 5-7",
    "Assistir vídeo complementar sobre aritmética"
  ],
  "next_steps": "Revisar conteúdo antes de avançar para módulo 2",
  "estimated_review_time_hours": 2,
  "difficulty_areas": ["operators", "math"],
  "ready_for_next_module": false,
  "analyzed_at": "2025-11-22T14:30:00Z",
  "agent": "tutor-llama3-local"
}
```

**badges** - Conquistas do módulo
```json
[
  {
    "badge_id": "quiz_perfect",
    "earned_at": "2025-11-22T15:00:00Z"
  }
]
```

---

## 🔗 Relacionamentos

### Cardinalidade

```
users (1) ──────── (N) progress
courses (1) ──────── (N) modules
courses (1) ──────── (N) progress
modules (1) ──────── (N) progress
```

### Constraints de Integridade

- **ON DELETE CASCADE**: Se um curso for deletado, todos os módulos e progresso são deletados
- **UNIQUE**: Garante que um usuário não tenha múltiplos registros para o mesmo módulo
- **CHECK**: Valida valores de enums e ranges numéricos

---

## ⚡ Índices e Performance

### Índices Principais

```sql
-- Busca por usuário
CREATE INDEX idx_progress_user_id ON progress(user_id);

-- Listagem de cursos
CREATE INDEX idx_courses_status_created ON courses(status, created_at DESC);

-- Busca de módulos de um curso
CREATE INDEX idx_modules_course_module ON modules(course_id, module_index);

-- Ranking (leaderboard)
CREATE INDEX idx_users_points ON users(total_points DESC);

-- Busca textual (futuro)
CREATE INDEX idx_courses_search ON courses USING gin(to_tsvector('portuguese', title || ' ' || description));
```

### Otimizações

- **JSONB com GIN index** para buscas em tags e badges
- **Particionamento** futuro na tabela `progress` por data
- **Materialized Views** para estatísticas agregadas

---

## 🔄 Migrations (Alembic)

### Setup Inicial

```bash
# Instalar Alembic
pip install alembic

# Inicializar
alembic init alembic

# Criar primeira migration
alembic revision --autogenerate -m "initial schema"

# Aplicar
alembic upgrade head
```

### Exemplo de Migration

```python
# alembic/versions/001_initial_schema.py

def upgrade():
    # Criar tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('total_points', sa.Integer(), server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Criar tabela courses
    # ... etc

def downgrade():
    op.drop_table('users')
    # ... etc
```

---

## 📝 Queries Comuns

### 1. Listar cursos publicados

```sql
SELECT 
    id,
    title,
    description,
    level,
    duration_hours,
    modules_count,
    average_rating
FROM courses
WHERE status = 'published' AND is_public = true
ORDER BY created_at DESC
LIMIT 20;
```

### 2. Progresso de um aluno em um curso

```sql
SELECT 
    c.title AS course_title,
    m.title AS module_title,
    p.status,
    p.quiz_score,
    p.quiz_passed,
    p.completed_at
FROM progress p
JOIN modules m ON p.module_id = m.id
JOIN courses c ON m.course_id = c.id
WHERE p.user_id = 'user_123' AND c.id = 42
ORDER BY m.module_index;
```

### 3. Estatísticas de um curso

```sql
SELECT 
    c.title,
    COUNT(DISTINCT p.user_id) AS total_students,
    AVG(p.quiz_score) AS avg_score,
    COUNT(CASE WHEN p.status = 'completed' THEN 1 END) AS completed_modules,
    COUNT(p.id) AS total_attempts
FROM courses c
LEFT JOIN modules m ON c.id = m.course_id
LEFT JOIN progress p ON m.id = p.module_id
WHERE c.id = 42
GROUP BY c.id, c.title;
```

### 4. Leaderboard (Ranking)

```sql
SELECT 
    u.name,
    u.total_points,
    u.level,
    u.badges->>'count' AS badge_count,
    RANK() OVER (ORDER BY u.total_points DESC) AS rank
FROM users u
WHERE u.total_points > 0
ORDER BY u.total_points DESC
LIMIT 100;
```

### 5. Cursos com melhor avaliação

```sql
SELECT 
    c.title,
    c.level,
    c.average_rating,
    c.total_enrollments,
    ROUND(c.average_completion_rate, 2) AS completion_rate
FROM courses c
WHERE c.status = 'published' 
  AND c.total_enrollments >= 10
ORDER BY c.average_rating DESC, c.total_enrollments DESC
LIMIT 10;
```

### 6. Módulos que precisam de revisão

```sql
SELECT 
    c.title AS course,
    m.title AS module,
    m.review_score,
    m.generated_by,
    m.created_at
FROM modules m
JOIN courses c ON m.course_id = c.id
WHERE m.review_score < 7.0 
   OR m.review_score IS NULL
ORDER BY m.review_score ASC NULLS FIRST;
```

---

## 🎯 Próximos Passos

### Fase 1 - Implementação Básica
- [ ] Criar models SQLAlchemy
- [ ] Configurar migrations com Alembic
- [ ] Seed data para desenvolvimento

### Fase 2 - Otimizações
- [ ] Implementar índices GIN para JSONB
- [ ] Criar materialized views para dashboards
- [ ] Adicionar full-text search

### Fase 3 - Analytics
- [ ] Tabela de eventos (user_events)
- [ ] Métricas de engajamento
- [ ] A/B testing de conteúdo

---

## 📚 Referências

- [PostgreSQL JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Database Indexing Best Practices](https://use-the-index-luke.com/)

---

**Última atualização:** Novembro 2025  
**Versão do Schema:** 1.0