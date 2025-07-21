import React, { useState, useEffect } from 'react';
import { AgentTemplate, TeamTemplate } from '../types/agent';
import { agentApi } from '../services/api';

interface AgentTemplateSelectorProps {
  onSelectAgentTemplate?: (template: AgentTemplate) => void;
  onSelectTeamTemplate?: (template: TeamTemplate) => void;
}

const AgentTemplateSelector: React.FC<AgentTemplateSelectorProps> = ({
  onSelectAgentTemplate,
  onSelectTeamTemplate,
}) => {
  const [agentTemplates, setAgentTemplates] = useState<AgentTemplate[]>([]);
  const [teamTemplates, setTeamTemplates] = useState<TeamTemplate[]>([]);
  const [activeTab, setActiveTab] = useState<'agents' | 'teams'>('agents');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const [agentTemplatesData, teamTemplatesData] = await Promise.all([
        agentApi.listAgentTemplates(),
        agentApi.listTeamTemplates(),
      ]);
      setAgentTemplates(agentTemplatesData);
      setTeamTemplates(teamTemplatesData);
    } catch (error) {
      console.error('Failed to load templates:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center p-4">Loading templates...</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex">
          <button
            onClick={() => setActiveTab('agents')}
            className={`px-6 py-3 text-sm font-medium ${
              activeTab === 'agents'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Agent Templates
          </button>
          <button
            onClick={() => setActiveTab('teams')}
            className={`px-6 py-3 text-sm font-medium ${
              activeTab === 'teams'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Team Templates
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'agents' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agentTemplates.map((template) => (
              <div
                key={template.template_type}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => onSelectAgentTemplate?.(template)}
              >
                <h3 className="font-semibold text-gray-900 mb-2">{template.name}</h3>
                <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                
                <div className="mb-3">
                  <h4 className="text-xs font-medium text-gray-700 mb-1">Capabilities</h4>
                  <div className="flex flex-wrap gap-1">
                    {template.capabilities.slice(0, 3).map((capability, index) => (
                      <span
                        key={index}
                        className="inline-block bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded"
                      >
                        {capability}
                      </span>
                    ))}
                    {template.capabilities.length > 3 && (
                      <span className="text-xs text-gray-500">
                        +{template.capabilities.length - 3} more
                      </span>
                    )}
                  </div>
                </div>

                <button className="w-full bg-blue-600 text-white text-sm py-2 px-4 rounded hover:bg-blue-700 transition-colors">
                  Create Agent
                </button>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'teams' && (
          <div className="grid grid-cols-1 gap-6">
            {teamTemplates.map((template, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => onSelectTeamTemplate?.(template)}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">{template.name}</h3>
                    <p className="text-sm text-gray-600">{template.description}</p>
                  </div>
                  <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    {template.coordination_pattern}
                  </span>
                </div>

                <div className="mb-4">
                  <p className="text-sm text-gray-700">
                    <strong>Use Case:</strong> {template.use_case}
                  </p>
                  <p className="text-sm text-gray-700 mt-1">
                    <strong>Target:</strong> {template.target_metric}
                  </p>
                </div>

                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Team Composition</h4>
                  <div className="grid grid-cols-2 gap-2">
                    {template.agents.map((agent, agentIndex) => (
                      <div key={agentIndex} className="bg-gray-50 p-3 rounded">
                        <h5 className="text-sm font-medium text-gray-800">{agent.role}</h5>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {agent.capabilities.slice(0, 2).map((capability, capIndex) => (
                            <span
                              key={capIndex}
                              className="inline-block bg-gray-200 text-gray-600 text-xs px-1 py-0.5 rounded"
                            >
                              {capability}
                            </span>
                          ))}
                          {agent.capabilities.length > 2 && (
                            <span className="text-xs text-gray-500">
                              +{agent.capabilities.length - 2}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <button className="w-full bg-green-600 text-white text-sm py-2 px-4 rounded hover:bg-green-700 transition-colors">
                  Create Team
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentTemplateSelector;