"""
This file is used to import all the models in the models folder.
location: backend/app/models/__init__.py
"""

from .base_model import Base
from .user_model import User
from .agent_model import AgentData
from .automate_event_model import AutomateEvent
from .task_model import Task
from .workflow_model import Workflow
from .trigger_model import Trigger
