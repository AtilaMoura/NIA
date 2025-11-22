# 🧠 NIA Platform

**Multi-Agent AI Learning Platform** - Sistema educacional inteligente com geração automática de cursos

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/next.js-14+-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🎯 Sobre o Projeto

NIA é uma plataforma educacional que utiliza **5 agentes de IA especializados** para criar cursos completos automaticamente:

- 🎓 **Specialist Agent** - Gera conteúdo especializado (Llama 3.3-70B)
- ✅ **Reviewer Agent** - Valida qualidade técnica (Llama 3.1-8B)
- 🎯 **Quiz Master** - Cria avaliações (Gemini Pro)
- 👨‍🏫 **Tutor Agent** - Análise personalizada (Llama 3 Local)
- 🎭 **Orchestrator** - Coordena todo o pipeline (Gemini Pro)

## ✨ Features

- ✅ Geração automática de cursos com IA
- ✅ Múltiplos agentes especializados
- ✅ Sistema de quiz inteligente
- ✅ Análise personalizada de desempenho
- ✅ Gamificação (pontos, badges, níveis)
- ✅ 100% gratuito (APIs grátis)

## 🏗️ Arquitetura

```
┌─────────────────┐
│  Next.js :4000  │  Frontend
└────────┬────────┘
         │
┌────────▼────────┐
│ FastAPI :8000   │  Backend + Multi-Agent System
└────────┬────────┘
         │
┌────────▼────────┐
│ PostgreSQL      │  Database
└─────────────────┘
```

## 🚀 Quick Start

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose
- [Ollama](https://ollama.com/) (opcional, para Tutor Agent local)

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/nia-platform.git
cd nia-platform
```

### 2. Configurar variáveis de ambiente

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

**Edite os arquivos `.env` com suas chaves de API:**

- [Google Gemini API](https://ai.google.dev) (gratuita)
- [Groq API](https://console.groq.com) (gratuita)

### 3. Executar com Docker

```bash
# Subir todos os serviços
docker-compose up --build

# Ou em modo detached
docker-compose up -d --build
```

### 4. Acessar

- 🎨 **Frontend**: http://localhost:4000
- ⚙️ **Backend**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 🗄️ **Database**: localhost:5432

## 📂 Estrutura do Projeto

```
nia-platform/
├── frontend/           # Next.js + React + TypeScript
│   ├── app/           # Pages (App Router)
│   ├── components/    # Componentes React
│   └── Dockerfile
│
├── backend/           # FastAPI + Python
│   ├── app/
│   │   ├── agents/    # Sistema Multi-Agent
│   │   ├── models/    # Modelos do banco
│   │   ├── routers/   # Endpoints da API
│   │   └── services/  # Serviços de IA
│   └── Dockerfile
│
├── docs/              # Documentação (GitHub Pages)
├── docker-compose.yml # Orquestração Docker
└── README.md
```

## 🤖 Sistema Multi-Agent

### Pipeline de Geração de Curso

```
1. Usuário solicita: "Criar curso de Python Avançado"
   ↓
2. Orchestrator Agent valida e cria pipeline
   ↓
3. Specialist Agent gera estrutura + módulos
   ↓
4. Reviewer Agent valida qualidade (nota 0-10)
   ↓
5. Quiz Master cria avaliações
   ↓
6. Salva no banco de dados
   ↓
7. Pronto para uso!
```

### Tempo médio: ~5-7 minutos para curso com 2 módulos

## 🎮 Gamificação

- **50 pontos** - Completar módulo
- **100 pontos** - Passar no quiz (70%+)
- **200 pontos** - Quiz perfeito (100%)
- **300 pontos** - Streak de 7 dias

**Badges:** First Steps, Quiz Master, Dedicated, Speedrunner, Perfectionist

## 📚 Documentação

- [Documentação Completa](https://seu-usuario.github.io/nia-platform)
- [API Reference](http://localhost:8000/docs)
- [Guia de Contribuição](CONTRIBUTING.md)

## 🛠️ Desenvolvimento

### Comandos úteis

```bash
# Ver logs
docker-compose logs -f

# Parar tudo
docker-compose down

# Reconstruir um serviço específico
docker-compose build frontend
docker-compose up frontend

# Limpar tudo
docker-compose down -v
docker system prune -a
```

### Rodar localmente (sem Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🗺️ Roadmap

- [x] ✅ Estrutura base (Docker + FastAPI + Next.js)
- [x] ✅ Sistema Multi-Agent
- [ ] 🔄 CRUD completo de cursos
- [ ] 🔄 Sistema de Quiz
- [ ] 📋 Dashboard do aluno
- [ ] 📋 Gamificação completa
- [ ] 📋 Autenticação (Google/LinkedIn)
- [ ] 📋 Certificados digitais
- [ ] 📋 Mobile app

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines.

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m 'feat: adiciona nova feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👥 Autor

Desenvolvido com 💜 por [Seu Nome]

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Google Gemini](https://ai.google.dev)
- [Groq](https://groq.com)
- [Ollama](https://ollama.com)

---

**⭐ Se este projeto te ajudou, deixe uma estrela!**