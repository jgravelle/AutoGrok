# agent_base_model

import os
import yaml

from base_models.tool_base_model import ToolBaseModel
from typing import List, Dict, Optional, Callable


class AgentBaseModel:
    def __init__(
        self,
        name: str,
        config: Dict,
        tools: Optional[Dict[str, "ToolBaseModel"]] = None,
        role: str = "",
        goal: str = "",
        backstory: str = "",
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        user_id: Optional[str] = None,
        workflows: Optional[str] = None,
        type: Optional[str] = None,
        models: Optional[List[Dict]] = None,
        verbose: Optional[bool] = False,
        allow_delegation: Optional[bool] = True,
        new_description: Optional[str] = None,
        timestamp: Optional[str] = None,
        is_termination_msg: Optional[bool] = None,
        code_execution_config: Optional[Dict] = None,
        llm: Optional[str] = None,
        function_calling_llm: Optional[str] = None,
        max_iter: Optional[int] = 25,
        max_rpm: Optional[int] = None,
        max_execution_time: Optional[int] = None,
        step_callback: Optional[Callable] = None,
        cache: Optional[bool] = True
    ):
        self.id = id
        self.name = name
        self.config = config
        self.description = config.get("description", "")
        self.tools = tools or {}
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id
        self.workflows = workflows
        self.type = type
        self.models = models
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.new_description = new_description
        self.timestamp = timestamp
        self.is_termination_msg = is_termination_msg
        self.code_execution_config = code_execution_config
        self.llm = llm
        self.function_calling_llm = function_calling_llm
        self.max_iter = max_iter
        self.max_rpm = max_rpm
        self.max_execution_time = max_execution_time
        self.step_callback = step_callback
        self.cache = cache

    def add_tool_child(self, tool_name: str, tool: "ToolBaseModel"):
        self.tools[tool_name] = tool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "config": {
                "name": self.name,
                "description": self.description,
                # ... other config values ...
            },
            "tools": {name: tool.to_dict() for name, tool in self.tools.items()},
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_id": self.user_id,
            "workflows": self.workflows,
            "type": self.type,
            "models": self.models,
            "verbose": self.verbose,
            "allow_delegation": self.allow_delegation,
            "new_description": self.new_description,
            "timestamp": self.timestamp,
            "is_termination_msg": self.is_termination_msg,
            "code_execution_config": self.code_execution_config,
            "llm": self.llm,
            "function_calling_llm": self.function_calling_llm,
            "max_iter": self.max_iter,
            "max_rpm": self.max_rpm,
            "max_execution_time": self.max_execution_time,
            "step_callback": self.step_callback,
            "cache": self.cache
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id=data.get("id"),
            name=data["config"]["name"],
            config=data["config"],
            tools={name: ToolBaseModel.from_dict(tool) for name, tool in data.get("tools", {}).items()},
            role=data.get("role", ""),
            goal=data.get("goal", ""),
            backstory=data.get("backstory", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            user_id=data.get("user_id"),
            workflows=data.get("workflows"),
            type=data.get("type"),
            models=data.get("models"),
            verbose=data.get("verbose", False),
            allow_delegation=data.get("allow_delegation", True),
            new_description=data.get("new_description"),
            timestamp=data.get("timestamp"),
            is_termination_msg=data.get("is_termination_msg"),
            code_execution_config=data.get("code_execution_config"),
            llm=data.get("llm"),
            function_calling_llm=data.get("function_calling_llm"),
            max_iter=data.get("max_iter", 25),
            max_rpm=data.get("max_rpm"),
            max_execution_time=data.get("max_execution_time"),
            step_callback=data.get("step_callback"),
            cache=data.get("cache", True)
        )
    
    @classmethod
    def create_agent(cls, agent_name: str, agent_data: Dict) -> "AgentBaseModel":
        agent = cls.from_dict(agent_data)
        
        # Create a YAML file for the agent
        with open(f"agents/yaml/{agent_name}.yaml", "w") as file:
            yaml.dump(agent_data, file)
        
        return agent

    @classmethod
    def get_agent(cls, agent_name: str) -> "AgentBaseModel":
        file_path = f"agents/yaml/{agent_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                agent_data = yaml.safe_load(file)
                return cls.from_dict(agent_data)
        else:
            raise FileNotFoundError(f"Agent file not found: {file_path}")

    @staticmethod
    def load_agents() -> List[str]:
        agent_names = []
        for file in os.listdir("agents/yaml"):
            if file.endswith(".yaml"):
                agent_name = file[:-5]  # Remove the ".yaml" extension
                agent_names.append(agent_name)
        return agent_names
    