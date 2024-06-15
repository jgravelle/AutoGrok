# project_base_model.py

import enum
import os
import yaml

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
        workflows: Optional[List[Dict]] = None
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
        self.workflows = workflows or []

    def add_deliverable(self, deliverable: str):
        self.deliverables.append({"text": deliverable, "done": False})

    @classmethod
    def create_project(cls, project_name: str) -> "ProjectBaseModel":
        project = cls(name=project_name)
        
        # Create a YAML file for the project
        project_data = project.to_dict()
        with open(f"projects/{project_name}.yaml", "w") as file:
            yaml.dump(project_data, file)
        
        return project
    

    @classmethod
    def get_project(cls, project_name: str) -> "ProjectBaseModel":
        file_path = f"projects/{project_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                project_data = yaml.safe_load(file)
                return cls.from_dict(project_data)
        else:
            raise FileNotFoundError(f"Project file not found: {file_path}")
            

    @staticmethod
    def load_projects() -> List[str]:
        project_names = []
        for file in os.listdir("projects"):
            if file.endswith(".yaml"):
                project_name = file[:-5]  # Remove the ".yaml" extension
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
            "workflows": self.workflows
        }

    @classmethod
    def from_dict(cls, data: Dict):
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
            workflows=data.get("workflows", [])
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