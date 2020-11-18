import simulation.config as config
import lgsvl
import copy
import json
import time
from parser import getAllPossibleConditions
from lgsvl.agent import NPCControl

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
    
    sim.run(1)

    # Log duration and index
    print("scenario: ", index)
    print("Time spent:", time.time() - before)
    index += 1

    # TODO: add more conditions
    #spawns = sim.get_spawn()
    #forward = lgsvl.utils.transform_to_forward(spawns[0])

    # ego vehicle

    #state = lgsvl.AgentState()
    #state.transform = spawns[0]

print("Total time spent:", time.time() - startTime )





    # state.transform.position = spawns[0].position + 60.0 * forward
    #ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

    #dreamview_connection = lgsvl.dreamview.Connection(simulator=sim, ego_agent=ego)
    # print(dreamview_connection.get_module_status())



    #target_state = copy.deepcopy(state)
    #target_state.transform.position += 50.0 * forward

    #sx = target_state.transform.position.x
    #sz = target_state.transform.position.z

    #sim.run(10)

    #modules = ['Camera', 'Canbus', 'Control', 'GPS', 'Guardian', 'Localization', 'Perception', 'Planning', 'Prediction', 'Radar', 'Recorder', 'Routing', 'Storytelling', 'Third Party Perception', 'Traffic Light', 'Transform', 'Velodyne']
    # dreamview_connection.enable_apollo(sx, sz, modules)


    # cf.All_Green_Light(sim)

    # controllables = sim.get_controllables("signal")
    # for c in controllables:
    #     print(c.control_policy)

    # sim.run(10)