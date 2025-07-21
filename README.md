# Kyoryoku (協力) - AI Team Collaboration Platform

A research prototype for exploring multi-agent AI systems and collaborative team configurations.

## Project Structure

```
kyoryoku/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   │   ├── agents/  # Agent implementations
│   │   ├── api/     # API endpoints
│   │   ├── core/    # Core configuration
│   │   ├── models/  # Database models
│   │   ├── services/# Business logic
│   │   └── utils/   # Utilities
│   └── tests/       # Backend tests
├── frontend/        # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   └── tests/
├── docs/           # Documentation
├── scripts/        # Utility scripts
└── docker-compose.yml

```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Anthropic API Key

### Setup

1. Clone the repository
2. Copy environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Update `.env` with your Anthropic API key

### Running with Docker

```bash
# Start all services
docker-compose up

# Or use make
make docker-up
```

### Running locally

```bash
# Install dependencies
make install

# Run development servers
make dev
```

Backend: http://localhost:8000
Frontend: http://localhost:5173

### Development Commands

```bash
# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean generated files
make clean
```

## Architecture

- **Backend**: FastAPI with async PostgreSQL and Redis
- **Frontend**: React with TypeScript and Vite
- **AI**: Anthropic Claude via LangChain/LangGraph
- **Real-time**: Socket.io for agent communication
- **Database**: PostgreSQL for persistence, Redis for caching

## Features

- Flexible agent configuration
- Pre-built team templates
- Real-time collaboration visualization
- Performance metrics and analysis
- Custom scenario builder

## License

Research prototype - see PRD for details