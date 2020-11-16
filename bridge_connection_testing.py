import simulation.config as config
import lgsvl
import random
import time

cf = config.Config()
sim = cf.Simulator()
cf.LoadOrResetScene(sim, "BorregasAve")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)

# An EGO will not connect to a bridge unless commanded to
print("Bridge connected:", a.bridge_connected)

# The EGO is now looking for a bridge at the specified IP and port
a.connect_bridge("127.0.0.1", 9090)
# a.connect_bridge("10.31.51.49", 9090)

print("Waiting for connection...")

while not a.bridge_connected:
  time.sleep(1)

print("Bridge connected:", a.bridge_connected)

sensors = a.get_sensors()

# Sensors have an enabled/disabled state that can be set
# By default all sensors are enabled
# Disabling sensor will prevent it to send or receive messages to ROS or Cyber bridges
for s in sensors:
  print(type(s), s.enabled)

# Get a list of controllable objects
controllables = sim.get_controllables("signal")

signal = sim.get_controllable(lgsvl.Vector(19, 5, 21), "signal")
print("\n# Signal of interest:")
print(signal)

# Get current controllable states
print("\n# Current control policy:")
print(signal.control_policy)

# Create a new control policy
control_policy = "trigger=5;green=59;yellow=2;red=1;loop"

# Control this traffic light with a new control policy
signal.control(control_policy)

print("\n# Updated control policy:")
print(signal.control_policy)

sim.run()

print("\n# Updated control policy:")
print(signal.control_policy)

# Get current state of signal
print("\n# Current signal state before simulation:")
print(signal.current_state)