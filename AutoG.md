# main.py

```python
# main.py

import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from session_variables import initialize_session_variables
from utils.display_main_util import sidebar_begin, display_main


def main():
    st.set_page_config(page_title="AutoGrok™")

    initialize_session_variables()
    sidebar_begin()
    
    # Main content area
    display_main()


if __name__ == "__main__":
    main()
```

# session_variables.py

```python
# session_variables.py

import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from configs.config_local import LLM_PROVIDER

def initialize_session_variables():

    if "agent_name_input" not in st.session_state:
        st.session_state.agent_name_input = ""

    if "available_models" not in st.session_state:
        st.session_state.available_models = []

    if "current_agent" not in st.session_state:
        st.session_state.current_agent = None

    if "current_framework" not in st.session_state:
        st.session_state.current_framework = None

    if "current_project" not in st.session_state:
        st.session_state.current_project = None

    if "current_tool" not in st.session_state:
        st.session_state.current_tool = None

    if "current_workflow" not in st.session_state:
        st.session_state.current_workflow = None

    if "default_llm" not in st.session_state:
        st.session_state.default_llm = ""

    if "default_provider" not in st.session_state:
        st.session_state.default_provider = LLM_PROVIDER

    if "default_provider_key" not in st.session_state:
        st.session_state.default_provider_key = None

    if "file_content" not in st.session_state:
        st.session_state.file_content = ""

    if "project_dropdown" not in st.session_state:
        st.session_state.project_dropdown = "Select..."

    if "project_model" not in st.session_state:
        st.session_state.project_model = ProjectBaseModel()
        
    if "project_name_input" not in st.session_state:
        st.session_state.project_name_input = ""

    if "provider" not in st.session_state:
        st.session_state.provider = ""

    if "reengineer" not in st.session_state:
        st.session_state.reengineer = True

    if "tool_name_input" not in st.session_state:
        st.session_state.tool_name_input = ""        

    if "workflow_dropdown" not in st.session_state:
        st.session_state.workflow_dropdown = "Select..."

    if "workflow_name_input" not in st.session_state:
        st.session_state.workflow_name_input = ""
```

# base_models\agent_base_model.py

```python
# agent_base_model

import json
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

        # Create a JSON file for the agent
        with open(f"agents/json/{agent_name}.json", "w") as file:
            json.dump(agent_data, file)
        
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
            if file and file.endswith(".yaml"):
                agent_name = file[:-5]  # Remove the ".yaml" extension
                agent_names.append(agent_name)
        if not agent_names:
            for file in os.listdir("agents/json"):
                if file and file.endswith(".json"):
                    agent_name = file[:-5]  # Remove the ".yaml" extension
                    agent_names.append(agent_name)
        return agent_names
    

    def rename_agent(self, old_name, new_name):
        # Rename YAML file
        old_yaml_path = f"agents/yaml/{old_name}.yaml"
        new_yaml_path = f"agents/yaml/{new_name}.yaml"
        if os.path.exists(old_yaml_path):
            os.rename(old_yaml_path, new_yaml_path)

        # Rename JSON file
        old_json_path = f"agents/json/{old_name}.json"
        new_json_path = f"agents/json/{new_name}.json"
        if os.path.exists(old_json_path):
            os.rename(old_json_path, new_json_path)
```

# base_models\project_base_model.py

```python
# project_base_model.py

import enum
import json
import os
import yaml

from base_models.workflow_base_model import WorkflowBaseModel
from datetime import datetime
from typing import List, Dict, Optional

class ProjectBaseModel:
    def __init__(
        self,
        prompt: str = "",
        deliverables: List[Dict] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        notes: Optional[str] = None,
        collaborators: Optional[List[str]] = None,
        tools: Optional[List[Dict]] = None,
        workflows: Optional[Dict[str, "WorkflowBaseModel"]] = None
    ):
        self.id = id or 1
        self.prompt = prompt
        self.deliverables = deliverables or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at
        self.user_id = user_id or "user"
        self.name = name or "project"
        self.description = description
        self.status = status or "not started"
        self.due_date = due_date
        self.priority = priority or "none"
        self.tags = tags or []
        self.attachments = attachments or []
        self.notes = notes
        self.collaborators = collaborators or []
        self.tools = tools or []
        self.workflows = workflows or {}

    def add_deliverable(self, deliverable: str):
        self.deliverables.append({"text": deliverable, "done": False})

    def add_workflow_child(self, workflow_name: str, workflow: "WorkflowBaseModel"):
        self.workflows[workflow_name] = workflow

    @classmethod
    def create_project(cls, project_name: str) -> "ProjectBaseModel":
        project = cls(name=project_name)
        
        # Create a YAML file for the project
        project_data = project.to_dict()
        with open(f"projects/yaml/{project_name}.yaml", "w") as file:
            yaml.dump(project_data, file)

        # Create a JSON file for the project
        with open(f"projects/json/{project_name}.json", "w") as file:
            json.dump(project_data, file)
        
        return project

    @classmethod
    def get_project(cls, project_name: str) -> "ProjectBaseModel":
        file_path = f"projects/yaml/{project_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                project_data = yaml.safe_load(file)
                return cls.from_dict(project_data)
        else:
            raise FileNotFoundError(f"Project file not found: {file_path}")

    @staticmethod
    def load_projects() -> List[str]:
        project_names = []
        for file in os.listdir("projects/yaml"):
            if file.endswith(".yaml"):
                project_name = file[:-5]  # Remove the ".yaml" extension
                project_names.append(project_name)
        if not project_names:
            for file in os.listdir("projects/json"):
                if file.endswith(".json"):
                    project_name = file[:-5]  # Remove the ".json" extension
                    project_names.append(project_name)
        return project_names

    def mark_deliverable_done(self, index: int):
        if 0 <= index < len(self.deliverables):
            self.deliverables[index]["done"] = True

    def mark_deliverable_undone(self, index: int):
        if 0 <= index < len(self.deliverables):
            self.deliverables[index]["done"] = False

    def set_prompt(self, prompt: str):
        self.prompt = prompt

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "deliverables": self.deliverables,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date,
            "priority": self.priority,
            "tags": self.tags,
            "attachments": self.attachments,
            "notes": self.notes,
            "collaborators": self.collaborators,
            "tools": self.tools,
            "workflows": {name: workflow.to_dict() for name, workflow in self.workflows.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict):
        from base_models.workflow_base_model import WorkflowBaseModel  # Avoid circular import
        return cls(
            id=data.get("id"),
            prompt=data.get("prompt", ""),
            deliverables=data.get("deliverables", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            user_id=data.get("user_id"),
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status"),
            due_date=data.get("due_date"),
            priority=data.get("priority"),
            tags=data.get("tags", []),
            attachments=data.get("attachments", []),
            notes=data.get("notes"),
            collaborators=data.get("collaborators", []),
            tools=data.get("tools", []),
            workflows={name: WorkflowBaseModel.from_dict(workflow) for name, workflow in data.get("workflows", {}).items()}
        )

class ProjectPriority(enum.Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ProjectStatus(enum.Enum):
    NOT_STARTED = "not started"
    ON_HOLD = "on hold"
    IN_PROGRESS = "in progress"
    COMPLETE = "complete"
    CANCELED = "canceled"
```

# base_models\tool_base_model.py

```python
# tool_base_model.py

import json
import os
import yaml

from typing import List, Dict, Optional

class ToolBaseModel:
    def __init__(
        self,
        name: str,
        title: str,
        content: str,
        file_name: str,
        description: Optional[str] = None,
        timestamp: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        self.name = name
        self.title = title
        self.content = content
        self.file_name = file_name
        self.description = description
        self.timestamp = timestamp
        self.user_id = user_id

    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "content": self.content,
            "file_name": self.file_name,
            "description": self.description,
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name=data["name"],
            title=data["title"],
            content=data["content"],
            file_name=data["file_name"],
            description=data.get("description"),
            timestamp=data.get("timestamp"),
            user_id=data.get("user_id")
        )
    
    @classmethod
    def create_tool(cls, tool_name: str, tool_data: Dict) -> "ToolBaseModel":
        tool = cls.from_dict(tool_data)
        
        # Create a YAML file for the tool
        with open(f"tools/yaml/{tool_name}.yaml", "w") as file:
            yaml.dump(tool_data, file)

        # Create a JSON file for the tool
        with open(f"tools/json/{tool_name}.json", "w") as file:
            json.dump(tool_data, file)
        
        return tool

    @classmethod
    def get_tool(cls, tool_name: str) -> "ToolBaseModel":
        file_path = f"tools/yaml/{tool_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                tool_data = yaml.safe_load(file)
                return cls.from_dict(tool_data)
        else:
            raise FileNotFoundError(f"Tool file not found: {file_path}")
            
    @staticmethod
    def load_tools() -> List[str]:
        tool_names = []
        for file in os.listdir("tools"):
            if file.endswith(".yaml"):
                tool_name = file[:-5]  # Remove the ".yaml" extension
                tool_names.append(tool_name)
        return tool_names
    
```

# base_models\workflow_base_model.py

