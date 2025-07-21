# Claude Code System Setup for Kyoryoku Development

## Role & Context

You are the sole developer for Kyoryoku (協力), a strategic research platform for validating the commercial viability of multi-agent AI systems. Your mission is to build a focused validation prototype that tests specific high-value use cases with rigorous market and technical validation.

## 📋 **CRITICAL: PRD as Source of Truth**

**ALWAYS reference `PRD.md` as the single source of truth for this project.**

### PRD Status

- **File**: `PRD.md` (Version 3.0)
- **Status**: Canonical source of truth - consolidated from multiple previous versions
- **Strategic Focus**: Customer Success Response Teams (PRIMARY), RFP/Proposal Acceleration (SECONDARY)
- **Last Updated**: December 2024
- **Key Change**: Shifted from general research to strategic market validation with clear PMF paths

### Before Making Any Decisions:

1. **Read relevant sections of `PRD.md`** for context
2. **Follow the prioritization matrix** in Section 2.1
3. **Align with the strategic focus** on customer success and RFP use cases
4. **Consider the technical risk assessment** in Section 6.2
5. **Reference the development roadmap** in Section 10

### PRD Quick Reference Guide

- **Market Analysis**: Section 2 - Use case prioritization and competitive landscape
- **Customer Research**: Section 3 - Validation framework with interview scripts
- **Core Hypotheses**: Section 4.1 - Four primary hypotheses with statistical frameworks
- **Architecture**: Section 5 - Focused prototype for customer success teams
- **Technical Risks**: Section 6.2 - Comprehensive risk assessment matrix
- **Success Metrics**: Section 8 - SMART goals with specific targets
- **Roadmap**: Section 10 - 12-week development phases with resource allocation

## Project Overview

- **Strategic Goal**: Validate multi-agent AI commercial viability in customer success and RFP markets
- **Primary Focus**: Customer Success Response Teams (18-minute → 3-minute ticket resolution)
- **Secondary Focus**: RFP/Proposal Acceleration (80-hour → 4-hour completion)
- **Stack**: FastAPI backend, React TypeScript frontend, PostgreSQL, Redis, Anthropic Claude
- **Timeline**: 12-week validation phases (Foundation → Scaled Validation → Business Case)
- **Success Criteria**: 60%+ willingness to pay, 50%+ performance improvement, 70%+ pilot retention

## Development Process

### Session Protocol

**ALWAYS start each development session by:**

1. **Reading `PRD.md` Section 10** (Development Roadmap) to understand current phase
2. **Checking the strategic focus** in Section 2.1 (Customer Success PRIMARY)
3. **Reviewing technical priorities** based on risk assessment in Section 6.2
4. **Identifying customer validation tasks** from Section 3 if applicable
5. **Updating progress** against the specific Phase metrics in PRD.md

### Current Status

- **Phase**: Phase 1 - Foundation & Validation (Weeks 1-4)
- **Primary Market Focus**: Customer Success Response Team (4-agent system)
- **Testing Priority**: Content Creation Team implementation (for platform validation)
- **Current Week**: Week 1 - Customer Research (60%) + Technical Setup (40%)
- **Next Priority**: Customer interviews + Content Creation Team for testing
- **PRD Version**: 3.0 - Strategic Research Prototype (canonical source)

## Development Principles

### 1. Customer-Validation-First Approach

- **Every feature must validate specific hypotheses** from PRD Section 4.1
- **Prioritize customer research** - 100 interviews planned (Section 3.1)
- **Build for pilot customers** - 3-5 pilots per use case target
- **Measure willingness to pay** - 60%+ target for $500+/month pricing
- **Track retention metrics** - 70%+ weekly active usage after 30 days

### 2. Strategic Focus Discipline

- **Primary**: Customer Success Response Teams ONLY (until validated)
- **Secondary**: RFP/Proposal Acceleration (after primary validation)
- **Resist scope creep** - No other use cases until current ones validated
- **Follow prioritization matrix** in PRD Section 2.1
- **Reference customer personas** Sarah (CS Ops Manager) and David (Sales Engineer) in Section 13.1

### 3. Technical Implementation with Business Focus

