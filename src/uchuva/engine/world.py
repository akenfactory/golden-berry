# -*- coding: utf-8 -*-
"""
----------------------------------------------------------
------------------------- UCHUVA -------------------------
----------------------------------------------------------

@autor AKEN
@version 1.0.1
@date 06/08/24
"""

# --------------------------------------------------------
# Define resources
# --------------------------------------------------------

from abc import ABC, abstractmethod
from uchuva.engine.agent import Agent

# --------------------------------------------------------
# Define component
# --------------------------------------------------------

class World(ABC):
	""" Represents a system world """
	
	def __init__(self) -> None:
		""" World constructor method """
		self.agent = None
		super().__init__()
	
	@abstractmethod
	def update(self, event, data) -> None:
		""" Update the world state """
		pass

	def set_agent(self, agent:Agent) -> None:
		""" Set the agent """
		self.agent = agent