```python
# workflow_base_model

import json
import os
import streamlit as st
import yaml

from base_models.agent_base_model import AgentBaseModel
from configs.config import DEBUG
from datetime import datetime
from typing import List, Dict, Optional


class Sender:
    def __init__(
        self,
        type: str,
        config: Dict,
        timestamp: str,
        user_id: str,
        tools: List[Dict],
    ):
        self.type = type
        self.config = config
        self.timestamp = timestamp
        self.user_id = user_id
        self.tools = tools

    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "tools": self.tools,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type=data["type"],
            config=data["config"],
            timestamp=data["timestamp"],
            user_id=data["user_id"],
            tools=data["tools"],
        )
    

class Receiver:
    def __init__(
        self,
        type: str,
        config: Dict,
        groupchat_config: Dict,
        timestamp: str,
        user_id: str,
        tools: List[Dict],
        agents: List[AgentBaseModel],
    ):
        self.type = type
        self.config = config
        self.groupchat_config = groupchat_config
        self.timestamp = timestamp
        self.user_id = user_id
        self.tools = tools
        self.agents = agents

    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "groupchat_config": self.groupchat_config,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "tools": self.tools,
            "agents": [agent.to_dict() for agent in self.agents],
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type=data["type"],
            config=data["config"],
            groupchat_config=data["groupchat_config"],
            timestamp=data["timestamp"],
            user_id=data["user_id"],
            tools=data["tools"],
            agents=[AgentBaseModel.from_dict(agent) for agent in data.get("agents", [])],
        )

class WorkflowBaseModel:
    def __init__(
        self,
        name: str = "",
        description: str = "",
        agent_children: Dict[str, "AgentBaseModel"] = None,
        sender: Sender = None,
        receiver: Receiver = None,
        type: str = "twoagents",
        user_id: str = "user",
        timestamp: str = datetime.now().isoformat(),
        summary_method: str = "last",
        settings: Dict = None,
        groupchat_config: Dict = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id or 1
        self.name = name or "New Workflow"
        self.description = description or "This workflow is used for general purpose tasks."
        self.agent_children = agent_children or {}
        self.sender = sender or Sender(
            type="userproxy",
            config={},
            timestamp=datetime.now().isoformat(),
            user_id="user",
            tools=[],
        )
        self.receiver = receiver or Receiver(
            type="assistant",
            config={},
            groupchat_config={},
            timestamp=datetime.now().isoformat(),
            user_id="default",
            tools=[],
            agents=[],
        )
        self.type = type or "twoagents"
        self.user_id = user_id or "user"
        self.timestamp = timestamp or datetime.now().isoformat()
        self.summary_method = summary_method or "last"
        self.settings = settings or {}
        self.groupchat_config = groupchat_config or {}
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent_children": {name: agent.to_dict() for name, agent in self.agent_children.items()},
            "sender": self.sender.to_dict(),
            "receiver": self.receiver.to_dict(),
            "type": self.type,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "summary_method": self.summary_method,
            "settings": self.settings,
            "groupchat_config": self.groupchat_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        sender = Sender.from_dict(data["sender"])
        receiver = Receiver.from_dict(data["receiver"])
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            agent_children={name: AgentBaseModel.from_dict(agent) for name, agent in data.get("agent_children", {}).items()},
            sender=sender,
            receiver=receiver,
            type=data["type"],
            user_id=data["user_id"],
            timestamp=data["timestamp"],
            summary_method=data["summary_method"],
            settings=data.get("settings", {}),
            groupchat_config=data.get("groupchat_config", {}),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def add_agent_child(self, agent_name: str, agent: "AgentBaseModel"):
        self.agent_children[agent_name] = agent

    @classmethod
    def create_workflow(cls, workflow_name: str) -> "WorkflowBaseModel":
        if DEBUG:
            print(f"Creating workflow {workflow_name}")

        current_timestamp = datetime.now().isoformat()

        workflow = cls(
            name=workflow_name,
            description=st.session_state.current_project.prompt if st.session_state.current_project else "This workflow is used for general purpose tasks.",
            sender=Sender(
                type="userproxy",
                config={
                    "name": "userproxy",
                    "llm_config": {
                        "config_list": [
                            {
                                "user_id": "default",
                                "timestamp": current_timestamp,
                                "model": st.session_state.selected_model,
                                "base_url": None,
                                "api_type": None,
                                "api_version": None,
                                "description": f"{st.session_state.default_provider} model configuration"
                            }
                        ],
                        "temperature": 0.1,
                        "cache_seed": None,
                        "timeout": None,
                        "max_tokens": None,
                        "extra_body": None
                    },
                    "human_input_mode": "NEVER",
                    "max_consecutive_auto_reply": 30,
                    "system_message": "You are a helpful assistant.",
                    "is_termination_msg": None,
                    "code_execution_config": {
                        "work_dir": None,
                        "use_docker": False
                    },
                    "default_auto_reply": "TERMINATE",
                    "description": "A user proxy agent that executes code."
                },
                timestamp=current_timestamp,
                user_id=st.session_state.current_project.user_id if st.session_state.current_project else "user",
                tools=st.session_state.current_project.tools if st.session_state.current_project else [
                    {
                        "title": "fetch_web_content",
                        "content": "...",  # Omitted for brevity
                        "file_name": "fetch_web_content.json",
                        "description": None,
                        "timestamp": current_timestamp,
                        "user_id": "default"
                    }
                ]
            ),
            receiver=Receiver(
                type="assistant",
                config={
                    "name": "primary_assistant",
                    "llm_config": {
                        "config_list": [
                            {
                                "user_id": "default",
                                "timestamp": current_timestamp,
                                "model": st.session_state.selected_model,
                                "base_url": None,
                                "api_type": None,
                                "api_version": None,
                                "description": f"{st.session_state.default_provider} model configuration"
                            }
                        ],
                        "temperature": 0.1,
                        "cache_seed": None,
                        "timeout": None,
                        "max_tokens": None,
                        "extra_body": None
                    },
                    "human_input_mode": "NEVER",
                    "max_consecutive_auto_reply": 30,
                    "system_message": "...",  # Omitted for brevity
                    "is_termination_msg": None,
                    "code_execution_config": None,
                    "default_auto_reply": "",
                    "description": "A primary assistant agent that writes plans and code to solve tasks."
                },
                groupchat_config={},
                timestamp=current_timestamp,
                user_id=st.session_state.current_project.user_id if st.session_state.current_project else "default",
                tools=st.session_state.current_project.tools if st.session_state.current_project else [
                    {
                        "title": "fetch_web_content",
                        "content": "...",  # Omitted for brevity
                        "file_name": "fetch_web_content.json",
                        "description": None,
                        "timestamp": current_timestamp,
                        "user_id": "default"
                    }
                ],
                agents=[]
            ),
            type="twoagents",
            user_id=st.session_state.current_project.user_id if st.session_state.current_project else "user",
            timestamp=current_timestamp,
            summary_method="last"
        )

        # Create a YAML file for the workflow with the default values
        workflow_data = workflow.to_dict()
        with open(f"workflows/yaml/{workflow_name}.yaml", "w") as file:
            yaml.dump(workflow_data, file)

        # Create a JSON file for the workflow
        with open(f"workflows/json/{workflow_name}.json", "w") as file:
            json.dump(workflow_data, file)

        return workflow
    

    @classmethod
    def get_workflow(cls, workflow_name: str) -> "WorkflowBaseModel":
        if DEBUG:
            print(f"Loading workflow: {workflow_name}")
        file_path = f"workflows/yaml/{workflow_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                workflow_data = yaml.safe_load(file)
                return cls.from_dict(workflow_data)
        else:
            raise FileNotFoundError(f"Workflow file not found: {file_path}")
    

    @staticmethod
    def load_workflows() -> List[str]:
        if DEBUG:
            print("Loading workflows")
        project_names = []
        for file in os.listdir("workflows/yaml"):
            if file.endswith(".yaml"):
                project_name = file[:-5]  # Remove the ".yaml" extension
                project_names.append(project_name)
        return project_names
    
    def set_description(self, description: str):
        self.description = description  
```

# configs\config.py

```python
# config.py

import os

# Get user home directory
home_dir = os.path.expanduser("~")
default_db_path = f'{home_dir}/.autogenstudio/database.sqlite'

# Debug
DEFAULT_DEBUG = False

# Default configurations
DEFAULT_LLM_PROVIDER = "groq"
DEFAULT_GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
DEFAULT_OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_OPENAI_API_KEY = None
DEFAULT_OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Try to import user-specific configurations from config_local.py
try:
    from config_local import *
except ImportError:
    pass

# Set the configurations using the user-specific values if available, otherwise use the defaults
DEBUG = locals().get('DEBUG', DEFAULT_DEBUG)

LLM_PROVIDER = locals().get('LLM_PROVIDER', DEFAULT_LLM_PROVIDER)
GROQ_API_URL = locals().get('GROQ_API_URL', DEFAULT_GROQ_API_URL)
LMSTUDIO_API_URL = locals().get('LMSTUDIO_API_URL', DEFAULT_LMSTUDIO_API_URL)
OLLAMA_API_URL = locals().get('OLLAMA_API_URL', DEFAULT_OLLAMA_API_URL)
OPENAI_API_KEY = locals().get('OPENAI_API_KEY', DEFAULT_OPENAI_API_KEY)
OPENAI_API_URL = locals().get('OPENAI_API_URL', DEFAULT_OPENAI_API_URL)

API_KEY_NAMES = {
    "groq": "GROQ_API_KEY",
    "lmstudio": None,
    "ollama": None,
    "openai": "OPENAI_API_KEY",
    # Add other LLM providers and their respective API key names here
}

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # in seconds
RETRY_TOKEN_LIMIT = 5000

# Model configurations
if LLM_PROVIDER == "groq":
    API_URL = GROQ_API_URL
    MODEL_TOKEN_LIMITS = {
        'mixtral-8x7b-32768': 32768,
        'llama3-70b-8192': 8192,
        'llama3-8b-8192': 8192,
        'gemma-7b-it': 8192,
    }
elif LLM_PROVIDER == "lmstudio":
    API_URL = LMSTUDIO_API_URL
    MODEL_TOKEN_LIMITS = {
        'instructlab/granite-7b-lab-GGUF': 2048,
        'MaziyarPanahi/Codestral-22B-v0.1-GGUF': 32768,
    } 
elif LLM_PROVIDER == "openai":
    API_URL = OPENAI_API_URL
    MODEL_TOKEN_LIMITS = {
        'gpt-4o': 4096,
    }
elif LLM_PROVIDER == "ollama":
    API_URL = OLLAMA_API_URL
    MODEL_TOKEN_LIMITS = {
        'llama3': 8192,
    }   
else:
    MODEL_TOKEN_LIMITS = {}

    
# Database path
# FRAMEWORK_DB_PATH="/path/to/custom/database.sqlite"
FRAMEWORK_DB_PATH = os.environ.get('FRAMEWORK_DB_PATH', default_db_path)

MODEL_CHOICES = {
    'default': None,
    'gemma-7b-it': 8192,
    'gpt-4o': 4096,
    'instructlab/granite-7b-lab-GGUF': 2048,
    'MaziyarPanahi/Codestral-22B-v0.1-GGUF': 32768,
    'llama3': 8192,
    'llama3-70b-8192': 8192,
    'llama3-8b-8192': 8192,
    'mixtral-8x7b-32768': 32768
}
```

# configs\config_local.py

```python
# config_local.py

# User-specific configurations

LLM_PROVIDER = "Groq_Provider"
DEFAULT_MODEL = "llama3-8b-8192"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
# OPENAI_API_KEY = "your_openai_api_key"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

DEBUG = True
```

# event_handlers\event_handlers_agent.py