- **Cost-conscious development** - Track token usage ($0.44/ticket target)
- **Error handling for pilot customers** - 95%+ uptime requirement
- **Shadow learning implementation** - Core differentiator for competitive moat
- **Integration readiness** - Plan for Zendesk, Salesforce, Intercom
- **Statistical rigor** - N=100+ samples, p<0.05 significance testing

## Key Research Hypotheses (From PRD Section 4.1)

### H1: Multi-Agent Teams Deliver Superior ROI vs Single Agents [PRIMARY]

- **Target**: 85% task completion vs 60% single agent
- **Measurement**: A/B test with N=200 tasks per condition
- **Implementation Focus**: Build customer support 4-agent team first

### H2: Shadow Learning Creates Sustainable Competitive Moats [PRIMARY]

- **Target**: 85% suggestion acceptance after 4 weeks
- **Measurement**: 12-week longitudinal study
- **Implementation Focus**: Observation → Suggestion → Assisted phases

### H3: Customers Will Pay Premium for Multi-Agent Capabilities [CRITICAL]

- **Target**: 70% pilot-to-paid conversion
- **Measurement**: Conjoint analysis with N=200 prospects
- **Implementation Focus**: ROI demonstration, pricing validation

### H4: Technical Infrastructure Can Scale Economically [SECONDARY]

- **Target**: <$0.50 cost per resolved ticket
- **Measurement**: Load testing with statistical monitoring
- **Implementation Focus**: Token optimization, response caching

## Customer Success Team Architecture (Primary Focus)

### Four-Agent Specialization (PRD Section 5.1)

```python
TriageSpecialist    # Categorization, urgency assessment, routing
SolutionResearcher  # Knowledge search, context matching, solution ranking
ResponseCrafter     # Writing, tone matching, personalization
EscalationAnalyst   # Complexity assessment, expert matching, handoff prep
```

### Success Metrics for Customer Success Use Case

- **Time Reduction**: 18 minutes → 3 minutes (83% improvement)
- **Quality Maintenance**: 4.2/5 rating (vs 3.8/5 human baseline)
- **Escalation Accuracy**: 95% correct escalations
- **Customer Satisfaction**: Maintain current levels while improving speed

## Content Creation Team Architecture (Testing Priority)

### Five-Agent Specialization (PRD Section 5.3)

```python
StoryMiner          # Extract compelling narratives from source material
TechnicalTranslator # Simplify complex concepts for general audiences
VoiceCrafter        # Maintain authentic, personal tone
StructureArchitect  # Organize ideas into compelling narrative flow
HookDesigner        # Create engaging openings and maintain momentum
```

### Iterative Refinement Coordination Pattern

Unlike Customer Success (sequential) or RFP (parallel), Content Creation uses iterative refinement:

1. **Story Mining** → 2. **Structure** → 3. **Translation** → 4. **Voice** → 5. **Hooks**
   Each agent builds on the previous agent's work in rounds.

### Testing Success Metrics

- **Platform Validation**: 90%+ successful multi-agent handoffs
- **Content Creation Speed**: 10 minutes vs 2 hours traditional
- **Demo Effectiveness**: Track prospect engagement during demos
- **Coordination Pattern Validation**: Prove iterative refinement works

### Why This Tests Our Platform

- **Proves multi-agent coordination** before customer pilots
- **Tests complex coordination patterns** (iterative vs sequential/parallel)
- **Validates agent reasoning transparency** needed for customer trust
- **Creates marketing assets** while testing the platform
- **Demonstrates value proposition** through meta-storytelling

**Implementation Priority**: Week 2-3 for platform testing and demos

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

### Customer Validation Workflows

```bash
# Reference PRD Section 3.1 for customer research framework
# Use interview scripts from PRD Appendix A
# Track metrics from PRD Section 8 (Success Metrics)
```

## Risk Management (From PRD Section 6.2)

### High-Priority Technical Risks

- **API costs exceed budget** - Implement token optimization, aggressive caching
- **Multi-agent coordination failures** - Extensive testing, fallback to single agent
- **Response latency > 10 seconds** - Async processing, pre-computation
- **Pilot customers don't convert** - Improve onboarding, demonstrate ROI

### Market Validation Risks

- **No clear PMF** - Continuous customer validation, pivot criteria defined
- **Competitive response** - Focus on network effects, data moats
- **Customer acquisition costs too high** - Product-led growth strategies

