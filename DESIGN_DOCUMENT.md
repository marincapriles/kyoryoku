# Kyoryoku System Design Document
**Version 1.0** | **Date**: 2025-01-20 | **Research Prototype Architecture**

---

## 1. Executive Summary

This document defines the system architecture for Kyoryoku (協力), a research platform for exploring multi-agent AI collaboration. The design prioritizes **flexibility for experimentation** over production optimization, enabling rapid testing of different agent configurations and coordination patterns.

### Design Philosophy
- **Research-First**: Every architectural decision supports hypothesis testing and pattern discovery
- **Flexibility Over Performance**: Optimize for configuration variety rather than speed
- **Observable Interactions**: Make all agent communications and reasoning transparent
- **Iterative Learning**: Support continuous improvement through feedback loops

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  Backend API    │    │   AI Services   │
│   (React TS)    │◄──►│   (FastAPI)     │◄──►│   (Claude API)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                        ┌──────┴──────┐
                        │             │
              ┌─────────▼─────┐ ┌─────▼─────┐
              │  PostgreSQL   │ │   Redis   │
              │  (Persistent) │ │ (Session) │
              └───────────────┘ └───────────┘
```

### 2.2 Core Design Decisions

| **Decision** | **Rationale** | **Trade-offs** |
|--------------|---------------|----------------|
| **Monolithic Backend** | Simplicity for research prototype | Limited horizontal scaling |
| **SQLAlchemy + PostgreSQL** | Rich querying for analysis | Higher complexity than NoSQL |
| **Redis for Sessions** | Fast state management | Additional infrastructure |
| **Socket.io for Real-time** | Mature WebSocket library | More overhead than native WS |
| **LangGraph Orchestration** | Built for agent workflows | Learning curve, dependency |

---

## 3. Domain Model & Core Entities

### 3.1 Agent Entity

**Purpose**: Represents an AI agent with specific capabilities, knowledge, and goals.

```python
class Agent:
    id: UUID
    name: str                    # "Market Researcher", "Data Analyst"
    description: str             # Human-readable purpose
    capabilities: List[str]      # ["search", "analyze", "summarize"]
    beliefs: Dict[str, float]    # Knowledge with confidence scores
    goals: List[str]            # Current objectives
    constraints: List[str]       # Limitations and boundaries
    memory: AgentMemory         # Persistent learning storage
    template_type: str          # "researcher", "analyst", "writer"
    created_at: datetime
    updated_at: datetime
```

**Key Design Decisions**:
- **Beliefs as Dict[str, float]**: Enables confidence-weighted knowledge
- **Capabilities as List[str]**: Simple but extensible skill system
- **Memory as Separate Entity**: Allows complex memory architectures
- **Template System**: Pre-built configurations for common roles

### 3.2 Team Entity

**Purpose**: Defines a collection of agents with coordination rules.

```python
class Team:
    id: UUID
    name: str                    # "Research Team Alpha"
    description: str
    agents: List[Agent]          # Team members
    coordination_pattern: str    # "hierarchical", "peer", "pipeline"
    communication_rules: Dict    # How agents interact
    shared_memory: Dict          # Team-wide knowledge
    goal: str                    # Team-level objective
    template_type: str           # "research", "creative", "analysis", "planning", "custom"
    created_at: datetime
