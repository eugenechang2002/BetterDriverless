import simulation.config as config
import lgsvl
from lgsvl.agent import NPCControl

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")

spawns = sim.get_spawn()

# ego vehicle

state = lgsvl.AgentState()
state.transform = spawns[0]

forward = lgsvl.utils.transform_to_forward(spawns[0])

state.transform.position = spawns[0].position + 60.0 * forward
ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

sim.run(3)

cf.All_Green_Light(sim)

controllables = sim.get_controllables("signal")
for c in controllables:
    print(c.control_policy)

sim.run(10)