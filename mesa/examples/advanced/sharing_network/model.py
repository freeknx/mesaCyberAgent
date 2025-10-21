import matplotlib.pyplot as plt
import math
import random
import decimal
import networkx as nx
import numpy as np
from itertools import combinations

import mesa
from mesa import Model
from mesa.examples.advanced.sharing_network.agents import Defender
#from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
#from itertools import combination
from mesa.space import NetworkGrid

#probability of attack, impact, cost to attacker, and index number, respectively, for 4 attack types
#1:malware, 2:web-based, 3:DOS, 4:malicious insider
attacks = [[0.25, 2600, 50, 0],[0.20, 2300, 60, 1], [0.20, 1700, 70, 2], [0.15, 1600, 65, 3]] 
att_combos = list()
for n in range(len(attacks) + 1):
    att_combos += list(combinations(attacks, n))
att_combos.remove(())

#prob of mitigating attack 1-4, investment, and annual cost, respectively, for 6 counter measure types
#1:security sharing, 2:access management, 3:cyber behavior analytics, 4:cryptography, 5:policy management, 6:enterprise governance
countermeasure = [[0.6, 0.5, 0.4, 0.5,   100, 25],[0.4, 0.6, 0.4, 0.6, 80, 30],[0.5, 0.5, 0.4, 0.6, 110, 30],[0.4, 0.5, 0.3, 0.4, 100, 5],[0.5, 0.4, 0.3, 0.5, 80, 45],[0.5, 0.5, 0.4, 0.5, 300, 50]]
cm_combos = list()
for n in range(len(countermeasure) + 1):
    cm_combos += list(combinations(countermeasure, n))
cm_combos.remove(())
#cm_combos[combo set][countermeasure][value]

class DefenderNetworkModel(mesa.Model):
    """A model with some number of agents."""
    """add description of network, change class names"""

    def __init__(self, num_groups=7, num_members=6, prob_add_friend=0.5, punish = 0, alphaM=45, betaM=45, punish_cost=50, penalty=100, seed=42):

        super().__init__(seed=seed)
        self.num_agents = num_groups*num_members
        self.num_nodes = self.num_agents
        self.network = nx.planted_partition_graph(num_groups, num_members, 0.5, 0.1, seed=seed)
        self.grid = NetworkGrid(self.network)
        self.rosi = 0
        self.datacollector = DataCollector(
            model_reporters={"prob_of_contr": self.prob_of_contr, "gain": self.gain, "wealth": self.wealth, "freeriders":self.freeriders, "friends":self.friends, "altruism":self.altruism, "contribution_value":self.contribution_value, "cmlist":self.cmlist, "attlist":self.attlist, "alpha": self.alpha, "beta": self.beta},
            agent_reporters={"Contribution %": lambda _: _.prob_of_contr, "Altruism": lambda _: _.gain}
        )

        Defender.create_agents(self, self.num_agents, prob_add_friend, punish, alphaM, betaM, punish_cost, penalty)

        ##list_of_random_nodes = self.random.sample(self.G.nodes(), self.num_agents)
        agent_ids = [
            agent.unique_id for agent in self.agents
        ]
        self.network.add_nodes_from(agent_ids)
        #Add values to the empty node at the end of the agent list
        self.network.nodes[self.num_agents]['block'] = 6
        self.network.nodes[self.num_agents]['agent'] = []

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        for agent in self.agents:
            agent.step()
        # collect data
        self.datacollector.collect(self)
        
    def datacollect(self):
        return self.datacollector.get_model_vars_dataframe()
        
    def prob_of_contr(self):
        y = [agent.prob_of_contr for agent in self.agents]
        #x = [agent.prob_of_contr <= 0 for agent in self.agents]
        return y
    
    def wealth(self): 
        y = [agent.wealth for agent in self.agents]
        #x = [agent.prob_of_contr <= 0 for agent in self.agents]
        return y
    
    def gain(self):
        y = [agent.gain for agent in self.agents]
        #x = [agent.prob_of_contr <= 0 for agent in self.agents]
        return y
    
    def freeriders(self):
        y = [agent.k for agent in self.agents]
        #x = [agent.prob_of_contr <= 0 for agent in self.agents]
        return y
    
    def friends(self):
        y = [len(agent.friends) for agent in self.agents]
        #x = [agent.prob_of_contr <= 0 for agent in self.agents]
        return y
    
    def altruism(self):
        y = [agent.altruism for agent in self.agents]
        #x = [agent.prob_of_contr <= 0 for agent in self.agents]
        return y
    
    def contribution_value(self):
        y = [agent.cmValue  + agent.attValue for agent in self.agents]
        return y
    
    def cmlist(self):
        y = [agent.cmlist for agent in self.agents]
        return y
    
    def attlist(self):
        y = [agent.attlist for agent in self.agents]
        return y
    
    def alpha(self):
        y = [agent.alpha for agent in self.agents]
        return y
    
    def beta(self):
        y = [agent.beta for agent in self.agents]
        return y

    def run_model(self, n):
        for i in range(n):
            self.step()
