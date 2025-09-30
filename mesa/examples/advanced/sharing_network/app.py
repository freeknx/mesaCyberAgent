import matplotlib.pyplot as plt
import networkx as nx
import solara
from matplotlib.figure import Figure
import sys
sys.path.insert(0, 'C:\\Users\\Jabari\\Documents\\Git\\mesaCyberAgent')

from mesa.examples.advanced.sharing_network.model import DefenderNetworkModel
from mesa.visualization import SolaraViz
from mesa.visualization.utils import update_counter
import random

# TODO: update model params
model_params = {
    "num_groups": {
        "type": "SliderInt",
        "value": 7,
        "label": "Number of groups",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "num_members": {
        "type": "SliderInt",
        "value": 6,
        "label": "Number of members per group",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "prob_add_friend": {
        "type": "SliderFloat",
        "label": "probability to add friend",
        "value": 0.5,
        "min": 0.0,
        "max": 1.0,
        "step": 0.1,
    },
    "punish": {
        "type": "SliderFloat",
        "label": "probability to punish",
        "value": 0.0,
        "min": 0.0,
        "max": 1.0,
        "step": 0.1,
    },
    "alphaM": {
        "type": "SliderInt",
        "value": 45,
        "label": "alphaM",
        "min": 1,
        "max": 75,
        "step": 1,
    },
    "betaM": {
        "type": "SliderInt",
        "value": 45,
        "label": "betaM",
        "min": 1,
        "max": 75,
        "step": 1,
    },
    "punish_cost": {
        "type": "SliderInt",
        "value": 50,
        "label": "Amount punished for",
        "min": 1,
        "max": 500,
        "step": 10,
    },
    "penalty": {
        "type": "SliderInt",
        "value": 100,
        "label": "penalty amount",
        "min": 1,
        "max": 500,
        "step": 10,
    },
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
}

# Create visualization elements. The visualization elements are solara components
# that receive the model instance as a "prop" and display it in a certain way.
# Under the hood these are just classes that receive the model instance.
# You can also author your own visualization elements, which can also be functions
# that receive the model instance and return a valid solara component.

# Create initial model instance
model = DefenderNetworkModel(7, 6, 0.5, 0, 45, 45, 50, 100, 42)
g = model.network
list(g.nodes)
@solara.component
def plot_network(model):
    update_counter.get()
    g = model.network
    pos = nx.kamada_kawai_layout(g, dist=None, pos=None, weight='weight', scale=1, center=None, dim=2)
    fig = Figure()
    ax = fig.subplots()
    labels = {agent.unique_id: agent.unique_id for agent in model.agents}
    #TODO find issue in agent model
    
    colors = []
    sizes  = []

    # We append a random color/size in the beginning to account for the root node
    colors.append(random.uniform(1, 100))
    sizes.append(random.uniform(1, 10))

    colors.extend([agent.altruism for agent in model.agents])
    sizes.extend([agent.wealth/20 for agent in model.agents])
    for node in g.nodes:
        print(node)
        print(g.nodes[node])
        print("\n")
    # print(list(g.nodes))
    # print(g.nodes[42])
    # g.nodes[42]["block"] = 6 
    
    # for agent in model.agents:
    #     print(agent.unique_id)

    nx.draw(
        g,
        pos,
        node_size=sizes,
        node_color=colors,
        cmap=plt.cm.coolwarm,
        labels=labels,
        ax=ax,
    )
    g.remove_node(42)
    for node in g.nodes:
        print(node)
        print(g.nodes[node])
        print("\n")

    solara.FigureMatplotlib(fig)




# Create the SolaraViz page. This will automatically create a server and display the
# visualization elements in a web browser.
# Display it using the following command in the example directory:
# solara run app.py
# It will automatically update and display any changes made to this file
page = SolaraViz(
    model,
    components=[plot_network],
    model_params=model_params,
    name="Sharing Network Model",
)
page  # noqa
