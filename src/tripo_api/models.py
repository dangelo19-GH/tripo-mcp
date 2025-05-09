"""
Data models for the Tripo API client.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import datetime


class TaskStatus(str, Enum):
    """Task status enum."""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"
    BANNED = "banned"
    EXPIRED = "expired"


class TopologyType(str, Enum):
    """Topology type enum."""
    BIP = "bip"
    QUAD = "quad"


@dataclass
class TaskOutput:
    """Task output data."""
    model: Optional[str] = None
    base_model: Optional[str] = None
    pbr_model: Optional[str] = None
    rendered_image: Optional[str] = None
    riggable: Optional[bool] = None
    topology: Optional[TopologyType] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskOutput':
        """Create a TaskOutput from a dictionary."""
        topology = data.get('topology')
        if topology and isinstance(topology, str):
            try:
                topology = TopologyType(topology)
            except ValueError:
                topology = None
                
        return cls(
            model=data.get('model'),
            base_model=data.get('base_model'),
            pbr_model=data.get('pbr_model'),
            rendered_image=data.get('rendered_image'),
            riggable=data.get('riggable'),
            topology=topology
        )


@dataclass
class Task:
    """Task data model."""
    task_id: str
    type: str
    status: TaskStatus
    input: Dict[str, Any]
    output: TaskOutput
    progress: int
    create_time: int
    
    @property
    def created_at(self) -> datetime.datetime:
        """Get the creation time as a datetime object."""
        return datetime.datetime.fromtimestamp(self.create_time)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a Task from a dictionary."""
        return cls(
            task_id=data['task_id'],
            type=data['type'],
            status=TaskStatus(data['status']),
            input=data['input'],
            output=TaskOutput.from_dict(data['output']),
            progress=data['progress'],
            create_time=data['create_time']
        )


@dataclass
class Balance:
    """User balance data model."""
    balance: float
    frozen: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Balance':
        """Create a Balance from a dictionary."""
        return cls(
            balance=data['balance'],
            frozen=data['frozen']
        ) 