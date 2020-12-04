import os
import lgsvl
import copy
import sys
sys.path.insert(1, '/home/wencen/Documents/cmpe295/simulation')
import config as config
import math 


# I suppose to get a dic or json with input looks like
# ego speed, weather, npc type, npc speed 
dict = {1:{'ego_speed':5, 'weather':0.5,'npc_type':"Sedan",'npc_speed':110.0},
2:{'ego_speed':14, 'weather':0,'npc_type':"SchoolBus",'npc_speed':20.0},
3:{'ego_speed':5, 'weather':1,'npc_type':"SUV",'npc_speed':20.0}}

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")
cf.All_Green_Light(sim)

for i in range(1,4):

    sim.weather = lgsvl.WeatherState(rain=dict[i]['weather'], fog=0, wetness=0)

    spawns = sim.get_spawn()

    sx = spawns[0].position.x
    sz = spawns[0].position.z
    ry = spawns[0].rotation.y

    # ego vehicle

    state = lgsvl.AgentState()
    state.transform = spawns[0]
    forward = lgsvl.utils.transform_to_forward(spawns[0])
    right = lgsvl.utils.transform_to_right(spawns[0])
    state.velocity = dict[i]['ego_speed'] * forward
    ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    # sedan, 10m ahead, driving forward
    state = lgsvl.AgentState()
    state.transform.position = spawns[0].position + 20.0 * forward
    state.transform.rotation = spawns[0].rotation
    npc = sim.add_agent(dict[i]['npc_type'], lgsvl.AgentType.NPC, state)
    # Even though the sedan is commanded to follow the lane, obstacle avoidance takes precedence and it will not drive into the bus
    npc.follow_closest_lane(True, dict[i]['npc_speed']) # 11.1 m/s is ~40 km/h

    vehicles = {
    ego: "EGO",
    npc: dict[i]['npc_type'],
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
    input("next")
    sim.reset()


    #TODO
    # i suppose to call a report function to save all info 