```python
# event_handlers_agent.py

import json
import importlib
import os
import re
import streamlit as st
import yaml

from datetime import datetime
from base_models.agent_base_model import AgentBaseModel
from configs.config_local import DEBUG


def handle_agent_close():
    if DEBUG:
        print("handle_agent_close()")
    st.session_state.current_agent = None
    st.session_state.agent_dropdown = "Select..."
    # st.rerun()


def handle_ai_agent_creation():
    if DEBUG:
        print("handle_ai_agent_creation()")
    agent_creation_input = st.session_state.agent_creation_input.strip()
    if agent_creation_input:
        # Load the generate_agent_prompt from the file
        with open("prompts/generate_agent_prompt.yaml", "r") as file:
            prompt_data = yaml.safe_load(file)
            if prompt_data is not None and "generate_agent_prompt" in prompt_data:
                generate_agent_prompt = prompt_data["generate_agent_prompt"]
            else:
                st.error("Failed to load the agent prompt.")
                return

        # Combine the generate_agent_prompt with the user input
        prompt = f"{generate_agent_prompt}\n\nRephrased agent request: {agent_creation_input}"

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": prompt}]})
            agent_code = provider.process_response(response)["choices"][0]["message"]["content"]

            # Extract the agent name from the generated code
            agent_name_match = re.search(r"# Agent filename: (\w+)\.py", agent_code)
            if agent_name_match:
                agent_name = agent_name_match.group(1)
            else:
                class_name_match = re.search(r"class (\w+):", agent_code)
                if class_name_match:
                    agent_name = class_name_match.group(1)
                else:
                    st.error("Failed to extract the agent name or class name from the generated code.")
                    return

            agent_data = {
                "name": agent_name,
                "config": {"name": agent_name},
                "skills": [],
                "code": agent_code
            }
            agent = AgentBaseModel.create_agent(agent_name, agent_data)
            st.session_state.current_agent = agent
            st.session_state.agent_dropdown = agent_name
            st.success(f"Agent '{agent_name}' created successfully!")
        except Exception as e:
            st.error(f"Error generating the agent: {str(e)}")


import os
import yaml
import json
from datetime import datetime


def handle_agent_property_change():
    if DEBUG:
        print("handle_agent_property_change()")
    agent = st.session_state.current_agent
    if agent:
        agent.description = st.session_state[f"agent_description_{agent.name}"]
        agent.role = st.session_state[f"agent_role_{agent.name}"]
        agent.goal = st.session_state[f"agent_goal_{agent.name}"]
        agent.backstory = st.session_state[f"agent_backstory_{agent.name}"]
        update_agent()


def handle_agent_selection():
    if DEBUG:
        print("handle_agent_selection()")
    selected_agent = st.session_state.agent_dropdown
    if selected_agent == "Select...":
        return
    if selected_agent == "Create manually...":
        # Handle manual agent creation
        agent_name = st.session_state.agent_name_input.strip()
        if agent_name:
            agent_data = {
                "name": agent_name,
                "description": "",
                "role": "",
                "goal": "",
                "backstory": "",
                "tools": [],
                "config": {},
                "timestamp": datetime.now().isoformat(),
                "user_id": "default"
            }
            agent = AgentBaseModel.from_dict(agent_data)
            AgentBaseModel.create_agent(agent_name, agent)
            st.session_state.current_agent = agent
            st.session_state.agent_dropdown = agent_name    
    elif selected_agent == "Create with AI...":
        # Clear the current agent selection
        st.session_state.current_agent = None
    else:
        # Load the selected agent
        agent = AgentBaseModel.get_agent(selected_agent)
        st.session_state.current_agent = agent


def handle_agent_name_change():
    if DEBUG:
        print("handle_agent_name_change()")
    new_agent_name = st.session_state.agent_name_edit.strip()
    if new_agent_name:
        old_agent_name = st.session_state.current_agent.name
        st.session_state.current_agent.name = new_agent_name
        
        # Rename the YAML agent file
        old_file_path = f"agents/yaml/{old_agent_name}.yaml"
        new_file_path = f"agents/yaml/{new_agent_name}.yaml"
        os.rename(old_file_path, new_file_path)

        # Rename the JSON agent file
        old_file_path = f"agents/json/{old_agent_name}.json"
        new_file_path = f"agents/json/{new_agent_name}.json"
        os.rename(old_file_path, new_file_path)
        update_agent()


def update_agent():
    if DEBUG:
        print("update_agent()")
    st.session_state.current_agent.updated_at = datetime.now().isoformat()
    agent_name = st.session_state.current_agent.name
    agent_data = st.session_state.current_agent.to_dict()
    with open(f"agents/yaml/{agent_name}.yaml", "w") as file:
        yaml.dump(agent_data, file)
    with open(f"agents/json/{agent_name}.json", "w") as file:
        json.dump(agent_data, file)
```

# event_handlers\event_handlers_files.py

```python
# event_handlers_files.py

from configs.config_local import DEBUG



```

# event_handlers\event_handlers_project.py

```python
# event_handlers_project.py

import os
import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from base_models.workflow_base_model import WorkflowBaseModel
from configs.config_local import DEBUG
from event_handlers.event_handlers_prompt import handle_prompt
from event_handlers.event_handlers_shared import update_project
from event_handlers.event_handlers_workflow import handle_workflow_close, update_workflow

# def handle_project_attachments_change():
#     new_project_attachments = st.session_state.current_project.attachments.strip()
#     if new_project_attachments:
#         attachments = [attachment.strip() for attachment in new_project_attachments.split(",")]
#         st.session_state.current_project.attachments = attachments
#         update()


def handle_project_collaborators_change():
    if DEBUG:
        print("called handle_project_collaborators_change()")
    new_project_collaborators = st.session_state.project_collaborators.strip()
    if new_project_collaborators:
        collaborators = [collaborator.strip() for collaborator in new_project_collaborators.split(",")]
        st.session_state.current_project.collaborators = collaborators
        update_project()


def handle_project_close():
    if DEBUG:
        print("handle_project_close()")
    st.session_state.current_project = None
    st.session_state.project_dropdown = "Select..."
    
    # Close the current workflow
    handle_workflow_close()
    
    # st.rerun()


def handle_project_delete():
    if DEBUG:
        print("handle_project_delete()")


def handle_project_description_change():
    if DEBUG:
        print("handle_project_description_change")
    new_project_description = st.session_state.project_description.strip()
    if new_project_description:
        st.session_state.current_project.description = new_project_description
        update_project()


def handle_project_due_date_change():
    if DEBUG:
        print("called handle_project_due_date_change()")
    new_project_due_date = st.session_state.project_due_date
    if new_project_due_date:
        st.session_state.current_project.due_date = new_project_due_date.strftime("%Y-%m-%d")
        update_project()


def handle_project_name_change():
    if DEBUG:
        print("called handle_project_name_change()")
    new_project_name = st.session_state.project_name_edit.strip()
    if new_project_name:
        old_project_name = st.session_state.current_project.name
        st.session_state.current_project.name = new_project_name
        
        # Rename the YAML project file
        old_file_path = f"projects/yaml/{old_project_name}.yaml"
        new_file_path = f"projects/yaml/{new_project_name}.yaml"
        os.rename(old_file_path, new_file_path)

        # Rename the JSON project file
        old_file_path = f"projects/json/{old_project_name}.json"
        new_file_path = f"projects/json/{new_project_name}.json"
        os.rename(old_file_path, new_file_path)
        
        update_project()


def handle_project_notes_change():
    if DEBUG:
        print("called handle_project_notes_change()")
    new_project_notes = st.session_state.project_notes.strip()
    if new_project_notes:
        st.session_state.current_project.notes = new_project_notes
        update_project()


def handle_project_prompt_reengineer():
    if DEBUG:
        print("handle_project_prompt_reengineer()")
    user_request = st.session_state.project_prompt_input.strip()
    result_text = handle_prompt(user_request, "prompts/rephrase_prompt.yaml", "rephrase_prompt")
    if result_text:
        st.session_state.project_prompt_output = result_text
        # Create new Project named "New Project" with the rephrased request as the 'prompt' property value
        st.session_state.current_project = ProjectBaseModel(name="New Project", prompt=result_text)
        st.session_state.current_project.create_project("New Project")
        st.session_state.current_project.set_prompt(result_text)
        st.session_state.current_workflow = WorkflowBaseModel(name="New Workflow")
        st.session_state.current_workflow.create_workflow("New Workflow")
        st.session_state.current_workflow.set_description(user_request + "\n\r" + result_text)

        update_project()
        update_workflow()


def handle_project_selection():
    if DEBUG:
        print("called handle_project_selection()")
    selected_project = st.session_state.project_dropdown
    if selected_project == "Select...":
        return
    if selected_project == "Create from AI...":
        return
    if selected_project == "Create manually...":
        project_name = st.session_state.project_name_input.strip()
        if project_name:
            project = ProjectBaseModel(name=project_name)
            st.session_state.current_project = project
            st.session_state.project_dropdown = project_name
            ProjectBaseModel.create_project(st.session_state.current_project.name)
            
            # Close the current workflow
            handle_workflow_close()
    else:
        # Load the selected project
        project = ProjectBaseModel.get_project(selected_project)
        st.session_state.current_project = project

        # Load the workflows for the selected project
        st.session_state.current_project.workflows = project.workflows


def handle_project_status_change():
    if DEBUG:
        print("called handle_project_status_change()")
    new_project_status = st.session_state.project_status
    if new_project_status:
        st.session_state.current_project.status = new_project_status
        update_project()


def handle_project_user_id_change():
    if DEBUG:
        print("called handle_project_user_id_change()")
    new_project_user_id = st.session_state.project_user_id.strip()
    if new_project_user_id:
        st.session_state.current_project.user_id = new_project_user_id
        update_project()

```

# event_handlers\event_handlers_prompt.py

```python
# event_handlers_prompt.py

import importlib
import streamlit as st
import yaml

from configs.config_local import DEBUG
from event_handlers.event_handlers_shared import update_project

def handle_prompt_change():
    if DEBUG:
        print("called handle_prompt_change()")
    new_prompt = st.session_state.prompt.strip()
    if new_prompt:
        st.session_state.current_project.prompt = new_prompt
        update_project()

def handle_prompt(user_request, prompt_file_path, prompt_label):
    if DEBUG:
        print(f"handle_prompt()\n\r - User request: {user_request}\n\r Prompt file path: {prompt_file_path}\n\r Prompt label: {prompt_label}")
    if user_request:
        # Load the prompt from the file
        with open(prompt_file_path, "r") as file:
            prompt_data = yaml.safe_load(file)
            prompt = prompt_data[prompt_label]

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            # Replace '{user_request}' in the prompt with the actual user's request
            formatted_prompt = prompt.replace("{user_request}", user_request)
            if DEBUG:
                print(f"Formatted prompt: {formatted_prompt}")
            # Send the formatted prompt to the provider
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": formatted_prompt}]})
            result_text = provider.process_response(response)["choices"][0]["message"]["content"]
            return result_text
        except Exception as e:
            st.error(f"Error processing the request: {str(e)}")
    return None


```

# event_handlers\event_handlers_settings.py

