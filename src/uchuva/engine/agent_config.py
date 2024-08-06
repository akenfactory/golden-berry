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

from uchuva.engine.exceptions import AgentException

# --------------------------------------------------------
# Define component
# --------------------------------------------------------

class AgentConfig():
    """ Represents a configuration for a agent """

    def __init__(self, agent_id:str, db = None) -> None:
        """
        Configuration constructor method.
        @param agentID:str Unic agent ID
        """
        try:
            if agent_id and isinstance(agent_id, str):
                self.id = agent_id
            else:
                raise AgentException("Agent ID must be a string type")
            self.db = db    
        except AgentException as e:
            raise e