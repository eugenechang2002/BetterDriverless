import simulation.config as config
import lgsvl
import json
import copy
import time

with open('input.json') as f:
    j = json.load(f)

print(j)

# Generating condition
queue = []
queue.append({})

size = len(queue)
print(len(queue))
for i in range(size):
    cur = queue.pop(0)

    for v in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        temp = copy.deepcopy(cur)

        if "weather" not in temp:
            temp["weather"] = {}
        temp["weather"]["rain"] = v
        queue.append(temp)
        print(temp)

print(len(queue))

size = len(queue)
for i in range(size):
    cur = queue.pop(0)
    print("cur:", cur)
    for v in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        temp = copy.deepcopy(cur)

        if "weather" not in temp:
            temp["weather"] = {}
        temp["weather"]["fog"] = v
        queue.append(temp)
        print(temp)
print(len(queue))

size = len(queue)
for i in range(size):
    cur = queue.pop(0)

    for v in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        temp = copy.deepcopy(cur)

        if "weather" not in temp:
            temp["weather"] = {}
        temp["weather"]["wetness"] = v
        queue.append(temp)
        print(temp)
print(len(queue))

size = len(queue)
for i in range(size):
    cur = queue.pop(0)

    for v in range(24):
        temp = copy.deepcopy(cur)

        if "time" not in temp:
            temp["time"] = {}
        temp["time"]["time_of_day"] = v
        queue.append(temp)

print(len(queue))

# Scenario
cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")

spawns = sim.get_spawn()
state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

startTime = time.time()
while len(queue) > 0:
    before = time.time()
    cur = queue.pop(0)

    sim.weather = lgsvl.WeatherState(cur["weather"]["rain"], cur["weather"]["fog"], cur["weather"]["wetness"])
    print(sim.weather)

    sim.run(1)

    # Time of day can be set from 0 ... 24
    sim.set_time_of_day(cur["time"]["time_of_day"])
    print("Time of Day:", sim.time_of_day)

    sim.run(1)
    print("Time spent:", time.time() - before )

print("Total time spent:", time.time() - startTime )