```python
# event_handlers\event_handlers_settings.py

import importlib
import os
import streamlit as st

from configs.config import DEBUG
from providers.base_provider import BaseLLMProvider


def handle_default_provider_change():
    if DEBUG:
        print("handle_default_provider_change()")
    selected_provider = st.session_state.default_provider
    st.session_state.default_provider = selected_provider


def load_model_classes():
    if DEBUG:
        print("load_model_classes()")
    model_classes = []
    models_folder = "models"

    for file_name in os.listdir(models_folder):
        if file_name.endswith(".py") and file_name != "llm_base_model.py":
            module_name = file_name[:-3]  # Remove the ".py" extension
            module = importlib.import_module(f"{models_folder}.{module_name}")

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseLLMProvider) and attr != BaseLLMProvider:
                    model_classes.append(attr_name)

    return model_classes


def load_provider_classes():
    if DEBUG:
        print("load_provider_classes()")
    provider_classes = []
    providers_folder = "providers"
    
    for file_name in os.listdir(providers_folder):
        if file_name.endswith(".py") and file_name != "base_provider.py":
            module_name = file_name[:-3]  # Remove the ".py" extension
            module = importlib.import_module(f"{providers_folder}.{module_name}")
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseLLMProvider) and attr != BaseLLMProvider:
                    provider_classes.append(attr_name)
    
    return provider_classes
```

# event_handlers\event_handlers_shared.py

```python
# event_handlers_shared.py

import json
import streamlit as st
import yaml

from base_models.project_base_model import ProjectBaseModel, WorkflowBaseModel
from configs.config_local import DEBUG
from datetime import datetime



def update_project():
    if DEBUG:
        print("called update_project()")

    # Update the project
    st.session_state.current_project.updated_at = datetime.now().isoformat()
    project_name = st.session_state.current_project.name
    project_data = st.session_state.current_project.to_dict()
    with open(f"projects/yaml/{project_name}.yaml", "w") as file:
        yaml.dump(project_data, file)
    with open(f"projects/json/{project_name}.json", "w") as file:
        json.dump(project_data, file)
```

# event_handlers\event_handlers_tool.py

```python
# event_handlers_tool.py

import importlib
import json
import os
import re
import streamlit as st
import yaml

from datetime import datetime
from base_models.tool_base_model import ToolBaseModel
from configs.config_local import DEBUG


def handle_ai_tool_creation():
    if DEBUG:
        print("handle_ai_tool_creation()")
    tool_creation_input = st.session_state.tool_creation_input.strip()
    if tool_creation_input:
        # Load the generate_tool_prompt from the file
        with open("prompts/generate_tool_prompt.yaml", "r") as file:
            prompt_data = yaml.safe_load(file)
            generate_tool_prompt = prompt_data["generate_tool_prompt"]

        # Combine the generate_tool_prompt with the user input
        prompt = f"{generate_tool_prompt}\n\nRephrased tool request: {tool_creation_input}"

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": prompt}]})
            tool_code = provider.process_response(response)["choices"][0]["message"]["content"]

            # Extract the tool name from the generated code
            tool_name_match = re.search(r"# Tool filename: ([\w_]+)\.py", tool_code)
            if tool_name_match:
                tool_name = tool_name_match.group(1)
                tool_data = {
                    "name": tool_name,
                    "title": tool_name,
                    "content": tool_code,
                    "file_name": f"{tool_name}.json",
                    "description": None,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": "default"
                }
                tool = ToolBaseModel.create_tool(tool_name, tool_data)
                st.session_state.current_tool = tool
                st.session_state.tool_dropdown = tool_name
                st.success(f"Tool '{tool_name}' created successfully!")
            else:
                st.error("Failed to extract the tool name from the generated code.")
        except Exception as e:
            st.error(f"Error generating the tool: {str(e)}")


def handle_tool_close():
    if DEBUG:
        print("handle_tool_close()")
    st.session_state.current_tool = None
    st.session_state.tool_dropdown = "Select..."
    # st.rerun()


def handle_tool_property_change():
    if DEBUG:
        print("handle_tool_property_change()")
    tool = st.session_state.current_tool
    if tool:
        tool.name = st.session_state[f"tool_name_{tool.name}"]
        tool.title = st.session_state[f"tool_title_{tool.name}"]
        tool.description = st.session_state[f"tool_description_{tool.name}"]
        tool.file_name = st.session_state[f"tool_file_name_{tool.name}"]
        tool.content = st.session_state[f"tool_content_{tool.name}"]
        tool.user_id = st.session_state[f"tool_user_id_{tool.name}"]

        tool_data = tool.to_dict()
        tool_name = tool.name
        with open(f"tools/yaml/{tool_name}.yaml", "w") as file:
            yaml.dump(tool_data, file)
        with open(f"tools/json/{tool_name}.json", "w") as file:
            json.dump(tool_data, file)


def handle_tool_selection():
    if DEBUG:
        print("handle_tool_selection()")
    selected_tool = st.session_state.tool_dropdown
    if selected_tool     == "Select...":
        return
    if selected_tool == "Create manually...":
        # Handle manual tool creation
        tool_name = st.session_state.tool_name_input.strip()
        if tool_name:
            tool_data = {
                "name": tool_name,
                "title": tool_name,
                "content": "",
                "file_name": f"{tool_name}.json",
                "description": None,
                "timestamp": datetime.now().isoformat(),
                "user_id": "default"
            }
            tool = ToolBaseModel.create_tool(tool_name, tool_data)
            st.session_state.current_tool = tool
            st.session_state.tool_dropdown = tool_name
    elif selected_tool == "Create with AI...":
        # Clear the current tool selection
        st.session_state.current_tool = None
    else:
        # Load the selected tool
        tool = ToolBaseModel.get_tool(selected_tool)
        st.session_state.current_tool = tool


def handle_tool_name_change():
    if DEBUG:
        print("handle_tool_name_change()")
    new_tool_name = st.session_state.tool_name_edit.strip()
    if new_tool_name:
        old_tool_name = st.session_state.current_tool.name
        st.session_state.current_tool.name = new_tool_name
        
        # Rename the YAML project file
        old_file_path = f"projects/yaml/{old_tool_name}.yaml"
        new_file_path = f"projects/yaml/{new_tool_name}.yaml"
        os.rename(old_file_path, new_file_path)

        # Rename the JSON project file
        old_file_path = f"projects/json/{old_tool_name}.json"
        new_file_path = f"projects/json/{new_tool_name}.json"
        os.rename(old_file_path, new_file_path)
        update_tool()


def update_tool():
    if DEBUG:
        print("update_tool()")
    st.session_state.current_tool.updated_at = datetime.now().isoformat()
    tool_name = st.session_state.current_tool.name
    tool_data = st.session_state.current_tool.to_dict()
    with open(f"tools/yaml/{tool_name}.yaml", "w") as file:
        yaml.dump(tool_data, file)
```

# event_handlers\event_handlers_workflow.py

```python
# event_handlers_workflow.py

import json
import os
import streamlit as st
import yaml

from datetime import datetime
from base_models.workflow_base_model import WorkflowBaseModel, Sender, Receiver
from configs.config_local import DEBUG
from event_handlers.event_handlers_shared import update_project


def handle_workflow_close():
    if DEBUG:
        print("called handle_workflow_close()")
    st.session_state.current_workflow = None
    st.session_state.workflow_dropdown = "Select..."
    # st.rerun()


def handle_workflow_delete(workflow_file):
    if DEBUG:
        print(f"called handle_workflow_delete({workflow_file})")
    os.remove(workflow_file)
    st.session_state.current_workflow = None
    st.session_state.workflow_dropdown = "Select..."
    st.success(f"Workflow '{workflow_file}' has been deleted.")


def handle_workflow_description_change():
    if DEBUG:
        print("called handle_workflow_description_change()")
    new_workflow_description = st.session_state.workflow_description.strip()
    if new_workflow_description:
        st.session_state.current_workflow.description = new_workflow_description
        update_workflow()


def handle_workflow_name_change():
    if DEBUG:
        print("called handle_workflow_name_change()")
    new_workflow_name = st.session_state.workflow_name_edit.strip()
    if new_workflow_name:
        old_workflow_name = st.session_state.current_workflow.name
        st.session_state.current_workflow.name = new_workflow_name
        
        # Rename the YAML project file
        old_file_path = f"workflows/yaml/{old_workflow_name}.yaml"
        new_file_path = f"workflows/yaml/{new_workflow_name}.yaml"
        os.rename(old_file_path, new_file_path)

        # Rename the JSON project file
        old_file_path = f"workflows/json/{old_workflow_name}.json"
        new_file_path = f"workflows/json/{new_workflow_name}.json"
        os.rename(old_file_path, new_file_path)
        
        # Update the workflow name in current_project.workflows
        if st.session_state.current_project and old_workflow_name in st.session_state.current_project.workflows:
            st.session_state.current_project.workflows[new_workflow_name] = st.session_state.current_project.workflows.pop(old_workflow_name)
            update_project()
        update_workflow()


def handle_workflow_selection():
    if DEBUG:
        print("called handle_workflow_selection()")
    selected_workflow = st.session_state.workflow_dropdown
    if selected_workflow == "Select...":
        return
    if selected_workflow == "Create...":
        workflow_name = st.session_state.workflow_name_input.strip()
        if workflow_name:
            workflow = WorkflowBaseModel(   
                name=workflow_name,
                description="This workflow is used for general purpose tasks.",
                sender=Sender(
                    type="userproxy",
                    config={
                        "name": "userproxy",
                        "llm_config": {
                            "config_list": [
                                {
                                    "user_id": "default",
                                    "timestamp": "2024-03-28T06:34:40.214593",
                                    "model": "gpt-4o",
                                    "base_url": None,
                                    "api_type": None,
                                    "api_version": None,
                                    "description": "OpenAI model configuration"
                                }
                            ],
                            "temperature": 0.1,
                            "cache_seed": None,
                            "timeout": None,
                            "max_tokens": None,
                            "extra_body": None
                        },
                        "human_input_mode": "NEVER",
                        "max_consecutive_auto_reply": 30,
                        "system_message": "You are a helpful assistant.",
                        "is_termination_msg": None,
                        "code_execution_config": {
                            "work_dir": None,
                            "use_docker": False
                        },
                        "default_auto_reply": "TERMINATE",
                        "description": "A user proxy agent that executes code."
                    },
                    timestamp="2024-03-28T06:34:40.214593",
                    user_id="user",
                    tools=[
                        {
                            "title": "fetch_web_content",
                            "content": "...",  # Omitted for brevity
                            "file_name": "fetch_web_content.json",
                            "description": None,
                            "timestamp": "2024-05-14T08:19:12.425322",
                            "user_id": "default"
                        }
                    ]
                ),
                receiver=Receiver(
                    type="assistant",
                    config={
                        "name": "primary_assistant",
                        "llm_config": {
                            "config_list": [
                                {
                                    "user_id": "default",
                                    "timestamp": "2024-05-14T08:19:12.425322",
                                    "model": "gpt-4o",
                                    "base_url": None,
                                    "api_type": None,
                                    "api_version": None,
                                    "description": "OpenAI model configuration"
                                }
                            ],
                            "temperature": 0.1,
                            "cache_seed": None,
                            "timeout": None,
                            "max_tokens": None,
                            "extra_body": None
                        },
                        "human_input_mode": "NEVER",
                        "max_consecutive_auto_reply": 30,
                        "system_message": "...",  # Omitted for brevity
                        "is_termination_msg": None,
                        "code_execution_config": None,
                        "default_auto_reply": "",
                        "description": "A primary assistant agent that writes plans and code to solve tasks."
                    },
                    groupchat_config={},
                    timestamp=datetime.now().isoformat(),
                    user_id="default",
                    tools=[
                        {
                            "title": "fetch_web_content",
                            "content": "...",  # Omitted for brevity
                            "file_name": "fetch_web_content.json",
                            "description": None,
                            "timestamp": "2024-05-14T08:19:12.425322",
                            "user_id": "default"
                        }
                    ],
                    agents=[]
                ),
                type="twoagents",
                user_id="user",
                timestamp=datetime.now().isoformat(),
                summary_method="last"
            )
            st.session_state.current_workflow = workflow
            st.session_state.workflow_dropdown = workflow_name
            WorkflowBaseModel.create_workflow(st.session_state.current_workflow.name)

            # Add the created workflow's name to current_project.workflows
            if st.session_state.current_project:
                st.session_state.current_project.workflows[workflow_name] = workflow
                update_project()
    else:
        print ("Selected workflow: ", selected_workflow)
        workflow = WorkflowBaseModel.get_workflow(selected_workflow)
        st.session_state.current_workflow = workflow

        # Update current_project.workflows to reflect the selected workflow
        if st.session_state.current_project:
            st.session_state.current_project.workflows[selected_workflow] = workflow
            update_project()



def handle_workflow_type_change():
    if DEBUG:
        print("called handle_workflow_type_change()")
    new_workflow_type = st.session_state.workflow_type.strip()
    if new_workflow_type:
        st.session_state.current_workflow.type = new_workflow_type
        update_workflow()


def handle_workflow_summary_method_change():
    if DEBUG:
        print("called handle_workflow_summary_method_change()")
    new_workflow_summary_method = st.session_state.workflow_summary_method.strip()
    if new_workflow_summary_method:
        st.session_state.current_workflow.summary_method = new_workflow_summary_method
        update_workflow()


def update_workflow():
    if DEBUG:
        print("called update_workflow()")
    st.session_state.current_workflow.updated_at = datetime.now().isoformat()
    workflow_name = st.session_state.current_workflow.name
    workflow_data = st.session_state.current_workflow.to_dict()
    with open(f"workflows/yaml/{workflow_name}.yaml", "w") as file:
        yaml.dump(workflow_data, file)
    with open(f"workflows/yaml/{workflow_name}.json", "w") as file:
        json.dump(workflow_data, file)
```

