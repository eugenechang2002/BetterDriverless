import json
import time
import os
import lgsvl
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from parser import getAllPossibleConditions
from output import outputJSON
from lgsvl.agent import NPCControl
import copy

sys.path.insert(1, '/home/wencen/Documents/cmpe295/simulation')
import config as config
import math 

# This function gets called whenever any of the 3 vehicles above collides with anything
def on_collision(agent1, agent2, contact):
  name1 = vehicles[agent1]
  name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
  print("{} collided with {} at {}".format(name1, name2, contact))

dict = {0:{'ego_speed':5, 'npc_speed':110.0},
1:{'ego_speed':6, 'npc_speed':20.0},
2:{'ego_speed':3, 'npc_speed':0.0},
3:{'ego_speed':14, 'npc_speed':0.0},
}

# Get user input
with open('UserInput.json') as f:
    user_json = json.load(f)

queue = []
queue.append({})

scenarios = getAllPossibleConditions(queue, user_json)
size = len(scenarios)
print("scenarios size:", size)

# Load config and simulator
cf = config.Config()
sim = cf.Simulator()

startTime = time.time()
Script_ID = 8
Scenario_ID = 1
while len(scenarios) > 0:
    before = time.time()
    cur = scenarios.pop(0)

    # Load Map
    cf.LoadOrResetScene(sim, "BorregasAve")

    # Weather
    if "Weather" in cur:
        sim.weather = lgsvl.WeatherState(cur["Weather"]["Rain"], cur["Weather"]["Fog"], cur["Weather"]["Wetness"])
    
    # Weather
    if "Time" in cur:
        sim.set_time_of_day(cur["Time"]["TimeOfDay"])
    
    # TrafficLight
    if "TrafficLight" not in cur:
        cf.All_Green_Light(sim)
    else:
        pass

    spawns = sim.get_spawn()
    # ego vehicle
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    forward = lgsvl.utils.transform_to_forward(spawns[0])
    state.transform.position = spawns[0].position + 80.0 * forward
    state.velocity = dict[0]['ego_speed'] * forward
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)


    # suv, 20m ahead, perpendicular to road, stopped
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + 40.0 * forward
    car = sim.add_agent("SUV", lgsvl.AgentType.NPC, state)

    vehicles = {
    ego: "EGO",
    sedan: "Sedan",
    car:"SUV",
    }

    # The above on_collision function needs to be added to the callback list of each vehicle
    ego.on_collision(on_collision)
    bus.on_collision(on_collision)

    #output json file by this function
    outputJSON(size=size, Script_ID=Script_ID, Scenario_ID=Scenario_ID
    , weather=[cur["Weather"]["Rain"], cur["Weather"]["Fog"], cur["Weather"]["Wetness"]], time = cur["Time"]["TimeOfDay"]) 

    sim.run(time_limit=20)
    sim.reset()

    # Log duration and index
    print("scenario: ", Scenario_ID)
    print("Time spent:", time.time() - before)
    Scenario_ID += 1

print("Total time spent:", time.time() - startTime )
print(f"Successfully dump {size} json file for scenaior {Script_ID}")
