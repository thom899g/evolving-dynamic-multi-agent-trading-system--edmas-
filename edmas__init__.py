"""
Evolving Dynamic Multi-Agent Trading System (EDMAS)
A decentralized AI-driven platform where specialized agents collaborate and compete,
adapting in real-time to market conditions through self-directed learning and evolution.
"""

__version__ = "1.0.0"
__author__ = "EDMAS Core Team"

from edmas.base_agent import BaseTradingAgent
from edmas.market_analyzer_agent import MarketAnalyzerAgent
from edmas.risk_manager_agent import RiskManagerAgent
from edmas.execution_agent import ExecutionAgent
from edmas.evolution_coordinator import EvolutionCoordinator

__all__ = [
    'BaseTradingAgent',
    'MarketAnalyzerAgent', 
    'RiskManagerAgent',
    'ExecutionAgent',
    'EvolutionCoordinator'
]