# providers\base_provider.py

```python

from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def send_request(self, data):
        pass

    @abstractmethod
    def process_response(self, response):
        pass
    
```

# providers\fireworks_provider.py

```python

import json
import requests

from providers.base_provider import BaseLLMProvider
from utils.auth_utils import get_api_key


class FireworksProvider(BaseLLMProvider):
    def __init__(self, api_url):
        self.api_key = get_api_key()
        self.api_url = api_url


    def process_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


    def send_request(self, data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        # Ensure data is a JSON string
        if isinstance(data, dict):
            json_data = json.dumps(data)
        else:
            json_data = data
        response = requests.post(self.api_url, data=json_data, headers=headers)
        return response
    
```

# providers\groq_provider.py

```python
# groq_provider.py

import json
import os
import requests
import streamlit as st

from configs.config_local import DEBUG
from providers.base_provider import BaseLLMProvider

class Groq_Provider(BaseLLMProvider):
    def __init__(self, api_url, api_key):
        self.api_key = api_key
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = "https://api.groq.com/openai/v1/chat/completions"


    def get_available_models(self):
        if DEBUG:
            print ("GROQ: get_available_models")
            #print (f"KEY: {self.api_key}")
        response = requests.get("https://api.groq.com/openai/v1/models", headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        if response.status_code == 200:
            models = response.json().get("data", [])
            return [model["id"] for model in models]
        else:
            raise Exception(f"Failed to retrieve models: {response.status_code}")


    def process_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


    def send_request(self, data):
        # Check for API key in environment variable
        api_key = os.environ.get("GROQ_API_KEY")
        
        # If not found in environment variable, check session state
        if not api_key:
            api_key = st.session_state.get("default_provider_key")
        
        # If not found in session state, check global variable
        if not api_key:
            api_key = globals().get("GROQ_API_KEY")
        
        # If no API key is found, raise an exception
        if not api_key:
            raise Exception("No Groq API key found. Please provide an API key.")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        # Ensure data is a JSON string
        if isinstance(data, dict):
            json_data = json.dumps(data)
        else:
            json_data = data
        response = requests.post(self.api_url, data=json_data, headers=headers)
        return response
    
```

# providers\lmstudio_provider.py

```python
# lmstudio_provider.py

import json
import requests
import streamlit as st

from providers.base_provider import BaseLLMProvider

class LmstudioProvider(BaseLLMProvider):
    def __init__(self, api_url, api_key=None):
        self.api_url = "http://localhost:1234/v1/chat/completions"

    def process_response(self, response):
        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data:
                content = response_data["choices"][0]["message"]["content"]
                return {
                    "choices": [
                        {
                            "message": {
                                "content": content.strip()
                            }
                        }
                    ]
                }
            else:
                raise Exception("Unexpected response format. 'choices' field missing.")
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


    def send_request(self, data):
        headers = {
            "Content-Type": "application/json",
        }

        # Construct the request data in the format expected by the LM Studio API
        lm_studio_request_data = {
            "model": data["model"],
            "messages": data["messages"],
            "temperature": st.session_state.temperature,
            "max_tokens": data.get("max_tokens", 2048),
            "stop": data.get("stop", "TERMINATE"),
        }

        # Ensure data is a JSON string
        if isinstance(lm_studio_request_data, dict):
            json_data = json.dumps(lm_studio_request_data)
        else:
            json_data = lm_studio_request_data

        response = requests.post(self.api_url, data=json_data, headers=headers)
        return response
    
```

# providers\ollama_provider.py

```python
import json
import requests
import streamlit as st

from providers.base_provider import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    def __init__(self, api_url, api_key=None):
        self.api_url = "http://127.0.0.1:11434/api/generate"


    def process_response(self, response):
        if response.status_code == 200:
            response_data = response.json()
            if "response" in response_data:
                content = response_data["response"].strip()
                if content:
                    return {
                        "choices": [
                            {
                                "message": {
                                    "content": content
                                }
                            }
                        ]
                    }
                else:
                    raise Exception("Empty response received from the Ollama API.")
            else:
                raise Exception("Unexpected response format. 'response' field missing.")
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


    def send_request(self, data):
        headers = {
            "Content-Type": "application/json",
        }
        # Construct the request data in the format expected by the Ollama API
        ollama_request_data = {
            "model": data["model"],
            "prompt": data["messages"][0]["content"],
            "temperature": st.session_state.temperature,
            "max_tokens": data.get("max_tokens", 2048),
            "stop": data.get("stop", "TERMINATE"),
            "stream": False,
        }
        # Ensure data is a JSON string
        if isinstance(ollama_request_data, dict):
            json_data = json.dumps(ollama_request_data)
        else:
            json_data = ollama_request_data
        response = requests.post(self.api_url, data=json_data, headers=headers)
        return response
```

# providers\openai_provider.py

```python
# openai_provider.py

import json
import os
import requests
import streamlit as st

from configs.config_local import DEBUG
from providers.base_provider import BaseLLMProvider

class Openai_Provider(BaseLLMProvider):
    def __init__(self, api_url, api_key):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"


    def get_available_models(self):
        if DEBUG:
            print ("GROQ: get_available_models")
            #print (f"KEY: {self.api_key}")
        response = requests.get("https://api.openai.com/v1/models", headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        if response.status_code == 200:
            models = response.json().get("data", [])
            return [model["id"] for model in models]
        else:
            raise Exception(f"Failed to retrieve models: {response.status_code}")
        

    def process_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


    def send_request(self, data):
        print("self.api_url: ", self.api_url)
        
        # Check for API key in environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        
        # If not found in environment variable, check session state
        if not api_key:
            api_key = st.session_state.get("default_provider_key")
        
        # If not found in session state, check global variable
        if not api_key:
            api_key = globals().get("OPENAI_API_KEY")
        
        # If no API key is found, raise an exception
        if not api_key:
            raise Exception("No OpenAI API key found. Please provide an API key.")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        # Ensure data is a JSON string
        if isinstance(data, dict):
            json_data = json.dumps(data)
        else:
            json_data = data
        
        response = requests.post(self.api_url, data=json_data, headers=headers)
        print("response.status_code: ", response.status_code)
        print("response.text: ", response.text)
        return response
    
```

# utils\auth_utils.py

```python

import os
import streamlit as st

from configs.config_local import LLM_PROVIDER


def get_api_key():
    api_key_env_var = f"{LLM_PROVIDER.upper()}_API_KEY"
    api_key = os.environ.get(api_key_env_var)
    if api_key is None:
        api_key = st.session_state.get(api_key_env_var)
    return api_key


def get_api_url():
    api_url_env_var = f"{LLM_PROVIDER.upper()}_API_URL"
    api_url = os.environ.get(api_url_env_var)
    if api_url is None:
        api_url = globals().get(api_url_env_var)
        if api_url is None:
            if api_url_env_var not in st.session_state:
                api_url = st.text_input(f"Enter the {LLM_PROVIDER.upper()} API URL:", type="password", key=f"{LLM_PROVIDER}_api_url_input")
                if api_url:
                    st.session_state[api_url_env_var] = api_url
                    st.success("API URL entered successfully.")
                else:
                    st.warning(f"Please enter the {LLM_PROVIDER.upper()} API URL to use the app.")
            else:
                api_url = st.session_state.get(api_url_env_var)
    return api_url

```

# utils\display_agent_util.py

