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

import simpy as simpPI #SIMP de PI 
import random as rnd
import statistics as stats

#----------------------------VARIABLES-------------------------
RANDOM_SEED = 314159265358979323 #PI's Seed
AMOUNT_CPU = 1
CAPACITY = 100
INTERVAL = 10
PROCESS = 25
INSTRUCTIONS = 3

#------------------------RAM-MEMORY CLASS----------------------
#--- Container ---
class RAM_Memory():
    def __init__(self, env):
        self.cpu = simpPI.Resource(env, capacity = AMOUNT_CPU) #Number of CPU
        self.ram = simpPI.Container(env, init = CAPACITY, capacity = CAPACITY) #Memory Capacity

time = 0 
times = []

def Process(id, env, RAM_Memory):
    #--- Atributtes ---
    memory = rnd.randint(1,10)
    instructions = rnd.randint(1,10)
    start_time=0.0
    finish_time=0.0
    running = True

                            #--- Actions ---
    #--- NEW ---
    print("-----------------------NEW---------------------------")
    print(f'NEW: Process {id} at {env.now} with memory: {memory}')
    print("-----------------------------------------------------")
    print()
    start_time = env.now
    while running:

        #--- Ready ---
        with RAM_Memory.cpu.request() as req:
            yield req
            yield env.timeout(1)
            yield RAM_Memory.ram.get(memory)
            print("-----------------------READY-------------------------")
            print(f'READY: Process {id} at {env.now} with {instructions} instructions')
            print("-----------------------------------------------------")
            print()

        #--- Running ---
        with RAM_Memory.cpu.request() as req:
            yield req
            yield env.timeout(1)
            instructions -= INSTRUCTIONS
            print("----------------------RUNNING------------------------")
            print(f'RUNNING: Process {id} at {env.now} decreasing {INSTRUCTIONS} instructions')
            print("-----------------------------------------------------")
            print()

        #Finalize the attention of the CPU
        if (instructions > 0):
            next_state = rnd.randint(1,2)
            if (next_state == 1):

                #--- Waiting ---
                with RAM_Memory.cpu.request() as req:
                    yield req
                    yield env.timeout(1)
                    yield RAM_Memory.ram.put(memory)
                    print("----------------------WAITING------------------------")
                    print(f'WAITING: Process {id} at {env.now}')
                    print("-----------------------------------------------------")
                    print()

            else:

                #--- Ready ---
                yield RAM_Memory.ram.put(memory)

        else:
            #--- Terminated ---
            with RAM_Memory.cpu.request() as req:
                yield req
                yield env.timeout(1)
                yield RAM_Memory.ram.put(memory)
                running = False
                print("--------------------TERMINATED-----------------------")
                print(f'TERMINATED: Process {id} ends at {env.now} asigment: {memory}')
                print("-----------------------------------------------------")
                print()
                finish_time=env.now #End of the process

                #--- Stats ---
                global time
                global times
                time += finish_time-start_time
                times.append(finish_time-start_time)
    

def newProcess(env, RAM_Memory):
    for i in range(PROCESS):
        env.process(Process(i, env, RAM_Memory))
        delay = rnd.expovariate(1.0 / INTERVAL)
        yield env.timeout(delay)
    
rnd.seed(RANDOM_SEED)
env = simpPI.Environment()
RAM_Memory = RAM_Memory(env)
env.process(newProcess(env, RAM_Memory))
env.run()

#--- Stats ---
average = time/PROCESS
desvest = stats.stdev(times)

print(f"Average: {average}")
print(f"Desvest: {desvest} ")
