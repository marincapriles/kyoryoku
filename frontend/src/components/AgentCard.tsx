import React from 'react';
import { Agent } from '../types/agent';

interface AgentCardProps {
  agent: Agent;
  onEdit?: (agent: Agent) => void;
  onDelete?: (agentId: string) => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
          {agent.template_type && (
            <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mt-1">
              {agent.template_type}
            </span>
          )}
        </div>
        <div className="flex space-x-2">
          {onEdit && (
            <button
              onClick={() => onEdit(agent)}
              className="text-blue-600 hover:text-blue-800 text-sm"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(agent.id)}
              className="text-red-600 hover:text-red-800 text-sm"
            >
              Delete
            </button>
          )}
        </div>
      </div>

      {agent.description && (
        <p className="text-gray-600 text-sm mb-4">{agent.description}</p>
      )}

      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Capabilities</h4>
        <div className="flex flex-wrap gap-1">
          {agent.capabilities.map((capability, index) => (
            <span
              key={index}
              className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
            >
              {capability}
            </span>
          ))}
        </div>
      </div>

      {agent.goals.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Goals</h4>
          <ul className="text-sm text-gray-600 list-disc list-inside">
            {agent.goals.map((goal, index) => (
              <li key={index}>{goal}</li>
            ))}
          </ul>
        </div>
      )}

      {agent.constraints.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Constraints</h4>
          <ul className="text-sm text-gray-600 list-disc list-inside">
            {agent.constraints.map((constraint, index) => (
              <li key={index}>{constraint}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default AgentCard;