```

**Key Design Decisions**:
- **Coordination Patterns**: Explicit models for different team structures
- **Communication Rules**: Configurable interaction protocols
- **Shared Memory**: Team-level knowledge distinct from individual agent memory
- **Template System**: Pre-built team configurations from PRD

### 3.3 Team Templates (from PRD v22)

**1. Customer Success Response Team**
- **Use Case**: Scale support quality across all representatives
- **Target Metric**: Resolve tickets in 2 minutes vs 20 minutes
```python
CUSTOMER_SUCCESS_TEMPLATE = {
    "name": "Customer Success Response Team",
    "coordination_pattern": "sequential_pipeline",
    "agents": [
        {"role": "Triage Specialist", "capabilities": ["categorize_issues", "identify_urgency", "route_appropriately"]},
        {"role": "Solution Researcher", "capabilities": ["search_knowledge_base", "find_past_tickets", "match_solutions"]},
        {"role": "Response Crafter", "capabilities": ["write_empathetic_responses", "maintain_brand_voice", "ensure_accuracy"]},
        {"role": "Escalation Analyst", "capabilities": ["identify_complex_cases", "determine_human_need", "route_to_experts"]}
    ]
}
```

**2. RFP/Proposal Acceleration Team**
- **Use Case**: Win more deals by responding to RFPs 10x faster
- **Target Metric**: Complete 50-page RFP in 1 hour vs 1 week
```python
RFP_ACCELERATION_TEMPLATE = {
    "name": "RFP/Proposal Acceleration Team",
    "coordination_pattern": "parallel_assembly",
    "agents": [
        {"role": "Requirements Analyst", "capabilities": ["parse_rfp_requirements", "extract_discrete_needs", "prioritize_requirements"]},
        {"role": "Content Assembler", "capabilities": ["pull_past_proposals", "access_case_studies", "organize_content"]},
        {"role": "Compliance Checker", "capabilities": ["verify_requirement_coverage", "ensure_compliance", "validate_completeness"]},
        {"role": "Customization Writer", "capabilities": ["tailor_content", "client_specific_customization", "personalize_proposals"]}
    ]
}
```

**3. Product Intelligence Team**
- **Use Case**: Synthesize customer feedback into actionable insights
- **Target Metric**: Process 1,000 inputs into 5 insights daily
```python
PRODUCT_INTELLIGENCE_TEMPLATE = {
    "name": "Product Intelligence Team",
    "coordination_pattern": "parallel_synthesis",
    "agents": [
        {"role": "Feedback Aggregator", "capabilities": ["collect_support_feedback", "monitor_reviews", "gather_surveys"]},
        {"role": "Pattern Detector", "capabilities": ["identify_trends", "detect_emerging_themes", "spot_anomalies"]},
        {"role": "Impact Analyzer", "capabilities": ["estimate_business_value", "assess_improvement_impact", "prioritize_features"]},
        {"role": "Insight Reporter", "capabilities": ["create_exec_summaries", "generate_reports", "present_findings"]}
    ]
}
```

**4. Knowledge Transfer Team**
- **Use Case**: Preserve and scale institutional knowledge
- **Target Metric**: Reduce onboarding time from 3 months to 3 weeks
```python
KNOWLEDGE_TRANSFER_TEMPLATE = {
    "name": "Knowledge Transfer Team",
    "coordination_pattern": "observational_learning",
    "agents": [
        {"role": "Process Observer", "capabilities": ["document_expert_workflows", "capture_decision_making", "record_interactions"]},
        {"role": "Pattern Extractor", "capabilities": ["identify_decision_rules", "extract_implicit_knowledge", "map_workflows"]},
        {"role": "Training Creator", "capabilities": ["build_training_guides", "create_onboarding_materials", "design_learning_paths"]},
        {"role": "Performance Coach", "capabilities": ["provide_real_time_guidance", "give_feedback", "track_progress"]}
    ]
}
```

**5. Market Intelligence Team**
- **Use Case**: Monitor competitive landscape continuously
- **Target Metric**: Track 50 competitors with daily updates
```python
MARKET_INTELLIGENCE_TEMPLATE = {
    "name": "Market Intelligence Team",
    "coordination_pattern": "continuous_monitoring",
    "agents": [
        {"role": "Signal Scanner", "capabilities": ["monitor_news", "track_social_media", "watch_job_posts", "scan_patents"]},
        {"role": "Change Detector", "capabilities": ["identify_market_shifts", "detect_strategy_changes", "spot_new_entrants"]},
        {"role": "Impact Assessor", "capabilities": ["analyze_business_implications", "assess_competitive_threats", "evaluate_opportunities"]},
        {"role": "Brief Builder", "capabilities": ["create_daily_summaries", "generate_weekly_reports", "produce_intelligence_briefs"]}
    ]
}
```

**5. Custom Teams**: User-defined configurations
```python
class CustomTeamBuilder:
    def create_team(self, team_spec: TeamSpecification) -> Team:
        """Allow users to define custom agent roles, capabilities, coordination rules"""
        return Team(
            name=team_spec.name,
            agents=[self.create_agent(agent_spec) for agent_spec in team_spec.agents],
            coordination_pattern=team_spec.coordination_pattern,
            communication_rules=team_spec.communication_rules,
            goal=team_spec.goal
        )
```

### 3.3 Session Entity

**Purpose**: Represents a single execution of a task by a team.

```python
class Session:
    id: UUID
    team_id: UUID
    task_description: str        # Natural language task
    status: SessionStatus        # pending, running, completed, failed
    start_time: datetime
    end_time: Optional[datetime]
    metrics: Dict               # Performance measurements
    configuration: Dict         # Snapshot of team config
    user_id: Optional[UUID]     # For authentication
```

**Key Design Decisions**:
- **Configuration Snapshot**: Immutable record of team state at execution
- **Metrics Dictionary**: Flexible schema for different measurement types
- **Status Enum**: Clear lifecycle management

### 3.4 Message Entity

**Purpose**: Records all communications between agents and with humans.

```python
class Message:
    id: UUID
    session_id: UUID
    sender_id: Optional[UUID]    # Agent ID or None for human
    recipient_id: Optional[UUID] # Agent ID or None for broadcast
    message_type: MessageType    # direct, broadcast, request, response
    content: str
    metadata: Dict              # Reasoning traces, confidence, etc.
    timestamp: datetime
```

**Key Design Decisions**:
- **Optional Sender/Recipient**: Supports human-agent and broadcast communication
- **Message Types**: Structured communication patterns
- **Metadata Dictionary**: Extensible for reasoning traces and debug info

---

## 4. Agent Architecture

### 4.1 Agent State Model

```python
class AgentState:
    # Core Identity
    identity: AgentIdentity      # name, role, capabilities
    
    # Working Memory (Session-specific)
    current_task: Optional[str]
    context: Dict[str, Any]      # Current conversation context
    active_goals: List[str]
    
    # Long-term Memory
    episodic_memory: List[Episode]    # Specific past interactions
    semantic_memory: Dict[str, float] # General knowledge patterns
    
    # Communication State
    message_queue: List[Message]
    waiting_for_response: bool
    
    # Performance Tracking
    success_rate: float
    learning_metrics: Dict