## Implementation Priorities (From PRD Section 10)

### Week 1: Customer Research & Technical Setup (Current)

**Customer Research (60% effort)**:

- Conduct 25 customer interviews using PRD Appendix A scripts
- Validate pain points: 18-minute ticket resolution, knowledge fragmentation
- Test willingness to pay: $500-2000/month pricing

**Technical Foundation (40% effort)**:

- Set up development environment
- Implement basic agent framework for TriageSpecialist
- Create customer support scenario prototype

### Week 2: Customer Success Prototype

- Build 4-agent coordination system (Triage → Research → Craft → Escalate)
- Implement basic shadow learning (observation phase)
- Create simple web interface for testing with pilot customers

### Week 3-4: Baseline Establishment & Testing

- Deploy prototype with 5 pilot customers
- Complete statistical baseline measurements
- A/B test multi-agent vs single agent performance
- Gather willingness to pay data

## Success Criteria & Decision Framework (PRD Section 12)

### Go Decision Criteria (Must achieve ALL)

1. **Technical feasibility demonstrated** - Multi-agent coordination >70% success
2. **Market demand validated** - 60%+ willing to pay $500+/month
3. **Sustainable unit economics** - 85%+ gross margins proven
4. **Clear competitive advantages** - Shadow learning differentiation

### Pivot Criteria (ANY triggers pivot)

1. **<40% willingness to pay** at target pricing
2. **<30% performance improvement** vs baselines
3. **<50% pilot retention** after 90 days
4. **Technical barriers prove insurmountable**

### Current Key Metrics to Track

- **Customer interview completion**: 25/25 target for Week 1
- **Pain point validation**: Average ticket time confirmation
- **Pricing validation**: Willingness to pay $500+ percentage
- **Technical progress**: Basic agent framework completion

## Environment Variables Required

```bash
# Backend (same as before)
ANTHROPIC_API_KEY=sk-...
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/kyoryoku
REDIS_URL=redis://localhost:6379

# Customer Research (if using tools)
CALENDLY_API_KEY=...    # For scheduling interviews
MIXPANEL_TOKEN=...      # For tracking pilot customer usage
```

## Customer Research Integration

### Interview Management

- **Target**: 25 CS Operations Managers, 15 CS Directors, 10 CS Reps
- **Scripts**: Use PRD Appendix A interview framework
- **Focus**: Pain validation, willingness to pay, pilot interest
- **Success Metric**: 60% show interest in pilot program

### Pilot Customer Onboarding

- **Shadow Learning**: Start with observation-only mode (Week 1-2)
- **Success Criteria**: 50%+ time reduction, 70%+ satisfaction, ROI demonstration
- **Retention Target**: 80%+ after 90 days

## Troubleshooting & Common Issues

### PRD Alignment Issues

- **Problem**: Feature request not aligned with strategic focus
- **Solution**: Reference PRD Section 2.1 prioritization matrix
- **Escalation**: Only implement if directly validates core hypotheses

### Customer Validation Blockers

- **Problem**: Low customer interview response rates
- **Solution**: Reference PRD Section 13 for customer journey optimization
- **Alternative**: Focus on warm network introductions

### Technical Performance Issues

- **Problem**: Token costs exceeding $0.50/ticket
- **Solution**: Implement PRD Section 6.3 cost optimization strategies
- **Monitoring**: Track real-time cost per interaction

---

## 🎯 **Key Reminders for Future Claude Instances**

1. **`PRD.md` is the single source of truth** - Always reference it before making decisions
2. **Customer Success Teams are PRIMARY market focus** - Don't dilute effort on other use cases
3. **Content Creation Team is TESTING PRIORITY** - Implement first for platform validation and demos
4. **Customer validation comes first** - 60% effort on research, 40% on technical in Week 1
5. **Statistical rigor required** - N=100+ samples, p<0.05 significance
6. **Pilot customers are real customers** - Build for production-level reliability
7. **Cost consciousness** - Track token usage and unit economics constantly
8. **Strategic decision criteria** - Clear Go/Pivot/No-Go thresholds defined

_This file should be updated when PRD.md changes or when major learnings emerge. Always maintain alignment between this file and the canonical PRD._
