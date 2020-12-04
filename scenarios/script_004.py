
import json
import time
import os
import lgsvl
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from parser import getAllPossibleConditions
from lgsvl.agent import NPCControl
import copy

sys.path.insert(1, '/home/wencen/Documents/cmpe295/simulation')
import config as config
import math 
#from .. import getAllPossibleConditions

dict = {0:{'ego_speed':5, 'npc_speed':110.0},
1:{'ego_speed':14, 'npc_speed':20.0},
2:{'ego_speed':3, 'npc_speed':0.0},
3:{'ego_speed':14, 'npc_speed':0.0},
}

# Get user input
with open('UserInput.json') as f:
    user_json = json.load(f)

queue = []
queue.append({})

scenarios = getAllPossibleConditions(queue, user_json)
print("scenarios size:", len(scenarios))

# Load config and simulator
cf = config.Config()
sim = cf.Simulator()

startTime = time.time()
index = 1


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
        # TODO

    # Log duration and index
    print("scenario: ", index)
    print("Time spent:", time.time() - before)
    index += 1

    spawns = sim.get_spawn()

    sx = spawns[0].position.x
    sz = spawns[0].position.z
    ry = spawns[0].rotation.y

    # ego vehicle

    state = lgsvl.AgentState()
    state.transform = spawns[0]
    forward = lgsvl.utils.transform_to_forward(spawns[0])
    right = lgsvl.utils.transform_to_right(spawns[0])
    state.velocity = dict[index%3]['ego_speed'] * forward
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    # sedan, right, turing right follow the lane
    state = lgsvl.AgentState()
    state.transform.position = spawns[0].position + 5.0 * right
    state.transform.rotation = spawns[0].rotation
    sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)
    print ("npc is ", index%3)
    sedan.follow_closest_lane(True, dict[index%3]['npc_speed']) # 11.1 m/s is ~40 km/h

    #suv coming to the car
    state = lgsvl.AgentState()
    state.transform = copy.deepcopy(spawns[0])
    state.transform.position = spawns[0].position + (20.0 * forward)
    #state.transform.position = spawns[0].position + (-5.0 * right)
    #state.transform.rotation = spawns[0].rotation * 360
    suv = sim.add_agent("SUV", lgsvl.AgentType.NPC, state)
    suv.follow_closest_lane(True, dict[(index+1)%3]['npc_speed']) # 11.1 m/s is ~40 km/h
    
    # Even though the sedan is commanded to follow the lane, obstacle avoidance takes precedence and it will not drive into the bus
   
    vehicles = {
    ego: "EGO",
    sedan: "Sedan",
    suv:"SUV",
    }


 # This function gets called whenever any of the 3 vehicles above collides with anything
    def on_collision(agent1, agent2, contact):
        name1 = vehicles[agent1]
        name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
        print("{} collided with {} at {}".format(name1, name2, contact))

    # The above on_collision function needs to be added to the callback list of each vehicle
    ego.on_collision(on_collision)
    #npc.on_collision(on_collision)

    sim.run(time_limit=7)
    sim.reset()

print("Total time spent:", time.time() - startTime )