```

### 4.2 Agent Lifecycle

```
Initialize → Configure → Activate → Execute → Respond → Learn → Persist
     ↑                                                              ↓
     └──────────────────── Feedback Loop ←─────────────────────────┘
```

**Phases**:
1. **Initialize**: Load agent configuration and memory
2. **Configure**: Apply session-specific settings
3. **Activate**: Begin monitoring for tasks/messages
4. **Execute**: Process assigned tasks using capabilities
5. **Respond**: Generate outputs and communicate with team
6. **Learn**: Update memory based on feedback
7. **Persist**: Save state changes to database

### 4.3 Shadow Agent Learning System (Major New Feature from PRD v22)

**Core Concept**: Transform customer onboarding into a knowledge capture process where agents learn by observing real human work before taking over tasks autonomously.

#### Learning Phases Architecture

**Phase 1: Shadow Mode (Weeks 1-2)**
```python
class ShadowMode:
    def __init__(self):
        self.observation_mode = True
        self.customer_interaction = False
        self.pattern_recognition = PatternRecognizer()
        self.knowledge_capture = KnowledgeCapture()
    
    async def observe_interaction(self, human_session: HumanSession):
        """Watch human interactions without participating"""
        patterns = await self.pattern_recognition.identify_patterns(human_session)
        await self.knowledge_capture.document_procedures(patterns)
        return ObservationResult(
            patterns_identified=patterns,
            confidence_scores=self.calculate_confidence(patterns),
            risk_level="zero"  # No customer-facing actions
        )
```

**Phase 2: Suggestion Mode (Weeks 3-4)**
```python
class SuggestionMode:
    def __init__(self):
        self.suggest_actions = True
        self.require_human_approval = True
        self.learning_tracker = LearningTracker()
    
    async def propose_response(self, ticket: SupportTicket) -> Suggestion:
        """Suggest responses for human review"""
        suggestion = await self.generate_suggestion(ticket)
        return Suggestion(
            proposed_action=suggestion,
            confidence_score=self.calculate_confidence(suggestion),
            requires_approval=True
        )
    
    async def learn_from_edit(self, suggestion: Suggestion, human_edit: HumanEdit):
        """Learn why humans modify suggestions"""
        await self.learning_tracker.record_modification(suggestion, human_edit)
        await self.update_patterns_from_feedback(human_edit)
```

**Phase 3: Assisted Mode (Week 5+)**
```python
class AssistedMode:
    def __init__(self):
        self.autonomous_threshold = 0.85  # Confidence threshold for autonomy
        self.escalation_rules = EscalationRules()
        
    async def handle_ticket(self, ticket: SupportTicket) -> ActionResult:
        """Handle tickets autonomously or escalate"""
        confidence = await self.assess_confidence(ticket)
        
        if confidence >= self.autonomous_threshold:
            return await self.handle_autonomously(ticket)
        else:
            return await self.escalate_to_human(ticket, confidence)
    
    async def expand_coverage(self):
        """Gradually increase autonomous scope"""
        successful_patterns = await self.analyze_success_patterns()
        await self.update_autonomous_capabilities(successful_patterns)
```

#### Knowledge Capture Components

**SOP Discovery System**
```python
class SOPDiscoverySystem:
    def __init__(self):
        self.document_analyzer = DocumentAnalyzer()
        self.interaction_recorder = InteractionRecorder()
        self.decision_mapper = DecisionMapper()
        
    async def discover_procedures(self) -> List[SOP]:
        """Extract standard operating procedures from observations"""
        documents = await self.document_analyzer.ingest_existing_docs()
        interactions = await self.interaction_recorder.capture_sessions()
        decisions = await self.decision_mapper.map_decision_trees()
        
        return await self.synthesize_sops(documents, interactions, decisions)
```

**Learning Data Model**
```python
class LearningSession:
    interaction_id: str
    human_actions: List[Action]
    agent_observations: List[Observation]
    patterns_identified: List[Pattern]
    confidence_scores: Dict[str, float]
    human_annotations: List[Annotation]
    learning_phase: LearningPhase  # shadow, suggestion, assisted
    
class LearningProgress:
    week: int
    phase: LearningPhase
    tickets_observed: int
    patterns_learned: int
    suggestion_accuracy: Optional[float]
    autonomous_coverage: float
    
class PatternLearning:
    pattern_type: str  # workflow, language, decision_rule, exception
    confidence: float
    examples: List[Example]
    validation_count: int
    last_updated: datetime
```

### 4.4 Traditional Memory Architecture

**Decision**: Implement hybrid memory system enhanced with shadow learning capabilities.

```python
class AgentMemory:
    # Shadow Learning Memory
    shadow_observations: List[ShadowObservation]
    learned_procedures: Dict[str, SOP]
    confidence_map: Dict[str, float]
    
    # Episodic Memory - Specific experiences
    episodes: List[Episode]
    max_episodes: int = 1000
    
    # Semantic Memory - Learned patterns
    patterns: Dict[str, MemoryPattern]
    confidence_threshold: float = 0.7
    
    # Working Memory - Current session
    context_window: List[Message]
    max_context_length: int = 4000  # tokens
    
    def retrieve_relevant(self, query: str) -> List[MemoryItem]:
        """Retrieve memories relevant to current task including shadow learnings"""
        traditional_memories = self._search_episodic_semantic(query)
        shadow_learnings = self._search_shadow_patterns(query)
        return self._merge_and_rank(traditional_memories, shadow_learnings)
    
    def update_from_shadow_learning(self, observation: ShadowObservation):
        """Update memory from shadow learning observations"""
        self.shadow_observations.append(observation)
        if observation.confidence > self.confidence_threshold:
            self._consolidate_to_semantic_memory(observation)
