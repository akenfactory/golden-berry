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

class Action(ABC):
    """ Represents the reaction to the occurrence of an event """
    
    def __init__(self) -> None:
        """ Action constructor method """
        self.id = None
        self.log = None
        self.adm = None
        self.agent = None      
        super().__init__()
        
    @abstractmethod
    def run(self, data:dict) -> None:
        """ Run the action 
        @param data:dict Data to run the action
        """
        pass

    def set_agent(self, agent:Agent) -> None:
        """ Set the agent
        @param agent:Agent The agent
        """
        self.agent = agent
        self.log = agent.log