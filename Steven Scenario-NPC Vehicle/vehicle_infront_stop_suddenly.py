#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import math
import copy

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
if sim.current_scene == "BorregasAve":
  sim.reset()
else:
  sim.load("BorregasAve")

spawns = sim.get_spawn()
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])
# EGO

state = lgsvl.AgentState()
state.velocity = 6 * forward
state.transform = spawns[0]
state2 = copy.deepcopy(state)
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state2)

# NPC, 10 meters ahead
sx = spawns[0].position.x
sy = spawns[0].position.y
sz = spawns[0].position.z + 10.0

state = lgsvl.AgentState()
state.transform.position = spawns[0].position + 10 * forward
state.transform.rotation = spawns[0].rotation
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

vehicles = {
  a: "EGO",
  npc: "Sedan",
}

def on_collision(agent1, agent2, contact):
  name1 = vehicles[agent1]
  name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
  print("{} collided with {}".format(name1, name2))

a.on_collision(on_collision)
npc.on_collision(on_collision)

waypoints = []
z_delta = 30

layer_mask = 0
layer_mask |= 1 << 0 # 0 is the layer for the road (default)

npc_speed = 12
# Waypoint angles are input as Euler angles (roll, pitch, yaw)
angle = spawns[0].rotation
hit = sim.raycast(spawns[0].position + 2*z_delta * forward, lgsvl.Vector(0,-1,0), layer_mask) 

# NPC will wait for 1 second at each waypoint
wp = lgsvl.DriveWaypoint(hit.point, npc_speed, angle, 1)
waypoints.append(wp)

# When the NPC is within 0.5m of the waypoint, this will be called
def on_waypoint(agent, index):
  print("waypoint {} reached".format(index))
  print("npc vehicle stop")

# The above function needs to be added to the list of callbacks for the NPC
npc.on_waypoint_reached(on_waypoint)
npc.follow(waypoints)

input("Press Enter to run")

sim.run()