```

**Key Design Decisions for Shadow Learning**:
- **Three-phase progression** ensures gradual capability building
- **Confidence-based autonomy** prevents premature independent action
- **Continuous learning** allows ongoing improvement post-deployment
- **Zero-risk shadow phase** protects customers during initial learning

---

## 5. Communication Architecture

### 5.1 Communication Patterns

**1. Direct Messaging**
```python
# Agent A sends specific request to Agent B
message = DirectMessage(
    sender=agent_a,
    recipient=agent_b,
    content="Please analyze this data and provide insights",
    data={"csv_content": "..."}
)
```

**2. Broadcast Communication**
```python
# Agent announces to entire team
message = BroadcastMessage(
    sender=agent_a,
    content="I've completed the research phase",
    metadata={"phase": "research", "status": "complete"}
)
```

**3. Request/Response Pattern**
```python
# Structured task delegation
request = TaskRequest(
    requester=agent_a,
    assignee=agent_b,
    task_type="analyze",
    parameters={"method": "statistical", "confidence": 0.95},
    deadline=datetime.now() + timedelta(minutes=5)
)
```

### 5.2 Coordination Patterns

**Hierarchical Coordination**
- Designated team leader assigns and coordinates tasks
- Clear authority structure
- Efficient for well-defined workflows

**Peer-to-Peer Coordination**
- Agents negotiate task distribution
- Democratic decision-making
- Better for creative/exploratory tasks

**Pipeline Coordination**
- Sequential task handoffs
- Each agent has specific role in pipeline
- Optimal for linear workflows

### 5.3 Conflict Resolution

**Decision**: Implement explicit conflict resolution mechanisms.

```python
class ConflictResolver:
    def resolve_capability_conflict(self, task: Task, candidates: List[Agent]):
        """When multiple agents can handle a task"""
        return self._select_by_expertise_score(candidates, task)
    
    def resolve_resource_conflict(self, resource: str, requesters: List[Agent]):
        """When multiple agents need same resource"""
        return self._queue_by_priority(requesters)
    
    def resolve_opinion_conflict(self, opinions: List[AgentOpinion]):
        """When agents disagree on approach/answer"""
        return self._weighted_consensus(opinions)
```

---

## 6. LLM Integration Architecture

### 6.1 Claude API Integration

**Design Decision**: Wrap Claude API in service layer for consistency and monitoring.

```python
class ClaudeService:
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.rate_limiter = RateLimiter(requests_per_minute=60)
        self.token_tracker = TokenUsageTracker()
    
    async def generate_response(
        self,
        messages: List[Message],
        agent_context: AgentContext,
        max_tokens: int = 1024
    ) -> AgentResponse:
        """Generate agent response with context and constraints"""
        
        # Build prompt with agent identity and context
        prompt = self._build_agent_prompt(agent_context, messages)
        
        # Apply rate limiting
        await self.rate_limiter.acquire()
        
        # Call Claude API
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=prompt
        )
        
        # Track token usage
        self.token_tracker.record(response.usage)
        
        return self._parse_agent_response(response)
```

### 6.2 Prompt Engineering Strategy

**Agent Identity Prompts**
```python
AGENT_PROMPT_TEMPLATE = """
You are {agent_name}, a {agent_role} with the following capabilities: {capabilities}.

Your current goals are:
{goals}

You must operate within these constraints:
{constraints}

Your beliefs about the current situation:
{beliefs}

Recent team communications:
{recent_messages}

Current task: {current_task}

Respond as {agent_name} would, using your capabilities to advance the team's goals.
"""
```

**Assumptions**:
- **Clear agent identity** in prompts improves role consistency
- **Explicit capabilities** help constrain agent behavior appropriately
- **Recent context** is more important than full conversation history
- **Structured output** can be encouraged through prompt design

### 6.3 Token Management

**Strategy**: Implement aggressive token optimization for cost control.

```python
class TokenManager:
    MAX_CONTEXT_TOKENS = 8000      # Per agent per session
    SUMMARY_THRESHOLD = 6000       # When to summarize context
    
    def optimize_context(self, messages: List[Message]) -> List[Message]:
        """Compress context when approaching token limits"""
        if self.estimate_tokens(messages) > self.SUMMARY_THRESHOLD:
            return self._summarize_older_messages(messages)
        return messages
    
    def _summarize_older_messages(self, messages: List[Message]) -> List[Message]:
        """Keep recent messages, summarize older ones"""
        recent = messages[-10:]  # Keep last 10 messages
        older = messages[:-10]
        
        summary = self._generate_summary(older)
        return [summary] + recent
