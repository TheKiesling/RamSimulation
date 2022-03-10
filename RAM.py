#      #    #######    ########   #######   #          #######   ##      #    #########
#     #        #       #          #         #             #      # #     #    #
#    #         #       #          #         #             #      #  #    #    #
####           #       #####      #######   #             #      #   #   #    #    ####
#    #         #       #                #   #             #      #    #  #    #       #
#     #        #       #                #   #             #      #     # #    #       #
#      #    ########   ########   #######   ########   #######   #      ##    #########

'''
- Scenario:
    Simulation of running programs in a timesharing OS. 

- Actions:
    * NEW: The process reaches the operating system but must wait for RAM to be allocated. 
                If there is memory available you can go to ready state. 
                Otherwise, it remains in queue, waiting for memory.

    * READY: The process is ready to run but must wait for the CPU to attend to it.
                When the CPU is free, it can be used.

    * RUNNING: The CPU attends the process for a limited time, enough to perform only 3 instructions.
                Upon completion of the attention time, the process is removed from the CPU.
                To simplify the simulation, if the number of instructions to be executed is less than 3,
                the processor also dedicates a complete cycle to perform them.

    At the end of the CPU attention, the following may occur:
        a) TERMINATED: If the process no longer has instructions to perform
        b) WAITING: when leaving the CPU a random integer between 1 and 2 is generated. If it is 1 then it goes to the Waiting queue to
        do I/O (input/output) operations. Leaving that queue returns to “ready”.
        c) READY: when leaving the CPU and the randomly generated number is 2, then it goes back to the “ready” queue.
'''

from urllib.request import CacheFTPHandler
import simpy as simpPI; #SIMP de PI 
import random as rnd;

#----------------------------VARIABLES-------------------------
RANDOM_SEED = 314 
AMOUNT_CPU = 1
CAPACITY = 100
INTERVAL = 10
PROCESS = 25
INSTRUCTIONS = 3

#----------------------------CLASSES---------------------------
class RAMMemory():
    def __init__(self, env):
        self.cpu = simpPI.Resource(env, capacity = 1)
        self.ram = simpPI.Container(env, init = 100, capacity = 100)

class Program():
    def __init__(self, id, env, RAM_Memory):
        self.env = env
        self.name = id
        self.action = env.process(self.newProgram(self.name, RAM_Memory))
    
    def newProgram(self, id, RAM_Memory):
        self.memory = rnd.randint(1,10)
        print("-----------------------NEW---------------------------")
        print(f'NEW: Process {id} at {env.now} with memory: {self.memory}')
        print("-----------------------------------------------------")
        print()
        with RAM_Memory.cpu.request() as req:
            yield req
            yield RAM_Memory.ram.get(self.memory)
            self.readyProgram(id)
    
    def readyProgram(self, id):
        self.instructions = rnd.randint(1,10)
        print("-----------------------READY--------------------------")
        print(f'READY: Process {id} at {env.now} with {self.instructions} instructions')
        print("-----------------------------------------------------")
        print()
    
    
    def _getname_(self):
            return self.name

    def __getmemory__(self):
            return self.memory
        
    def _getinstructions_(self):
            return self.instructions      

def newProcess(env, RAM_Memory):
    for i in range(PROCESS):
        Program(i, env, RAM_Memory)
        t = rnd.expovariate(1.0 / INTERVAL)
        yield env.timeout(t)
    

env = simpPI.Environment()
RAM_Memory = RAMMemory(env)
env.process(newProcess(env, RAM_Memory))
env.run(100000)
