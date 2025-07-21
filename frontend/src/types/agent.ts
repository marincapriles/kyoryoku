export interface Agent {
  id: string;
  name: string;
  description?: string;
  capabilities: string[];
  beliefs: Record<string, number>;
  goals: string[];
  constraints: string[];
  memory: Record<string, any>;
  template_type?: string;
  created_at: string;
  updated_at: string;
}

export interface AgentCreate {
  name: string;
  description?: string;
  capabilities: string[];
  beliefs?: Record<string, number>;
  goals?: string[];
  constraints?: string[];
  memory?: Record<string, any>;
  template_type?: string;
}

export interface AgentTemplate {
  name: string;
  description: string;
  template_type: string;
  capabilities: string[];
  default_goals: string[];
  constraints: string[];
}

export interface TeamTemplate {
  name: string;
  description: string;
  use_case: string;
  target_metric: string;
  coordination_pattern: string;
  agents: Array<{
    role: string;
    capabilities: string[];
  }>;
}