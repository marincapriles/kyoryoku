import React, { useState, useEffect } from 'react';
import { Agent, AgentTemplate, TeamTemplate } from '../types/agent';
import { agentApi } from '../services/api';
import AgentCard from '../components/AgentCard';
import AgentTemplateSelector from '../components/AgentTemplateSelector';

const AgentDashboard: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTemplateSelector, setShowTemplateSelector] = useState(false);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const agentsData = await agentApi.listAgents();
      setAgents(agentsData);
      setError(null);
    } catch (err) {
      setError('Failed to load agents');
      console.error('Error loading agents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAgentTemplate = async (template: AgentTemplate) => {
    try {
      const newAgent = await agentApi.createAgentFromTemplate(template.name);
      setAgents([...agents, newAgent]);
      setShowTemplateSelector(false);
    } catch (err) {
      setError('Failed to create agent from template');
      console.error('Error creating agent:', err);
    }
  };

  const handleSelectTeamTemplate = async (template: TeamTemplate) => {
    try {
      // Create all agents from the team template
      const newAgents = await Promise.all(
        template.agents.map(agentConfig => 
          agentApi.createAgentFromTemplate(agentConfig.role, `${template.name} - ${agentConfig.role}`)
        )
      );
      setAgents([...agents, ...newAgents]);
      setShowTemplateSelector(false);
    } catch (err) {
      setError('Failed to create team from template');
      console.error('Error creating team:', err);
    }
  };

  const handleDeleteAgent = async (agentId: string) => {
    if (!confirm('Are you sure you want to delete this agent?')) {
      return;
    }

    try {
      await agentApi.deleteAgent(agentId);
      setAgents(agents.filter(agent => agent.id !== agentId));
    } catch (err) {
      setError('Failed to delete agent');
      console.error('Error deleting agent:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading agents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Kyoryoku Agent Dashboard</h1>
              <p className="text-gray-600 mt-1">Manage your AI agents and teams</p>
            </div>
            <button
              onClick={() => setShowTemplateSelector(!showTemplateSelector)}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              {showTemplateSelector ? 'Hide Templates' : 'Add Agent/Team'}
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Template Selector */}
        {showTemplateSelector && (
          <div className="mb-8">
            <AgentTemplateSelector
              onSelectAgentTemplate={handleSelectAgentTemplate}
              onSelectTeamTemplate={handleSelectTeamTemplate}
            />
          </div>
        )}

        {/* Agents Grid */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Your Agents ({agents.length})
            </h2>
            <button
              onClick={loadAgents}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Refresh
            </button>
          </div>

          {agents.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg
                  className="mx-auto h-12 w-12"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No agents yet</h3>
              <p className="text-gray-600 mb-4">
                Get started by creating your first agent or team from a template.
              </p>
              <button
                onClick={() => setShowTemplateSelector(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Create Your First Agent
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents.map((agent) => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  onDelete={handleDeleteAgent}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard;