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

import logging
from abc import ABC, abstractmethod
from uchuva.engine.queue import Queue
from uchuva.engine.action import Action
from uchuva.engine.channel import Channel
from uchuva.engine.agent_config import AgentConfig
from uchuva.engine.behavior_exe import BehaviorExe
from uchuva.engine.exceptions import AgentException

# --------------------------------------------------------
# Define component
# --------------------------------------------------------

class Agent(ABC):
    """ Represents a system agent """
    
    def __init__(self, config:AgentConfig) -> None:
        """
        Agent constructor method.
        @param agentID:str Unic agent ID
        """    
        self.id = config.agent_id
        self.config = config
        self.state = {}
        self.__events_table = {}
        self.__channels_table = {}
        self.__worker_list = []
        self.__channel_list = []
        self.__behaviors = {}
        self.log = None
        self.db = None
        # Check if the agent is persistent
        if self.config.is_persist:
            # Create MongoDB colletion
            self.db = config.db
        self.__build_agent()
        super().__init__()
        
    
    def __build_agent(self) -> None:
        """ Build the agent structure """
        self.setup()
        # Create the agent behaviors
        if len(self.__behaviors) > 0: 
            for key, beh in self.__behaviors.items():            
                queue = Queue(100)
                channel = Channel(queue)    
                worker = BehaviorExe(queue)
                self.__channels_table[key] = {'channel' : channel, 'worker': worker}  
                self.__worker_list.append(worker)
                self.__channel_list.append(channel)
                for evts in beh:
                    try:
                        evts['action'].set_agent(self)
                        self.__events_table[evts['event']] = {'behavior' : key, 'action': evts['action']}
                    except:
                        raise AgentException('[Fatal, buildAgent]: The action must be instantiated: %s' % str(evts['action']))          
        else:
            raise AgentException('[Fatal, buildAgent]: Agent behaviors must be defined')
        # Check if the agent is persistent
        if self.db:
            # Create MongoDB colletion from ID agent
            self.db[f"agent_{self.id}"].insert_one(self.state)

    @abstractmethod
    def setup(self) -> None:
        """ Method to create and initialize the agent structure
        @exceptions AgentException
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """ Method to free up the resources taken by the agent """
        pass

    def send_event(self, event:dict, data:dict) -> None:
        """
        Method that registers an event to the agent.
        @param event Envent
        @param Data event
        @exceptions AgentException
        """
        if event in self.__events_table:    
            behavior = self.__events_table[event]
            channel = self.__channels_table[behavior['behavior']]
            evt = {'event': event, 'data': data, 'action': behavior['action']}              
            channel['channel'].sendEvent(evt)
        else:
            raise AgentException('[Warn, sendEvent]: The agent has not registered the event %s' % event)
    
    def start(self) -> None:
        """ Start the agent """
        for w in self.__worker_list:
            w.setLet(True)
            w.start()
            
    def wait(self) -> None:
        """ Wait for the agent to finish """
        for w in self.__worker_list:
            w.setLet(False)

    def finalize(self) -> None:
        """ Finalize the agent """
        for w in self.__worker_list:
            w.setAlive(False)
            w.finalize()
    
    def kill(self) -> None:
        """ Remove the agent from the system """
        if self.conf.is_persist:
            self.persist()
        self.shutdown()
        self.id = None
        self.log = None
        self.state = None
        self.__events_table = None
        self.__channels_table = None
        self.finalize()
        self.__worker_list = None
        self.__channel_list = None
        self.__behaviors = None

    def to_dto(self) -> str:
        """ Convert the agent to a DTO """
        dto = {
            'command': 'MOVE',
            'class': self.__class__.__name__,
            'path': self.__module__,
            'id': self.id,
            'state': self.state  
        }
        rtn = str(dto)
        rtn = rtn.replace("'", "\"")  
        return rtn

    def add_behavior(self, behavior:str) -> None:
        """
        Add the new behavior to the agent's behavior.
        @param behavior New behavior
        """
        self.__behaviors[behavior] = []

    def bind_action(self, behavior:str, event:dict, action:Action) -> None:
        """
        Link behavior to event with action.
        @param behavior Behavior
        @param event Event link to behavior
        @param action Action link to event
        @exceptions AgentException
        """
        if behavior in self.__behaviors:
            self.__behaviors[behavior].append({
                'event': event, 
                'action': action
            })
        else:
            raise AgentException('[Fatal, bindAction]: The behavior "%s" is not associated with the agent. Must be added before behavior' % behavior)

    def setup_logger(self, logger_name:str, logger_file:str, level:str) -> None:
        """
        Inicia un componente de seguimiento de la aplicacion.
        @param logger_name nombre del log
        @param logger_file ruta del archivo
        """
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('[PBESA]: %(asctime)s %(name)-12s %(lineno)d %(levelname)-8s %(message)s')
        fileHandler = logging.FileHandler(logger_file, 'w', 'utf-8')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

    def active_logger(self, logger:str, level:int=logging.INFO) -> None:
        """ Active the logger
        @param logger:str Logger name
        @param level:int Logger level
        """
        if not level:
            level = logging.INFO
        self.setUpLogger(logger, '%s.log' % logger, level)
        self.log = logging.getLogger(logger)
    
    def suscribe_logger(self, logger) -> None:
        """ Subscribe to the logger
        @param logger:str Logger name
        """
        self.log = logging.getLogger(logger)

    def persist(self) -> None:
        """ Persist the agent state """
        self.db[self.id].delete_many({})
        self.db[self.id].insert_one(self.state)