```

---

## 7. Data Architecture

### 7.1 Database Schema Design

**Core Tables**:
```sql
-- Agents table
CREATE TABLE agents (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    capabilities JSONB DEFAULT '[]',
    beliefs JSONB DEFAULT '{}',
    goals JSONB DEFAULT '[]',
    constraints JSONB DEFAULT '[]',
    memory JSONB DEFAULT '{}',
    template_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Teams table
CREATE TABLE teams (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    coordination_pattern VARCHAR(50),
    communication_rules JSONB DEFAULT '{}',
    shared_memory JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Team membership
CREATE TABLE team_members (
    team_id UUID REFERENCES teams(id),
    agent_id UUID REFERENCES agents(id),
    role VARCHAR(50),
    joined_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (team_id, agent_id)
);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    team_id UUID REFERENCES teams(id),
    task_description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    metrics JSONB DEFAULT '{}',
    configuration JSONB DEFAULT '{}',
    user_id UUID
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    sender_id UUID REFERENCES agents(id),
    recipient_id UUID REFERENCES agents(id),
    message_type VARCHAR(20),
    content TEXT,
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### 7.2 Data Flow Architecture

```
User Input → Session Creation → Team Activation → Agent Execution → Message Logging → Results Collection
                     ↓                ↓                ↓               ↓                ↓
              PostgreSQL       Redis Cache      Claude API     PostgreSQL       Analytics
```

**Design Decisions**:
- **JSONB for flexibility**: Allows schema evolution without migrations
- **UUID for all IDs**: Enables distributed systems later
- **Separate team membership**: Supports agents in multiple teams
- **Message metadata**: Extensible for reasoning traces and debug info

### 7.3 Caching Strategy

**Redis Usage**:
```python
# Session state caching
session_key = f"session:{session_id}"
redis.hset(session_key, {
    "active_agents": json.dumps(agent_ids),
    "current_task": task_description,
    "message_queue": json.dumps(pending_messages),
    "last_activity": datetime.now().isoformat()
})
redis.expire(session_key, 3600)  # 1 hour TTL

# Agent state caching
agent_key = f"agent:{agent_id}:session:{session_id}"
redis.hset(agent_key, {
    "working_memory": json.dumps(context),
    "status": "active",
    "last_message_id": last_msg_id
})
```

**Assumptions**:
- **Session state** changes frequently and benefits from caching
- **Agent working memory** is session-specific and can be cached
- **1-hour TTL** balances memory usage with session length
- **Redis pub/sub** can handle real-time message distribution

---

## 8. Performance & Scalability Assumptions

### 8.1 Performance Requirements (from PRD)

| **Metric** | **Target** | **Design Implication** |
|------------|------------|------------------------|
| Response Time | < 5 seconds | Async processing, request queuing |
| Concurrent Sessions | 20+ | Connection pooling, resource limits |
| Message Throughput | 100+ msgs/min | Efficient WebSocket handling |
| Storage per Session | 1GB | Optimized message storage |

### 8.2 Scalability Constraints

**Current Architecture Limits**:
- **Single Backend Instance**: No horizontal scaling
- **Shared PostgreSQL**: Potential bottleneck for high concurrency
- **In-Memory Session State**: Limited by server RAM
- **Synchronous Agent Processing**: Sequential execution within teams

**Future Scaling Strategies** (Out of Scope):
- Microservices architecture for agent execution
- Database sharding by session/team
- Distributed caching with Redis Cluster
- Async agent processing with message queues

### 8.3 Resource Management

```python
class ResourceManager:
    MAX_CONCURRENT_SESSIONS = 20
    MAX_AGENTS_PER_SESSION = 10
    MAX_MESSAGES_PER_MINUTE = 100
    
    def __init__(self):
        self.session_semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_SESSIONS)
        self.rate_limiters = {}
    
    async def acquire_session_slot(self) -> bool:
        """Acquire permission to start new session"""
        return await self.session_semaphore.acquire()
    
    def get_rate_limiter(self, session_id: str) -> RateLimiter:
        """Get rate limiter for specific session"""
        if session_id not in self.rate_limiters:
            self.rate_limiters[session_id] = RateLimiter(
                requests_per_minute=self.MAX_MESSAGES_PER_MINUTE
            )
        return self.rate_limiters[session_id]
```

---

## 9. Security & Authentication Design

### 9.1 Authentication Strategy

**Decision**: Magic link authentication for simplicity in research prototype.

```python
class AuthenticationService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.pending_logins = {}  # In-memory for prototype
    
    async def request_login(self, email: str) -> bool:
        """Send magic link to user email"""
        token = self._generate_secure_token()
        magic_link = f"{settings.FRONTEND_URL}/auth/verify?token={token}"
        
        # Store pending login
        self.pending_logins[token] = {
            "email": email,
            "expires_at": datetime.now() + timedelta(minutes=15)
        }
        
        # Send email
        await self.email_service.send_magic_link(email, magic_link)
        return True
    
    def verify_token(self, token: str) -> Optional[User]:
        """Verify magic link token and create session"""
        if token in self.pending_logins:
            login_data = self.pending_logins[token]
            if datetime.now() < login_data["expires_at"]:
                del self.pending_logins[token]
                return self._create_or_get_user(login_data["email"])
        return None
```

### 9.2 Authorization Model

**Simple Role-Based Access**:
- **Anonymous**: Can view public demos
- **Authenticated**: Can create sessions and teams
- **Admin**: Can view all sessions and system metrics

**Assumptions**:
- **Research prototype** doesn't need complex permissions
- **Email-based identity** is sufficient for user tracking
- **No sensitive data** requiring encryption at rest
- **Rate limiting** provides basic protection against abuse

### 9.3 Data Privacy

**Minimal Data Collection**:
- Email addresses for authentication only
- Session data for research analysis
- No personal information in agent configurations
- Automatic data expiration after research period

---

## 10. Test Scenarios & Research Framework

### 10.1 Core Test Scenarios (from PRD v22)

**Scenario 1: Customer Support Excellence**
- **Team**: Customer Success Response Team
- **Task**: Handle 20 real support tickets across billing, technical, and feature requests
- **Metrics**: Resolution time, accuracy, escalation rate, customer satisfaction
- **Target**: Resolve tickets in 2 minutes vs 20 minutes
- **Architecture Requirement**: Sequential pipeline with escalation routing

**Scenario 2: RFP Response Speed**
- **Team**: RFP/Proposal Acceleration Team
- **Task**: Complete comprehensive response to 30-page RFP
- **Metrics**: Completion time, requirement coverage, win rate, accuracy
- **Target**: Complete 50-page RFP in 1 hour vs 1 week
- **Architecture Requirement**: Parallel assembly with compliance validation

**Scenario 3: Product Feedback Synthesis**
- **Team**: Product Intelligence Team  
- **Task**: Analyze 500 customer feedback items from multiple channels
- **Metrics**: Insight quality, pattern identification, actionability score
- **Target**: Process 1,000 inputs into 5 insights daily
- **Architecture Requirement**: Parallel collection with intelligent synthesis

**Scenario 4: Competitive Intelligence**
- **Team**: Market Intelligence Team
- **Task**: Monitor 10 competitors for one week, produce daily briefs
- **Metrics**: Signal detection rate, relevance, timeliness, actionability
- **Target**: Track 50 competitors with daily updates
- **Architecture Requirement**: Continuous monitoring with impact assessment

**Scenario 5: Knowledge Preservation**
- **Team**: Knowledge Transfer Team
- **Task**: Document and teach complex multi-step process
- **Metrics**: Accuracy, completeness, new hire success rate
- **Target**: Reduce onboarding time from 3 months to 3 weeks
- **Architecture Requirement**: Observational learning with progressive autonomy

### 10.1.1 Custom Scenario Builder (from PRD)

**Requirements**: Allow users to define custom test scenarios with:
- Agent roles and capabilities
- Task descriptions and success criteria  
- Coordination rules
- Evaluation metrics

```python
class CustomScenarioBuilder:
    def create_scenario(self, scenario_spec: ScenarioSpecification) -> TestScenario:
        """Build custom test scenario from user specification"""
        return TestScenario(
            name=scenario_spec.name,
            description=scenario_spec.description,
            team_configuration=self.build_team(scenario_spec.team_spec),
            task_definition=TaskDefinition(
                description=scenario_spec.task_description,
                success_criteria=scenario_spec.success_criteria,
                complexity_level=scenario_spec.complexity  # Simple, Compound, Creative, Strategic
            ),
            evaluation_metrics=scenario_spec.metrics,
            coordination_rules=scenario_spec.coordination_rules
        )

class ScenarioSpecification:
    name: str
    description: str
    team_spec: TeamSpecification
    task_description: str
    success_criteria: List[str]
    complexity: TaskComplexity  # From PRD: Simple → Compound → Creative → Strategic
    metrics: List[EvaluationMetric]
    coordination_rules: Dict[str, Any]
```

**Example Shadow Learning Scenario** (from PRD v22 Appendix):
```yaml
scenario: "Customer Support Shadow Learning"
team:
  - name: "Triage Specialist"
    role: "Observe ticket categorization patterns"
    learning_focus: ["priority_detection", "routing_rules", "urgency_markers"]
  - name: "Solution Researcher"  
    role: "Learn knowledge base navigation"
    learning_focus: ["search_patterns", "doc_relevance", "solution_matching"]
  - name: "Response Crafter"
    role: "Learn communication style and tone"
    learning_focus: ["brand_voice", "empathy_patterns", "clarity_rules"]

phases:
  shadow:
    duration: "2 weeks"
    activities:
      - Observe 500+ ticket resolutions
      - Map decision trees for common issues
      - Identify undocumented workarounds
  
  suggestion:
    duration: "2 weeks"  
    activities:
      - Propose responses for human review
      - Track acceptance and modification rates
      - Learn from human corrections
      
  assisted:
    metrics:
      - autonomy_rate: "85% of routine tickets"
      - escalation_accuracy: "95% correct escalations"
      - time_savings: "18 minutes per ticket"
```

### 10.2 Hypothesis Testing Framework

**H1: Specialized Agents Outperform Generalists**
```python
class SpecializationTest:
    def run_comparison(self, task: Task):
        # Single generalist agent baseline
        generalist_result = await self.run_single_agent(
            agent=GeneralistAgent(), task=task
        )
        
        # Specialized team execution
        specialist_result = await self.run_team(
            team=self.get_specialist_team(task.domain), task=task
        )
        
        return ComparisonMetrics(
            task_completion_rate=specialist_result.success_rate / generalist_result.success_rate,
            quality_improvement=specialist_result.quality_score - generalist_result.quality_score,
            time_efficiency=generalist_result.duration / specialist_result.duration
        )
```

**H2: Agents Can Learn from Human Feedback**
```python
class LearningTest:
    async def measure_improvement(self, agent: Agent, feedback_sessions: int = 5):
        baseline_performance = await self.run_baseline_test(agent)
        
        for session in range(feedback_sessions):
            result = await self.run_task_with_feedback(agent)
            await self.apply_coaching_feedback(agent, result)
            
        final_performance = await self.run_final_test(agent)
        
        return LearningMetrics(
            error_reduction_rate=(baseline_performance.errors - final_performance.errors) / baseline_performance.errors,
            pattern_recognition_improvement=final_performance.pattern_score - baseline_performance.pattern_score,
            generalization_ability=await self.test_transfer_learning(agent)
        )
```

**H3: Transparent Reasoning Builds Trust**
```python
class TransparencyTest:
    async def measure_trust_impact(self, session: Session):
        # Run with explanation features
        transparent_session = await self.run_with_explanations(session)
        
        # Run without explanation features  
        opaque_session = await self.run_without_explanations(session)
        
        return TrustMetrics(
            trust_scores=await self.collect_user_trust_ratings(),
            adoption_rates=self.measure_feature_usage(),
            correction_frequency=transparent_session.corrections / opaque_session.corrections
        )
```

**H4: Agent Teams Can Self-Coordinate**
```python
class CoordinationTest:
    async def measure_self_coordination(self, team: Team, task: Task):
        coordination_result = await self.run_autonomous_coordination(team, task)
        
        return CoordinationMetrics(
            coordination_accuracy=coordination_result.correct_delegations / coordination_result.total_delegations,
            handoff_success_rate=coordination_result.successful_handoffs / coordination_result.total_handoffs,
            conflict_resolution_rate=coordination_result.resolved_conflicts / coordination_result.total_conflicts
        )
```

### 10.3 Success Metrics from PRD v22

**Technical Validation Targets**:
- **Coordination Success**: 70%+ multi-agent task completion
- **Learning Effectiveness**: 15%+ improvement after coaching  
- **Explanation Quality**: 85%+ reasoning accuracy
- **System Reliability**: 95%+ uptime

**Shadow Learning Metrics** (New in v22):
- **Knowledge Coverage**: Percentage of ticket types learned
- **Pattern Discovery**: New SOPs identified per week
- **Accuracy Progression**: Improvement in suggestion acceptance (target: 72% → 93%)
- **Time to Autonomy**: Days until agents handle tasks independently
- **Edge Case Handling**: Successful resolution of unusual scenarios

**Use Case Discovery Goals**:
- **High-Potential Cases**: Identify 3-5 with clear value
- **PMF Indicators**: Measurable improvement over single agent
- **Feasibility Assessment**: Technical readiness for production
- **Market Validation**: User excitement and willingness to pay

**Business Impact Targets** (from v22 Team Templates):
- **Customer Support**: 2 minutes vs 20 minutes resolution time
- **RFP Response**: 1 hour vs 1 week completion time
- **Product Intelligence**: 1,000 inputs → 5 insights daily
- **Knowledge Transfer**: 3 weeks vs 3 months onboarding time
- **Market Intelligence**: Track 50 competitors with daily updates

### 10.4 Monitoring & Observability

```python
class MetricsCollector:
    def __init__(self):
        self.prometheus_registry = CollectorRegistry()
        self.session_counter = Counter('kyoryoku_sessions_total')
        self.message_counter = Counter('kyoryoku_messages_total')
        self.response_time_histogram = Histogram('kyoryoku_response_time_seconds')
        self.agent_performance_gauge = Gauge('kyoryoku_agent_performance_score')
        
        # PRD-specific metrics
        self.coordination_success_rate = Gauge('kyoryoku_coordination_success_rate')
        self.learning_improvement_rate = Gauge('kyoryoku_learning_improvement_rate')
        self.explanation_accuracy = Gauge('kyoryoku_explanation_accuracy')
    
    def record_hypothesis_test_result(self, hypothesis: str, result: TestResult):
        """Record results for each core hypothesis"""
        self.hypothesis_results.labels(hypothesis=hypothesis).set(result.success_score)
        
    def record_scenario_completion(self, scenario: str, team_config: str, success: bool):
        """Track completion rates by scenario and team configuration"""
        self.scenario_success.labels(
            scenario=scenario, 
            team_config=team_config
        ).inc() if success else self.scenario_failure.labels(
            scenario=scenario,
            team_config=team_config
        ).inc()
```

### 10.5 Research Analytics Pipeline

**Key Metrics for Research Questions**:
- **Optimal Team Size**: Success rate vs. team size by task type
- **Context Sharing Effectiveness**: Information retention across agent handoffs  
- **Feedback Mechanism Efficiency**: Learning rate by feedback type
- **Coordination Protocol Breakdown Points**: Failure modes by coordination pattern

### 10.3 Error Handling & Logging

```python
import structlog

logger = structlog.get_logger()

class AgentExecutionService:
    async def execute_task(self, agent: Agent, task: Task) -> TaskResult:
        try:
            logger.info("Starting task execution", 
                       agent_id=agent.id, task_type=task.type)
            
            result = await self._execute_with_timeout(agent, task)
            
            logger.info("Task completed successfully",
                       agent_id=agent.id, duration=result.duration)
            return result
            
        except TimeoutError:
            logger.error("Task execution timeout",
                        agent_id=agent.id, timeout=task.timeout)
            return TaskResult.timeout()
            
        except Exception as e:
            logger.error("Task execution failed",
                        agent_id=agent.id, error=str(e), exc_info=True)
            return TaskResult.error(str(e))
```

---

## 11. Technology Choices & Rationale

### 11.1 Backend Technology Stack

| **Component** | **Choice** | **Alternative Considered** | **Rationale** |
|---------------|------------|---------------------------|---------------|
| **Web Framework** | FastAPI | Django, Flask | Async support, automatic OpenAPI docs |
| **Database** | PostgreSQL | MongoDB, SQLite | JSONB support, ACID properties for research data |
| **ORM** | SQLAlchemy | Django ORM, Tortoise | Mature async support, flexibility |
| **Cache** | Redis | Memcached, In-memory | Pub/sub for real-time, data structures |
| **AI Orchestration** | LangGraph | Custom, LangChain | Purpose-built for agent workflows |
| **WebSocket** | Socket.io | Native WebSocket | Mature ecosystem, fallback support |

### 11.2 Frontend Technology Stack

| **Component** | **Choice** | **Alternative Considered** | **Rationale** |
|---------------|------------|---------------------------|---------------|
| **Framework** | React 18 | Vue, Svelte | Large ecosystem, TypeScript support |
| **Build Tool** | Vite | Create React App, Webpack | Fast development, modern tooling |
| **State Management** | React Context + Hooks | Redux, Zustand | Sufficient for prototype complexity |
| **UI Library** | Custom Components | Material-UI, Chakra | Full control for research UI needs |
| **Real-time** | Socket.io Client | Native WebSocket | Matches backend choice |

### 11.3 Infrastructure Choices

| **Component** | **Choice** | **Alternative Considered** | **Rationale** |
|---------------|------------|---------------------------|---------------|
| **Deployment** | Docker Compose | Kubernetes, Serverless | Simple for single-machine prototype |
| **Auth Provider** | Custom Magic Links | Auth0, Firebase | Research prototype simplicity |
| **Email Service** | SMTP | SendGrid, AWS SES | Cost-effective for low volume |
| **Monitoring** | Prometheus + Custom | DataDog, New Relic | Open source, research data ownership |

---

## 12. Risk Assessment & Mitigation

### 12.1 Technical Risks

| **Risk** | **Probability** | **Impact** | **Mitigation** |
|----------|----------------|------------|----------------|
| **Claude API Rate Limits** | High | High | Implement aggressive rate limiting, request queuing |
| **Database Performance** | Medium | Medium | Connection pooling, query optimization |
| **Memory Leaks in Long Sessions** | Medium | Medium | Session timeouts, periodic cleanup |
| **WebSocket Connection Issues** | Low | Medium | Automatic reconnection, fallback polling |

### 12.2 Research Risks

| **Risk** | **Probability** | **Impact** | **Mitigation** |
|----------|----------------|------------|----------------|
| **Insufficient Agent Coordination** | Medium | High | Multiple coordination patterns, fallback to single agent |
| **Poor Learning from Feedback** | Medium | Medium | Multiple feedback mechanisms, manual pattern curation |
| **Limited Use Case Validation** | Low | High | Diverse test scenarios, external user testing |

### 12.3 Product Risks

| **Risk** | **Probability** | **Impact** | **Mitigation** |
|----------|----------------|------------|----------------|
| **No Clear PMF Indicators** | Medium | High | Multiple metrics, qualitative feedback collection |
| **Technical Debt Impedes Research** | High | Medium | Regular refactoring, clear architecture boundaries |
| **Prototype Not Scalable** | High | Low | Document scaling requirements, architecture evolution path |

---

## 13. Evolution & Future Considerations

### 13.1 Architecture Evolution Path

**Phase 1 (Current)**: Monolithic prototype
- Single backend service
- Shared database
- Synchronous agent execution

**Phase 2 (Scaling)**: Service-oriented
- Agent execution service
- Coordination service
- Analytics service

**Phase 3 (Production)**: Microservices
- Independent agent containers
- Event-driven architecture
- Distributed state management

### 13.2 Technical Debt Management

**Acceptable Debt for Research Phase**:
- Hardcoded configuration values
- Simple error handling
- Manual deployment processes
- Basic monitoring setup

**Must Address Before Scaling**:
- Database query optimization
- Comprehensive test coverage
- Security hardening
- Automated deployment pipeline

---

## 14. Appendices

### 14.1 Glossary

- **Agent**: AI entity with specific capabilities and goals
- **Team**: Collection of agents with coordination rules
- **Session**: Single execution of a task by a team
- **Coordination Pattern**: Rules governing how agents interact
- **Episode**: Specific memory of past interaction
- **Capability**: Skill or function an agent can perform

### 14.2 References

- [Kyoryoku PRD v2.0](./ai-team-studio-prd.md)
- [Development Plan](./DEVELOPMENT_PLAN.md)
- [Claude Code Setup](./CLAUDE.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

**Document Status**: Living document, updated throughout development
**Next Review**: Weekly during active development
**Owner**: Claude Development Agent