```python
# display_main_util.py

import streamlit as st

from base_models.agent_base_model import AgentBaseModel
from configs.config_local import DEBUG
from event_handlers.event_handlers_agent import (
    handle_agent_close, handle_agent_selection, handle_ai_agent_creation, 
    handle_agent_name_change, handle_agent_property_change
)

def display_agent_dropdown():
    if DEBUG:
        print("display_agent_dropdown()")
    if st.session_state.current_agent is None:
        # Display the agents dropdown
        agent_names = AgentBaseModel.load_agents()
        selected_agent = st.selectbox(
            "Agents",
            ["Select..."] + ["Create with AI..."] + ["Create manually..."] + agent_names,
            key="agent_dropdown",
            on_change=handle_agent_selection,
        )

        if selected_agent == "Select...":
            return
        if selected_agent == "Create manually...":
            # Show the manual agent creation input field
            st.text_input("Agent Name:", key="agent_name_input", on_change=handle_agent_selection)
        elif selected_agent == "Create with AI...":
            # Show the AI-assisted agent creation input field
            st.text_input("What should this new agent do?", key="agent_creation_input", on_change=handle_ai_agent_creation)
    else:
        st.session_state.current_agent.name = st.text_input(
            "Agent Name:",
            value=st.session_state.current_agent.name,
            key="agent_name_edit",
            on_change=handle_agent_name_change,
        )
        if st.button("CLOSE THIS AGENT"):
            handle_agent_close()


def display_agent_properties():
    if DEBUG:
        print("display_agent_properties()")
    agent = st.session_state.current_agent
    st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>AGENT PROPERTIES</div>", unsafe_allow_html=True)
    st.write(f"<div style='text-align:right; width:100%;'>Timestamp: {agent.timestamp}</div>", unsafe_allow_html=True)

    agent.description = st.text_area("Description:", value=agent.description or "", key=f"agent_description_{agent.name}", on_change=handle_agent_property_change)
    agent.role = st.text_input("Role:", value=agent.role or "", key=f"agent_role_{agent.name}", on_change=handle_agent_property_change)
    agent.goal = st.text_input("Goal:", value=agent.goal or "", key=f"agent_goal_{agent.name}", on_change=handle_agent_property_change)
    agent.backstory = st.text_area("Backstory:", value=agent.backstory or "", key=f"agent_backstory_{agent.name}", on_change=handle_agent_property_change)
    

def display_sidebar_agents():
    if DEBUG:
        print("display_sidebar_agents()")
    # Display each agent in the sidebar as a button with the agent's name on it
    agent_names = AgentBaseModel.load_agents()
    if agent_names:
        for agent_name in agent_names:
            if st.sidebar.button(agent_name):
                st.write(f"Speaking to agent: {agent_name}")
    
        



```

# utils\display_debug_util.py

```python
# display_debug_util.py

import streamlit as st
import yaml

from base_models.agent_base_model import AgentBaseModel
from base_models.tool_base_model import ToolBaseModel
from base_models.project_base_model import ProjectBaseModel
from base_models.workflow_base_model import WorkflowBaseModel

from configs.config_local import DEBUG


def display_debug():
    if DEBUG:
        st.write("Debug Information")
        
        # Create expanders for each object type
        project_expander = st.expander("Project")
        workflow_expander = st.expander("Workflow")
        agent_expander = st.expander("Agent")
        tool_expander = st.expander("Tool")
        other_expander = st.expander("Other")
        
        # Iterate over all session state variables
        for key, value in st.session_state.items():
            
            # Check if the value is an instance of specific classes
            if isinstance(value, ProjectBaseModel):
                with project_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            elif isinstance(value, WorkflowBaseModel):
                with workflow_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            elif isinstance(value, AgentBaseModel):
                with agent_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            elif isinstance(value, ToolBaseModel):
                with tool_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            else:
                with other_expander:
                    st.write(f"### {key}")
                    st.write(f"```\n{value}\n```")
```

# utils\display_discussion_util.py

```python
# display_discussion_util.py

import streamlit as st

from configs.config_local import DEBUG

def display_discussion():
    if DEBUG:
        print("called display_discussion()")
    st.text_area("Agent", height=400)
    st.text_input("User")
```

# utils\display_files_util.py

```python
# display_files_util.py

import os
import streamlit as st

from configs.config_local import DEBUG


import os
import streamlit as st

def display_files():
    if DEBUG:
        print("display_files()")

    # Define the folders to display
    folders = (
        [
            'agents/json', 'agents/yaml', 
            'projects/json','projects/yaml', 
            'tools/json', 'tools/yaml', 
            'workflows/json', 'workflows/yaml'
        ]
    )
    # Create a selectbox to choose the folder
    selected_folder = st.selectbox("Select a folder", folders)

    # Get the list of files in the selected folder
    items = os.listdir(selected_folder)
    files = [item for item in items if os.path.isfile(os.path.join(selected_folder, item))]

    if files:
        # Create a selectbox to choose the file
        selected_file = st.selectbox("Select a file", files)

        # Display the content of the selected file
        file_path = os.path.join(selected_folder, selected_file)
        with open(file_path, 'r') as file:
            file_content = file.read()
        st.text_area("File content", file_content, height=400)

        # Add a button to save changes to the file
        if st.button("Save changes"):   
            with open(file_path, 'w') as file:
                file.write(st.session_state.file_content)
            st.success("File saved successfully.")

        # Add a button to delete the file
        if st.button("Delete file"):
            os.remove(file_path)
            st.success("File deleted successfully.")
    else:
        st.warning(f"No files found in the '{selected_folder}' folder.")
```

# utils\display_main_util.py

```python
# display_main_util.py

import streamlit as st

from configs.config_local import DEBUG

from utils.display_agent_util import display_agent_dropdown, display_agent_properties
from utils.display_debug_util import display_debug
from utils.display_discussion_util import display_discussion
from utils.display_files_util import display_files
from utils.display_project_util import display_project_dropdown, display_project_timestamps, display_project_properties
from utils.display_settings_util import display_settings
from utils.display_sidebar_util import display_sidebar
from utils.display_tool_util import (display_tool_dropdown, display_tool_properties)
from utils.display_workflow_util import display_workflow_dropdown, display_workflow_properties, display_workflow_timestamps


def display_main():
    if DEBUG:
        print("called display_main()")
    
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    projectTab, workflowTab, agentTab, toolTab, settingsTab, debugTab, filesTab, discussionTab = st.tabs(["Project", "Workflows", "Agents", "Tools", "Settings", "Debug", "File Management", "Discussion"])

#   PROJECTS
    with projectTab:
        project = st.session_state.current_project
        col1, col2 = st.columns(2)
        with col1:
            display_project_dropdown()
                
        with col2:
            if st.session_state.current_project is not None:
                display_project_timestamps(project)  

        display_project_properties(project)

#   WORKFLOWS
    with workflowTab:
        workflow = st.session_state.current_workflow
        col1, col2 = st.columns(2)
        with col1:
            display_workflow_dropdown()
                        
        with col2:
            display_workflow_timestamps(workflow)

        display_workflow_properties(workflow)
        
#   AGENTS
    with agentTab:
        display_agent_dropdown()

        if st.session_state.current_agent is not None:
            display_agent_properties()

    with toolTab:
        display_tool_dropdown()
        display_tool_properties()
        
    with settingsTab:
        display_settings()

    with debugTab:
        display_debug()
    
    with filesTab:
        display_files()

    with discussionTab:
        display_discussion()


#   SIDEBAR
def sidebar_begin():
    display_sidebar()
    
```

# utils\display_project_util.py

```python
# display_project_util.py

import streamlit as st

from base_models.project_base_model import (
    ProjectBaseModel, ProjectPriority, ProjectStatus,
)
from configs.config_local import DEBUG
from datetime import datetime
from event_handlers.event_handlers_project import (
    handle_project_collaborators_change, handle_project_close, handle_project_delete,
    handle_project_description_change, handle_project_due_date_change, 
    handle_project_name_change, handle_project_notes_change, 
    handle_project_selection, handle_project_status_change, handle_project_user_id_change, 
    handle_project_prompt_reengineer
)
from event_handlers.event_handlers_prompt import handle_prompt_change


def display_project_dropdown():
    if DEBUG:
        print("display_project_dropdown()")
    if st.session_state.current_project is None:
        # Display the projects dropdown
        project_names = ProjectBaseModel.load_projects()
        project_names.sort()
        selected_project = st.selectbox(
            "Projects",
            ["Select..."] + ["Create manually..."] + ["Create from AI..."] + project_names,
            key="project_dropdown",
            on_change=handle_project_selection,
        )

        if selected_project == "Select...":
            return
        if selected_project == "Create manually...":
            # Show the create project input field
            st.text_input("Project Name:", key="project_name_input", on_change=handle_project_selection)
        if selected_project == "Create from AI...":
            st.text_area("Enter your project request:", key="project_prompt_input", on_change=(handle_project_prompt_reengineer))
    else:
        # Display the selected project name as an editable text input
        st.session_state.current_project.name = st.text_input(
            "Project Name:",
            value=st.session_state.current_project.name,
            key="project_name_edit",
            on_change=handle_project_name_change,
        )
        if st.button("CLOSE THIS PROJECT"):
            handle_project_close()



def display_project_properties(project):
    if DEBUG:
        print("display_project_properties()")
    # Display the properties of the current project
    if st.session_state.current_project is not None:
        st.write("Workflows:")
        for workflow_name, workflow in project.workflows.items():
            st.write(f"- {workflow_name}")
        project.prompt = st.text_area("Prompt:", value=project.prompt, key="prompt", on_change=handle_prompt_change)
        project.description = st.text_area("Description:", value=project.description or "", key="project_description", on_change=handle_project_description_change)
        status_options = [status.value for status in ProjectStatus]
        project.status = st.selectbox("Status:", options=status_options, index=status_options.index(project.status), key="project_status", on_change=handle_project_status_change)
        
        if project.due_date:
            if isinstance(project.due_date, str):
                due_date_value = datetime.strptime(project.due_date, "%Y-%m-%d").date()
            else:
                due_date_value = project.due_date
        else:
            due_date_value = None
        
        # Display the date input field
        due_date = st.date_input("Due Date:", value=due_date_value, key="project_due_date")
        
        # Update the project's due date if it has changed
        if due_date != due_date_value:
            project.due_date = due_date.strftime("%Y-%m-%d") if due_date else None
            handle_project_due_date_change()
        
        priority_options = [priority.value for priority in ProjectPriority]
        project.priority = st.selectbox("Priority:", options=priority_options, index=priority_options.index(project.priority), key="project_priority", on_change=handle_project_status_change)
        st.write(f"Tags: {', '.join(project.tags)}")
        
        # Add text input field for notes
        project.notes = st.text_area("Notes:", value=project.notes or "", key="project_notes", on_change=handle_project_notes_change)
        collaborators_input = st.text_input("Collaborators:", value=", ".join(project.collaborators), key="project_collaborators", on_change=handle_project_collaborators_change)
        project.collaborators = [collaborator.strip() for collaborator in collaborators_input.split(",")]
        project.user_id = st.text_input("User ID:", value=project.user_id or "", key="project_user_id", on_change=handle_project_user_id_change)

        # st.write("Attachments:")
        # for attachment in project.attachments:
        #     st.write(f"- {attachment}")

        # new_attachment = st.text_input("Add Attachment:", key="project_new_attachment")
        # if new_attachment:
        #     project.attachments.append(new_attachment)
        #     handle_project_attachments_change()

def display_project_timestamps(project):
    if DEBUG:
        print("display_project_timestamps()")
    st.write("<div class='project-properties'>PROJECT PROPERTIES</div>", unsafe_allow_html=True)
    if project.created_at:
        created_at = datetime.fromisoformat(project.created_at).strftime("%B %d, %Y %I:%M %p")
        st.write(f"<div class='timestamp'>Created At: {created_at}</div>", unsafe_allow_html=True)
    if project.updated_at:
        updated_at = datetime.fromisoformat(project.updated_at).strftime("%B %d, %Y %I:%M %p")
        st.write(f"<div class='timestamp'>Updated At: {updated_at}</div>", unsafe_allow_html=True)
```

