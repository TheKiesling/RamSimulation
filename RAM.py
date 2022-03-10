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

import simpy as simpPI; #SIMP de PI 
import random as rnd;

#----------------------------VARIABLES-------------------------
RANDOM_SEED = 314 
AMOUNT_CPU = 1
CAPACITY = 100
INTERVAL = 10
PROCESS = 25

#----------------------------CLASSES---------------------------
class memory():
        def __init__(self, env, cpus, ram_capacity):
            self.cpu = simpPI.Resource(env, cpus)
            self.ram = simpPI.Container(env, init = ram_capacity, capacity = ram_capacity)

class process():
    def __init__(self, id, env):
        self.env = env
        self.name = id
        self.memory = rnd.randint(1,10)
        self.instructions = rnd.randint(1,10)
    
    def _getname_(self):
            return self.name

    def __getmemory__(self):
            return self.memory
        
    def _getinstructions_(self):
            return self.instructions      

