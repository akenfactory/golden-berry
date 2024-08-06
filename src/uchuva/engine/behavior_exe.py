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

import traceback
from threading import Thread
from uchuva.engine.queue import Queue

# --------------------------------------------------------
# Define component
# --------------------------------------------------------
class BehaviorExe(Thread):
    """ Behavior executor component """

    def __init__(self, queue):
        self.__let = False
        self.__alive = True
        self.__stop_agent = Queue(1)
        self.__queue = queue
        super().__init__()

    def execute(self):
        while self.__alive:
            evt = self.__queue.get()
            if not self.__let:
                self.__stop_agent.get()
            try:
                if self.__alive:
                    evt['action'].run(evt['data'])
            except Exception as e:
                traceback.print_exc()
                self.__let = False        
            self.__queue.task_done()
        
    def set_let(self, val):
        self.__let = val
       
    def notify_let(self, val):
        self.__stop_agent.put(None)
        
    def set_alive(self, val):
        self.__alive = val

    def finalize(self):
        self.__let = False
        self.__queue.put(None)
        self.__stop_agent.put(None)