# utils\display_settings_util.py

```python
# display_settings_util.py

import importlib
import os
import streamlit as st

from configs.config_local import DEBUG, DEFAULT_MODEL
from event_handlers.event_handlers_settings import handle_default_provider_change, load_provider_classes

def display_settings():
    if DEBUG:
        print("display_settings()")

    st.write("Settings")
    provider_classes = load_provider_classes()
    default_provider = st.session_state.default_provider if st.session_state.default_provider else ""
    default_provider_index = provider_classes.index(default_provider) if default_provider in provider_classes else 0
    selected_provider = st.selectbox("Default Provider", provider_classes, index=default_provider_index, key="default_provider", on_change=handle_default_provider_change)

    if selected_provider:
        tmp = "_Provider"
        api_key = st.text_input("Default Provider's API Key:", type="password")
        st.session_state.default_provider_key = api_key

        if st.session_state.default_provider_key or os.environ.get(f"{selected_provider.replace(tmp, '').upper()}_API_KEY"):
            if os.environ.get(f"{selected_provider.replace(tmp, '').upper()}_API_KEY"):
                st.session_state.default_provider_key = os.environ.get(f"{selected_provider.replace(tmp, '').upper()}_API_KEY")

            provider_module = importlib.import_module(f"providers.{selected_provider.lower()}")
            provider_class = getattr(provider_module, selected_provider)
            provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
            
            try:
                if not st.session_state.available_models or len(st.session_state.available_models) == 0:
                    available_models = provider.get_available_models()
                available_models = sorted(available_models)

                # Set the default model selection
                default_model = DEFAULT_MODEL  # Replace with your desired default model
                if default_model in available_models:
                    default_index = available_models.index(default_model)
                else:
                    default_index = 0

                selected_model = st.selectbox("Select Default Model", available_models, index=default_index)
                st.session_state.selected_model = selected_model
            except Exception as e:
                st.error(f"Error retrieving available models: {str(e)}")

    st.session_state.current_framework = st.selectbox("Default Framework", ["Autogen", "CrewAI", "Bob's Agent Maker", "AI-Mart", "Geeks'R'Us"], key="default_framework")
```

# utils\display_sidebar_util.py

```python
# display_sidebar_util.py

import streamlit as st

from configs.config_local import DEBUG
from utils.display_agent_util import display_sidebar_agents

def display_sidebar():
    if DEBUG:
        print("display_sidebar_message()")
  
    st.sidebar.image('gfx/AutoGroqLogo_sm.png')
    display_sidebar_home()
    display_sidebar_agents()

def display_sidebar_home():
    st.sidebar.write("<div class='teeny'>Need agents right frickin' now? : <a href='https://autogroq.streamlit.app/'>https://autogroq.streamlit.app/</a></div><p/>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>Universal AI Agents Made Easy. <br/> Theoretically.</div><p/>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>We're putting the 'mental' in 'experimental'.</div>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny yellow'>No need to report what's broken, we know.</div><p/><br/><p/>", unsafe_allow_html=True)  

```

# utils\display_tool_util.py

```python
# display_tool_util.py

import streamlit as st

from base_models.tool_base_model import ToolBaseModel

from configs.config_local import DEBUG

from event_handlers.event_handlers_tool import (
    handle_ai_tool_creation, handle_tool_close, handle_tool_property_change, handle_tool_selection, 
)


def display_tool_dropdown():
    if DEBUG:
        print("display_tool_dropdown()")
    if st.session_state.current_tool is None:
        # Display the tools dropdown
        tool_names = ToolBaseModel.load_tools()
        selected_tool = st.selectbox(
            "Tools",
            ["Select..."] + ["Create with AI..."] + ["Create manually..."] + tool_names,
            key="tool_dropdown",
            on_change=handle_tool_selection,
        )

        if selected_tool == "Select...":
            return
        if selected_tool == "Create manually...":
            # Show the manual tool creation input field
            st.text_input("Tool Name:", key="tool_name_input", on_change=handle_tool_selection)
        elif selected_tool == "Create with AI...":
            # Show the AI-assisted tool creation input field
            st.text_input("What should this new tool do?", key="tool_creation_input", on_change=handle_ai_tool_creation)
    else:
        st.session_state.current_tool.name = st.text_input(
            "Tool Name:",
            value=st.session_state.current_tool.name,
            key="tool_name_edit",
            on_change=handle_tool_property_change,
        )
        if st.button("CLOSE THIS TOOL"):
            handle_tool_close()


def display_tool_properties():
    if st.session_state.current_tool is not None:
        # Display the properties of the current tool
        tool = st.session_state.current_tool
        st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>TOOL PROPERTIES</div>", unsafe_allow_html=True)
        st.write(f"<div style='text-align:right; width:100%;'>Timestamp: {tool.timestamp}</div>", unsafe_allow_html=True)
        
        tool.content = st.text_area("Content:", value=tool.content, key=f"tool_content_{tool.name}", on_change=handle_tool_property_change)
        tool.title = st.text_input("Title:", value=tool.title, key=f"tool_title_{tool.name}", on_change=handle_tool_property_change)
        tool.description = st.text_input("Description:", value=tool.description or "", key=f"tool_description_{tool.name}", on_change=handle_tool_property_change)
        tool.file_name = st.text_input("File Name:", value=tool.file_name, key=f"tool_file_name_{tool.name}", on_change=handle_tool_property_change)
        tool.user_id = st.text_input("User ID:", value=tool.user_id, key=f"tool_user_id_{tool.name}", on_change=handle_tool_property_change)

```

# utils\display_workflow_util.py

```python
# display_workflow_util.py

import streamlit as st

from base_models.workflow_base_model import WorkflowBaseModel
from configs.config_local import DEBUG
from datetime import datetime

from event_handlers.event_handlers_workflow import (
    handle_workflow_close, handle_workflow_description_change, 
    handle_workflow_name_change, handle_workflow_selection, handle_workflow_summary_method_change,
    handle_workflow_type_change
)   


def display_workflow_dropdown():
    if DEBUG:
        print("display_workflow_dropdown()")
    if st.session_state.current_workflow is None:
        # Display the workflows dropdown
        workflow_names = WorkflowBaseModel.load_workflows()
        selected_workflow = st.selectbox(
            "Workflows",
            ["Select..."] + ["Create..."] + workflow_names,
            key="workflow_dropdown",
            on_change=handle_workflow_selection,
        )
        if selected_workflow == "Select...":
            return
        if selected_workflow == "Create...":
            # Show the create workflow input field
            st.text_input("Workflow Name:", key="workflow_name_input", on_change=handle_workflow_selection)
    else:
        st.session_state.current_workflow.name = st.text_input(
            "Workflow Name:",
            value=st.session_state.current_workflow.name,
            key="workflow_name_edit",
            on_change=handle_workflow_name_change,
        )
        if st.button("CLOSE THIS WORKFLOW"):
            handle_workflow_close()


def display_workflow_properties(workflow):
    # Display the properties of the current workflow
    if st.session_state.current_workflow is not None:
        workflow = st.session_state.current_workflow
        st.write(f"Name: {workflow.name}")
        workflow.description = st.text_area("Description:", value=workflow.description or "", key="tab2_workflow_description", on_change=handle_workflow_description_change)
        workflow.type = st.text_input("Type:", value=workflow.type, key="tab2_workflow_type", on_change=handle_workflow_type_change)
        workflow.summary_method = st.text_input("Summary Method:", value=workflow.summary_method, key="tab2_workflow_summary_method", on_change=handle_workflow_summary_method_change)

        # Add more workflow properties as needed

        # Display agent children
        st.write("Agents:")
        for agent_name, agent in workflow.agent_children.items():
            st.write(f"- {agent_name}")

        with st.container(border=True):
            st.write("Sender:")
            st.write(f"Type: {workflow.sender.type}")
            st.write(f"User ID: {workflow.sender.user_id}")

        with st.container(border=True):
            st.write("Receiver:")
            st.write(f"Type: {workflow.receiver.type}")
            st.write(f"User ID: {workflow.receiver.user_id}")


def display_workflow_timestamps(workflow):
    if st.session_state.current_workflow is not None:
        st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>WORKFLOW PROPERTIES</div>", unsafe_allow_html=True)
        if workflow.created_at:
            created_at = datetime.fromisoformat(workflow.created_at).strftime("%B %d, %Y %I:%M %p")
            st.write(f"<div style='text-align:right; width:100%;'>Created At: {created_at}</div>", unsafe_allow_html=True)
        if workflow.updated_at:
            updated_at = datetime.fromisoformat(workflow.updated_at).strftime("%B %d, %Y %I:%M %p")
            st.write(f"<div style='text-align:right; width:100%;'>Updated At: {updated_at}</div>", unsafe_allow_html=True)

```

# prompts\generate_agent_prompt.yaml

