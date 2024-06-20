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
    