# RamSimulation

A simulation of CPU using SimPy
****************************************************************************************
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
