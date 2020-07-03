import os
import lgsvl

class config():

    def __init__(self, simulator="SIMULATOR_HOST", ip="127.0.0.1", port=8181):
        self.simulator = simulator
        self.ip = ip
        self.port = port

    def Simulator(self):
        lgsvl.Simulator(os.environ.get(self.simulator, self.ip), self.port)
    
    