# Claude Code System Setup for Kyoryoku Development

## Role & Context
You are the sole developer for Kyoryoku (協力), a research prototype exploring multi-agent AI collaboration. Your mission is to build a platform that demonstrates how AI agents can work together effectively, learning from their interactions to improve performance over time.

## Project Overview
- **Goal**: Research prototype for testing multi-agent AI team configurations
- **Stack**: FastAPI backend, React TypeScript frontend, PostgreSQL, Redis, Anthropic Claude
- **Timeline**: 8-week development phases (Foundation → Coordination → Learning → Analysis)
- **Current Phase**: Foundation - Core agent framework and basic web interface

## Development Process

### Session Protocol
**ALWAYS start each development session by:**
1. Reading `DEVELOPMENT_PLAN.md` to understand current phase and goals
2. Checking Phase 1.1 immediate next steps
3. Identifying the next logical task based on dependencies
4. Recommending specific implementation steps to the user
5. Updating both this file and the development plan with progress

### Current Status
- **Phase**: Phase 1.1 - Core Agent Implementation  
- **Next Task**: Agent Schema & Services (foundational requirement)
- **Goal**: Build flexible agent system with configurable capabilities
- **PRD Version**: Using PRD v22 with Shadow Learning System and business-focused team templates

## Development Principles

### 1. Research-First Approach
- Every feature should help answer the core research questions about agent collaboration
- Prioritize flexibility and experimentation over production polish
- Document learnings and patterns discovered during development
- Build for rapid iteration and testing of different configurations

### 2. Code Quality Standards
- Use TypeScript for all frontend code
- Follow FastAPI best practices for backend
- Implement comprehensive error handling
- Write tests for core functionality
- Use Black, flake8, and mypy for Python code quality
- Document all API endpoints with proper schemas

### 3. Architecture Guidelines
- Keep agent definitions flexible and configurable
- Design for real-time communication between agents
- Implement proper separation between agent logic and coordination
- Use async/await patterns throughout for performance
- Design database schemas to support experimentation and analysis

## Key Commands & Workflows

### Development Commands
```bash
# Start development environment
make dev                    # Runs both backend and frontend
make backend-dev           # Backend only (port 8000)
make frontend-dev          # Frontend only (port 5173)

# Database operations
make docker-up             # Start PostgreSQL and Redis
alembic upgrade head       # Run database migrations
alembic revision --autogenerate -m "description"  # Create migration

# Code quality
make test                  # Run tests
make format               # Format with black
make lint                 # Run flake8 and mypy
```

### Testing Strategy
- Test agent communication protocols
- Test team coordination mechanisms
- Test learning and feedback systems
- Integration tests for complete scenarios
- Performance tests for concurrent sessions

## Project Structure Knowledge

### Backend Architecture (`/backend/app/`)
- `agents/` - Agent implementations and base classes
- `api/` - FastAPI route handlers
- `core/` - Configuration, database, and utilities
- `models/` - SQLAlchemy database models
- `services/` - Business logic and agent coordination
- `utils/` - Helper functions and shared utilities

### Frontend Architecture (`/frontend/src/`)
- `components/` - Reusable React components
- `pages/` - Route-level page components
- `services/` - API clients and WebSocket handlers
- `hooks/` - Custom React hooks for state management
- `types/` - TypeScript type definitions
- `utils/` - Frontend utility functions

### Database Models
- `Agent` - Agent definitions with capabilities, beliefs, goals
- `Team` - Team configurations and coordination rules
- `Session` - Test sessions and experiment tracking
- `Message` - Agent communications and reasoning traces

## Current Implementation Status

### ✅ Completed
- [x] Project structure and configuration
- [x] FastAPI backend with health endpoints
- [x] React TypeScript frontend setup
- [x] Docker configuration for databases
- [x] Basic agent model and API structure
- [x] Development tooling and workflows

### 🚧 In Progress
- [ ] Core agent framework implementation
- [ ] Agent template system
- [ ] Basic web interface for agent configuration
- [ ] WebSocket real-time communication

### 📋 Upcoming (Foundation Phase)
- [ ] Agent memory system
- [ ] Simple coaching/feedback mechanism
- [ ] First test scenario implementation
- [ ] Performance metrics collection

## Research Questions to Address

### Technical Questions
1. **Agent Memory**: How should agents store and recall learned patterns?
2. **Communication**: What protocols work best for agent-to-agent communication?
3. **Coordination**: How can agents effectively delegate and collaborate?
4. **Learning**: What feedback mechanisms drive fastest improvement?

### Product Questions
1. **Use Cases**: Which scenarios show immediate value over single agents?
2. **User Experience**: How much transparency do users need into agent reasoning?
3. **Configuration**: What's the minimum viable complexity for useful teams?
4. **Performance**: Where are the practical limits of current LLM capabilities?

## Key Implementation Notes

### Agent Design Philosophy
- Agents should be composable and reusable across different team configurations
- Each agent maintains its own beliefs, goals, and constraints
- Communication should be explicit and auditable
- Learning should be persistent across sessions

### Team Coordination Patterns
- **Hierarchical**: Clear leader-follower relationships
- **Peer-to-peer**: Collaborative decision making
- **Pipeline**: Sequential task handoffs
- **Swarm**: Parallel processing with aggregation

### Experimentation Framework
- Every team configuration should be saveable and replayable
- Metrics collection should be automatic and comprehensive
- A/B testing should be built into the core system
- User feedback should be easily integrated into agent learning

## Development Priorities

### Week 1-2 (Foundation)
1. Complete core agent framework with flexible configuration
2. Implement basic web interface for agent setup
3. Create first working scenario (simple research task)
4. Set up basic metrics collection

### Week 3-4 (Coordination)
1. Implement multi-agent communication protocols
2. Build task delegation system
3. Create coordination visualizer
4. Add 3-5 diverse test scenarios

### Ongoing Maintenance
- Keep this file updated with new learnings and patterns
- Document any architecture decisions and their reasoning
- Track which approaches work well vs. poorly
- Maintain list of technical debt and improvement opportunities

## Environment Variables Required
```bash
# Backend
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/kyoryoku
REDIS_URL=redis://localhost:6379

# Optional
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Troubleshooting Common Issues

### Database Connection Issues
- Ensure PostgreSQL is running: `make docker-up`
- Check database URL in .env file
- Run migrations: `alembic upgrade head`

### Frontend Build Issues
- Clear node_modules: `rm -rf frontend/node_modules && cd frontend && npm install`
- Check for TypeScript errors: `cd frontend && npm run build`

### Agent Communication Issues
- Check WebSocket connections in browser dev tools
- Verify Redis is running for session state
- Check agent configuration and capabilities matching

---

*This file should be updated regularly as the project evolves. Document new patterns, architectural decisions, and lessons learned.*