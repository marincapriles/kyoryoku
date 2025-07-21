# Kyoryoku - Content Creation Team Scope Addition

## Overview
Add a pre-configured "Content Creation Team" template to demonstrate Kyoryoku's capabilities through practical use. This team will be used to write blog posts, documentation, and marketing content about Kyoryoku itself, serving as both a feature and a demonstration.

## Business Justification
- **Dogfooding**: Use our own product to create content about the product
- **Demo Power**: Perfect showcase of multi-agent collaboration
- **Immediate Value**: Helps with actual marketing/documentation needs
- **Meta Storytelling**: The product literally tells its own story

## Implementation Requirements

### 1. New Team Template: Content Creation Squad

Add to the existing team templates in `backend/app/services/template_service.py`:

```python
{
    "name": "Content Creation Squad",
    "description": "Transform ideas into engaging content through specialized collaboration",
    "template_type": "content_creation",
    "coordination_pattern": "iterative_refinement",
    "agents": [
        {
            "role": "Story Miner",
            "capabilities": [
                "analyze_source_material",
                "identify_key_moments", 
                "extract_narratives",
                "find_emotional_arcs"
            ],
            "prompts": {
                "init": "You extract compelling stories and key moments from source material.",
                "analyze": "Find the most interesting and relatable moments in this content."
            }
        },
        {
            "role": "Technical Translator",
            "capabilities": [
                "simplify_complex_concepts",
                "create_analogies",
                "remove_jargon",
                "explain_clearly"
            ],
            "prompts": {
                "init": "You make technical concepts accessible to general audiences.",
                "translate": "Explain this concept like you're talking to a smart friend who isn't technical."
            }
        },
        {
            "role": "Voice Crafter", 
            "capabilities": [
                "maintain_tone",
                "inject_personality",
                "balance_formality",
                "ensure_authenticity"
            ],
            "prompts": {
                "init": "You ensure content sounds personal, authentic, and engaging.",
                "refine": "Make this sound like a founder sharing their journey, not a corporation."
            }
        },
        {
            "role": "Structure Architect",
            "capabilities": [
                "organize_flow",
                "create_transitions",
                "ensure_coherence",
                "optimize_narrative_arc"
            ],
            "prompts": {
                "init": "You organize ideas into compelling narrative structures.",
                "structure": "Arrange these ideas for maximum impact and readability."
            }
        },
        {
            "role": "Hook Designer",
            "capabilities": [
                "craft_openings",
                "create_cliffhangers",
                "design_cta",
                "maintain_momentum"
            ],
            "prompts": {
                "init": "You create attention-grabbing hooks and maintain reader engagement.",
                "hook": "Add elements that make people need to keep reading."
            }
        }
    ]
}
```

### 2. New Coordination Pattern: Iterative Refinement

Add to `backend/app/agents/coordination_patterns.py`:

```python
class IterativeRefinementPattern(CoordinationPattern):
    """
    Agents work in rounds, each building on the previous agent's work.
    Perfect for creative processes where each specialist improves the output.
    """
    
    async def execute(self, task: Task, team: Team) -> Result:
        # Round 1: Story Mining
        story_elements = await team.agents['Story Miner'].extract_stories(task.source_material)
        
        # Round 2: Structure
        structured_draft = await team.agents['Structure Architect'].organize(story_elements)
        
        # Round 3: Translation
        readable_draft = await team.agents['Technical Translator'].simplify(structured_draft)
        
        # Round 4: Voice
        personality_draft = await team.agents['Voice Crafter'].add_voice(readable_draft)
        
        # Round 5: Hooks
        final_draft = await team.agents['Hook Designer'].add_engagement(personality_draft)
        
        # Allow for additional refinement rounds based on feedback
        return final_draft
```

### 3. Content Creation Specific Features

#### 3.1 Source Material Ingestion
```python
class ContentCreationSession(Session):
    source_materials: List[SourceMaterial]  # Conversations, docs, examples
    target_audience: str                    # Who we're writing for
    content_type: str                       # blog_post, documentation, pitch
    voice_samples: List[str]                # Previous writing examples
    iteration_count: int = 0                # Track refinement rounds
```

