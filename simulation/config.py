import os
import lgsvl

class Config():

    def __init__(self, simulator="SIMULATOR_HOST", ip="127.0.0.1", port=8181):
        self.simulator = simulator
        self.ip = ip
        self.port = port

    def Simulator(self):
        # Connects to the simulator instance at the ip defined by SIMULATOR_HOST, default is localhost or 127.0.0.1
        sim = lgsvl.Simulator(os.environ.get(self.simulator, self.ip), self.port)
        return sim

# uncomment for testing
# c = Config()
# sim = c.Simulator()
# print("Version =", sim.version)
# print("Current Time =", sim.current_time)
# print("Current Frame =", sim.current_frame)