"""
Base Trading Agent - Foundation for all specialized agents in EDMAS.
Implements core survival mechanisms, state management, and evolutionary interfaces.
"""
import logging
import asyncio
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
import firebase_admin
from firebase_admin import firestore, credentials
from dataclasses import dataclass, asdict
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class AgentState:
    """Immutable agent state container for reliable state management"""
    agent_id: str
    agent_type: str
    status: str  # ACTIVE, PAUSED, EVOLVING, FAILED
    performance_score: float
    created_at: datetime
    last_heartbeat: datetime
    configuration_hash: str
    memory_usage_mb: float
    error_count: int = 0
    success_count: int = 0
    
    def to_firestore_dict(self) -> Dict[str, Any]:
        """Convert to Firestore-compatible dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_heartbeat'] = self.last_heartbeat.isoformat()
        return data
    
    @classmethod
    def from_firestore_dict(cls, data: Dict[str, Any]) -> 'AgentState':
        """Create from Firestore dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_heartbeat'] = datetime.fromisoformat(data['last_heartbeat'])
        return cls(**data)


class BaseTradingAgent(ABC):
    """
    Abstract base class for all EDMAS trading agents.
    Implements core survival patterns and Firebase state management.
    """
    
    def __init__(
        self, 
        agent_id: Optional[str] = None,
        agent_type: str = "generic",
        firebase_project_id: Optional[str] = None,
        firebase_credentials_path: Optional[str] = None
    ):
        """
        Initialize base agent with essential survival mechanisms.
        
        Args:
            agent_id: Unique identifier for this agent instance
            agent_type: Type of agent (analyzer, risk, execution, etc.)
            firebase_project_id: Firebase project ID
            firebase_credentials_path: Path to Firebase credentials JSON
        """
        # Initialize agent identity
        self.agent_id = agent_id or f"{agent_type}_{uuid.uuid4().hex[:8]}"
        self.agent_type = agent