#### 3.2 Collaboration Visibility
Show how agents negotiate and build on each other's work:

```python
class AgentNegotiation:
    agent_1: str
    agent_2: str
    conflict: str      # "Too technical" vs "Needs accuracy"
    resolution: str    # "Added analogy while keeping facts"
    timestamp: datetime
```

#### 3.3 Process Documentation
Automatically generate "how this was written" sections:

```python
def generate_process_story(session: ContentCreationSession) -> str:
    """
    Creates a meta-narrative about how the content was created.
    Shows which agent contributed what and why.
    """
    timeline = []
    for event in session.events:
        if event.type == "agent_contribution":
            timeline.append(f"{event.agent}: {event.contribution}")
    
    return format_as_story(timeline)
```

### 4. UI Components

#### 4.1 Content Creation Wizard
- Select content type (blog post, documentation, etc.)
- Upload source materials
- Define target audience
- Provide voice samples
- Set iteration preferences

#### 4.2 Real-time Collaboration View
```typescript
interface CollaborationView {
    currentDraft: string
    activeAgent: Agent
    agentThoughts: string[]      // Show reasoning
    suggestions: Suggestion[]     // Show alternatives considered
    negotiations: Negotiation[]   // Show agent debates
}
```

#### 4.3 Iteration Controls
- "Refine Further" button
- Specific agent feedback (e.g., "Make it funnier" → Voice Crafter)
- A/B comparison of drafts
- Highlight what changed between iterations

### 5. Demo Scenarios

#### 5.1 "Write About Yourself" Demo
```python
demo_task = {
    "type": "blog_post",
    "topic": "How Kyoryoku Works",
    "source_materials": [
        session_history,
        prd_document,
        user_conversations
    ],
    "target_audience": "Technical founders",
    "desired_outcome": "Compelling story about multi-agent collaboration"
}
```

#### 5.2 Documentation Generation
- Feed in code + conversations
- Generate user-friendly documentation
- Show how different agents contribute to clarity

### 6. Success Metrics
- Time to create content: 10 minutes vs 2 hours traditional
- Engagement metrics: Track if agent-written content performs better
- Iteration efficiency: How many rounds to reach satisfaction
- Voice consistency: Measure against provided samples

### 7. Database Schema Additions

```sql
-- Content creation specific tables
CREATE TABLE content_sessions (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    content_type VARCHAR(50),
    target_audience TEXT,
    final_output TEXT,
    iteration_count INTEGER,
    quality_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE content_sources (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES content_sessions(id),
    source_type VARCHAR(50), -- conversation, document, example
    source_content TEXT,
    relevance_score FLOAT
);

CREATE TABLE agent_negotiations (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    agent_1_id UUID REFERENCES agents(id),
    agent_2_id UUID REFERENCES agents(id),
    conflict_description TEXT,
    resolution TEXT,
    impact_on_output TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### 8. API Endpoints

```python
# New endpoints for content creation
POST   /api/content/create          # Start content creation session
GET    /api/content/{id}/progress   # Real-time progress updates
POST   /api/content/{id}/iterate    # Request another refinement round
GET    /api/content/{id}/history    # See how content evolved
POST   /api/content/{id}/feedback   # Provide specific agent feedback
```

### 9. Implementation Priority

1. **Week 1**: Basic content team template and agents
2. **Week 1**: Simple iterative refinement pattern
3. **Week 2**: UI for content creation wizard
4. **Week 2**: Process documentation generation
5. **Week 3**: Advanced features (negotiations, A/B testing)

### 10. Testing Strategy

- Create blog post about Kyoryoku's development
- Generate documentation from code comments
- Write investor pitch deck content
- Create user testimonials from session data
- Generate FAQ from common questions

This addition serves both as a feature and a demonstration of Kyoryoku's capabilities, making it perfect for early demos and attracting pilot customers.