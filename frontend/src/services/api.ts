import axios from 'axios';
import { Agent, AgentCreate, AgentTemplate, TeamTemplate } from '../types/agent';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const agentApi = {
  // Agent CRUD operations
  createAgent: async (agentData: AgentCreate): Promise<Agent> => {
    const response = await api.post('/api/agents/', agentData);
    return response.data;
  },

  createAgentFromTemplate: async (templateName: string, customName?: string): Promise<Agent> => {
    const response = await api.post(`/api/agents/from-template/${templateName}`, null, {
      params: { custom_name: customName }
    });
    return response.data;
  },

  listAgents: async (): Promise<Agent[]> => {
    const response = await api.get('/api/agents/');
    return response.data;
  },

  getAgent: async (agentId: string): Promise<Agent> => {
    const response = await api.get(`/api/agents/${agentId}`);
    return response.data;
  },

  updateAgent: async (agentId: string, agentData: Partial<AgentCreate>): Promise<Agent> => {
    const response = await api.put(`/api/agents/${agentId}`, agentData);
    return response.data;
  },

  deleteAgent: async (agentId: string): Promise<void> => {
    await api.delete(`/api/agents/${agentId}`);
  },

  // Template operations
  listAgentTemplates: async (): Promise<AgentTemplate[]> => {
    const response = await api.get('/api/agents/templates');
    return response.data;
  },

  listTeamTemplates: async (): Promise<TeamTemplate[]> => {
    const response = await api.get('/api/agents/team-templates');
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/api/health/');
    return response.data;
  }
};

export default api;