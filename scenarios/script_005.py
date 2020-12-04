
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

    # This will create waypoints in a circle for the pedestrian to follow
    radius = 5
    count = 8
    wp = []
    for i in range(count):
        x = radius * math.cos(i * 2 * math.pi / count)
        z = radius * math.sin(i * 2 * math.pi / count)
        # idle is how much time the pedestrian will wait once it reaches the waypoint
        idle = 1 if i < count//2 else 0
        wp.append(lgsvl.WalkWaypoint(spawns[1].position + (8 + x) * right + z * forward, idle))

    state = lgsvl.AgentState()
    state.transform = spawns[1]
    state.transform.position = wp[0].position

    p = sim.add_agent("Pamela", lgsvl.AgentType.PEDESTRIAN, state)

    # This sends the list of waypoints to the pedestrian. The bool controls whether or not the pedestrian will continue walking (default false)
    p.follow(wp, True)
    
    # Even though the sedan is commanded to follow the lane, obstacle avoidance takes precedence and it will not drive into the bus
   
    vehicles = {
    ego: "EGO",
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

