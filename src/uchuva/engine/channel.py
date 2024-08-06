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

from uchuva.engine.queue import Queue

# --------------------------------------------------------
# Define component
# --------------------------------------------------------

class Channel():
    """ Represents a channel for communication between agents """

    def __init__(self, queue:Queue) -> None:
        """ Channel constructor method """
        self.queue = queue
        super().__init__()
    
    def send_event(self, num):
        """ Send a event to the channel """
        self.queue.put(num)