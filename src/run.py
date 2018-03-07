from agent import Agent
from environment import Environment


'''
1. Set up connection with neuropype (tcp)
2. start stimulation.
3. detect goal

4. feed goal to environment

'''

env = Environment()
agent1 = Agent()

def setup_run():
    env.goal = goal
    agent1.set_position(env)
    env.register_agent(agent1)

setup_run()

env.register_agent(agent1)
agent1.path = agent1.shortest_path(env.graph, agent1.pos, env.goal)
