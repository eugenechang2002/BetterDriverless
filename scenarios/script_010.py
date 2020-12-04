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
1:{'pedestrian_speed':6, 'npc_speed':20.0},
2:{'ego_speed':3, 'npc_speed':0.0},
3:{'ego_speed':14, 'npc_speed':0.0},
}

#variables
ego_position = [150, 30]  #the forward, right position for parking spot
pedestrian_spot = [140, 5]  #the forward, right position for npcSpot spot
pedestrian_speed = 1    #npcSpeed in terms of forward
ego_speed = 3

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
Script_ID = 10
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

    forward = lgsvl.utils.transform_to_forward(spawns[0])
    spawns = sim.get_spawn()
    #npc ##add pedestrian
    state = copy.deepcopy(lgsvl.AgentState())
    state.transform = copy.deepcopy(spawns[0])
    state.velocity = pedestrian_speed * forward

    # Give waypoints for the spawn location and walk 10m ahead
    start = spawns[0].position + pedestrian_spot[0]*forward + pedestrian_spot[1]*right
    end =  start + 10 * forward
    wp = [ lgsvl.WalkWaypoint(start, 0),
           lgsvl.WalkWaypoint(end, 0),
         ]

    state.transform.position = start
    state.transform.rotation = spawns[0].rotation
    pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, state)
    pedestrian.follow(wp, True)

    #ego
    state = copy.deepcopy(lgsvl.AgentState())
    state.velocity = ego_speed * right *  -1
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + ego_position[0]*forward + ego_position[1]*right
    state.transform.rotation.y = spawns[0].rotation.y + 270.0
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    vehicles = {
      ego: "EGO",
      pedestrian: "Bob",
    }

    # The above on_collision function needs to be added to the callback list of each vehicle
    ego.on_collision(on_collision)
    pedestrian.on_collision(on_collision)

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