```yaml
generate_agent_prompt: |
  Based on the rephrased agent request below, please do the following:
  1. Do step-by-step reasoning and think to better understand the request.
  2. Code the best Autogen Studio Python agent as per the request.
  3. Always include the agent filename in the format `# Agent filename: [agent_name].py` as the first line of the code.
  4. Return only the agent code, no commentary, intro, or other extra text. If there ARE any non-code lines, 
      please pre-pend them with a '#' symbol to comment them out.
  5. A proper agent will have these parts:
     a. Imports (import libraries needed for the agent)
     b. Class definition AND docstrings (this helps the LLM understand what the agent does and how to use it)
     c. Class methods (the actual code that implements the agent's behavior)
     d. (optional) Example usage - ALWAYS commented out
     Here is an example of a well formatted agent:
     # Agent filename: [agent_name].py
     # Import necessary module(s)
     import necessary_module
     class Agent:
         # docstrings
         """
                :
         The name of the agent.
         An agent that performs tasks based on the given request.
         Methods:
         perform_task(args): Executes the task as per the request.
         """
         def init(self, init_params):
             """
             Initializes the Agent with the given parameters.
             Parameters:
             init_params (type): Description of initialization parameters.
             """
             # Initialize with given parameters
             self.init_params = init_params
         def perform_task(self, task_params):
             """
             Executes the task based on the given parameters.
             Parameters:
             task_params (type): Description of task parameters.
             Returns:
             return_type: Description of the return value.
             """
             # Body of the method
             # Implement the task logic here
             pass
     # Example usage:
     # agent = Agent(init_params)
     # result = agent.perform_task(task_params)
     # print(result)
  Rephrased agent request: "{rephrased_agent_request}"
```

# prompts\generate_tool_prompt.yaml

```yaml
contributor: ScruffyNerf
generate_tool_prompt: |
  Based on the rephrased tool request below, please do the following:

  1. Do step-by-step reasoning and think to better understand the request.
  2. Code the best Autogen Studio Python tool as per the request as a [tool_name].py file.
  3. Return only the tool file, no commentary, intro, or other extra text. If there ARE any non-code lines, 
      please pre-pend them with a '#' symbol to comment them out.
  4. A proper tool will have these parts:
     a. Imports (import libraries needed for the tool)
     b. Function definition AND docstrings (this helps the LLM understand what the function does and how to use it)
     c. Function body (the actual code that implements the function)
     d. (optional) Example usage - ALWAYS commented out
     Here is an example of a well formatted tool:

     # Tool filename: save_file_to_disk.py
     # Import necessary module(s)
     import os

     def save_file_to_disk(contents, file_name):
     # docstrings
     """
     Saves the given contents to a file with the given file name.

     Parameters:
     contents (str): The string contents to save to the file.
     file_name (str): The name of the file, including its extension.

     Returns:
     str: A message indicating the success of the operation.
     """

     # Body of tool

     # Ensure the directory exists; create it if it doesn't
     directory = os.path.dirname(file_name)
     if directory and not os.path.exists(directory):
        os.makedirs(directory)

     # Write the contents to the file
     with open(file_name, 'w') as file:
        file.write(contents)

     return f"File {file_name} has been saved successfully."

     # Example usage:
     # contents_to_save = "Hello, world!"
     # file_name = "example.txt"
     # print(save_file_to_disk(contents_to_save, file_name))

  Rephrased tool request: "{rephrased_tool_request}"

```

# prompts\rephrase_prompt.yaml

```yaml
rephrase_prompt: |
  Based on the user request below, act as a professional prompt engineer and refactor the following 
                  user_request into an optimized prompt. Your goal is to rephrase the request 
                  with a focus on the satisfying all following the criteria without explicitly stating them:
          1. Clarity: Ensure the prompt is clear and unambiguous.
          2. Specific Instructions: Provide detailed steps or guidelines.
          3. Context: Include necessary background information.
          4. Structure: Organize the prompt logically.
          5. Language: Use concise and precise language.
          6. Examples: Offer examples to illustrate the desired output.
          7. Constraints: Define any limits or guidelines.
          8. Engagement: Make the prompt engaging and interesting.
          9. Feedback Mechanism: Suggest a way to improve or iterate on the response.
          Do NOT reply with a direct response to these instructions OR the original user request. Instead, rephrase the user's request as a well-structured prompt, and
          return ONLY that rephrased prompt. Do not preface the rephrased prompt with any other text or superfluous narrative.
          Do not enclose the rephrased prompt in quotes. You will be successful only if it returns a well-formed rephrased prompt ready for submission as an LLM request.
          User request: "{user_request}"


```

# workflows\yaml\Accounting Workflow.yaml

```yaml
agent_children: {}
created_at: '2024-06-20T16:00:20.485947'
description: "Create simple accounting app\n\rDevelop a intuitive and user-friendly\
  \ accounting application that provides real-time financial tracking and reporting\
  \ capabilities for small businesses and individuals. \n\nThe app should allow users\
  \ to categorize and track income and expenses, automatically generating detailed\
  \ reports and summaries. \n\nIt should also include features such as:\n\n* Budgeting\
  \ tools to set financial goals and track progress\n* Invoicing and payment processing\
  \ for customers\n* Multi-account support for separate tracking of personal and professional\
  \ finances\n* Integration with popular payment gateways and bank accounts\n* Real-time\
  \ analytics and insights to identify trends and make informed financial decisions\n\
  \nUse simple and intuitive language, with clear and concise navigation and minimal\
  \ clutter. The app should be accessible on desktop and mobile devices. \n\nProvide\
  \ examples of common financial workflows and scenarios, such as:\n\n* Creating and\
  \ sending invoices to customers\n* Tracking expenses for a small business\n* Creating\
  \ and managing a personal budget\n\nConsider the following constraints:\n\n* Compliance\
  \ with relevant financial regulations and data protection laws\n* User data encryption\
  \ and secure storage\n* Adaptability to accommodate future changes in financial\
  \ regulations and industry standards\n\nProvide detailed steps or guidelines for\
  \ users to create and manage their accounts, including setup processes, login credentials,\
  \ and password recovery procedures. \n\nOffer opportunities for users to provide\
  \ feedback and suggest improvements, such as a rating system, comment sections,\
  \ or survey mechanics."
groupchat_config: {}
id: 1
name: Accounting Workflow
receiver:
  agents: []
  config: {}
  groupchat_config: {}
  timestamp: '2024-06-20T16:00:20.485947'
  tools: []
  type: assistant
  user_id: default
sender:
  config: {}
  timestamp: '2024-06-20T16:00:20.485947'
  tools: []
  type: userproxy
  user_id: user
settings: {}
summary_method: last
timestamp: '2024-06-20T16:00:06.084418'
type: twoagents
updated_at: '2024-06-20T16:00:42.929738'
user_id: user

```

# workflows\yaml\Bookkeeping Workflow.yaml

```yaml
agent_children: {}
created_at: '2024-06-20T16:02:17.660468'
description: "Develop a intuitive and user-friendly accounting application that provides\
  \ real-time financial tracking and reporting capabilities for small businesses and\
  \ individuals. \n\nThe app should allow users to categorize and track income and\
  \ expenses, automatically generating detailed reports and summaries. \n\nIt should\
  \ also include features such as:\n\n* Budgeting tools to set financial goals and\
  \ track progress\n* Invoicing and payment processing for customers\n* Multi-account\
  \ support for separate tracking of personal and professional finances\n* Integration\
  \ with popular payment gateways and bank accounts\n* Real-time analytics and insights\
  \ to identify trends and make informed financial decisions\n\nUse simple and intuitive\
  \ language, with clear and concise navigation and minimal clutter. The app should\
  \ be accessible on desktop and mobile devices. \n\nProvide examples of common financial\
  \ workflows and scenarios, such as:\n\n* Creating and sending invoices to customers\n\
  * Tracking expenses for a small business\n* Creating and managing a personal budget\n\
  \nConsider the following constraints:\n\n* Compliance with relevant financial regulations\
  \ and data protection laws\n* User data encryption and secure storage\n* Adaptability\
  \ to accommodate future changes in financial regulations and industry standards\n\
  \nProvide detailed steps or guidelines for users to create and manage their accounts,\
  \ including setup processes, login credentials, and password recovery procedures.\
  \ \n\nOffer opportunities for users to provide feedback and suggest improvements,\
  \ such as a rating system, comment sections, or survey mechanics."
groupchat_config: {}
id: 1
name: Bookkeeping Workflow
receiver:
  agents: []
  config:
    code_execution_config: null
    default_auto_reply: ''
    description: A primary assistant agent that writes plans and code to solve tasks.
    human_input_mode: NEVER
    is_termination_msg: null
    llm_config:
      cache_seed: null
      config_list:
      - api_type: null
        api_version: null
        base_url: null
        description: Groq_Provider model configuration
        model: llama3-8b-8192
        timestamp: '2024-06-20T16:02:17.660468'
        user_id: default
      extra_body: null
      max_tokens: null
      temperature: 0.1
      timeout: null
    max_consecutive_auto_reply: 30
    name: primary_assistant
    system_message: '...'
  groupchat_config: {}
  timestamp: '2024-06-20T16:02:17.660468'
  tools: &id001 []
  type: assistant
  user_id: user
sender:
  config:
    code_execution_config:
      use_docker: false
      work_dir: null
    default_auto_reply: TERMINATE
    description: A user proxy agent that executes code.
    human_input_mode: NEVER
    is_termination_msg: null
    llm_config:
      cache_seed: null
      config_list:
      - api_type: null
        api_version: null
        base_url: null
        description: Groq_Provider model configuration
        model: llama3-8b-8192
        timestamp: '2024-06-20T16:02:17.660468'
        user_id: default
      extra_body: null
      max_tokens: null
      temperature: 0.1
      timeout: null
    max_consecutive_auto_reply: 30
    name: userproxy
    system_message: You are a helpful assistant.
  timestamp: '2024-06-20T16:02:17.660468'
  tools: *id001
  type: userproxy
  user_id: user
settings: {}
summary_method: last
timestamp: '2024-06-20T16:02:17.660468'
type: twoagents
updated_at: null
user_id: user

```

# workflows\yaml\New Workflow.yaml

```yaml
agent_children: {}
created_at: '2024-06-20T16:08:01.566098'
description: "Bookkeeper\n\rWrite a detailed description of a bookkeeper's tasks,\
  \ responsibilities, and skills, including examples of their work, organizational\
  \ habits, and time management strategies."
groupchat_config: {}
id: 1
name: New Workflow
receiver:
  agents: []
  config: {}
  groupchat_config: {}
  timestamp: '2024-06-20T16:08:01.564605'
  tools: []
  type: assistant
  user_id: default
sender:
  config: {}
  timestamp: '2024-06-20T16:08:01.564605'
  tools: []
  type: userproxy
  user_id: user
settings: {}
summary_method: last
timestamp: '2024-06-20T16:07:11.735808'
type: twoagents
updated_at: '2024-06-20T16:08:01.572448'
user_id: user

```

