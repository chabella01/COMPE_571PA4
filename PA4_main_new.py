import random
import sys
global time_counter

def replacement(alg, counter, PT):
    victim = None
    if alg == 1:   				 #RAND
        victim = random.randint(0, 31)
    elif alg == 2:   			 #FIFO
        victim = counter
    elif alg == 3:  # LRU
        oldest_time = float('inf')
        for i, page in enumerate(PT):
            if page[0] != -1:  # ensure the page is in memory
                if page[3] < oldest_time or (page[3] == oldest_time and page[1] == 0):
                    oldest_time = page[3]
                    victim = i
    elif alg == 4:   			 #PER
        pass
    return victim

def scanMM(MM):
    x = sum(1 for i in MM if i != -1)
    return x

def main():
    file = open(sys.argv[1], "r")
    random.seed(0)
    PT1 = [[-1]*5 for _ in range(128)]   		 #0-translation 1-dirty bit 2-reference bit 3-time 4-freq used
    PT2 = [[-1]*5 for _ in range(128)]
    PT3 = [[-1]*5 for _ in range(128)]
    PT4 = [[-1]*5 for _ in range(128)]
    MM = [-1]*32
    process, addr, location, reference, dirty, value, alg, memLoc = 0, 0, 0, 0, 0, 0, 0, 0
    faults = 0   	 # number of page faults
    disk = 0   	 # number of disk references
    dpw = 0   	 # number of disk page writes
    counter = 0
    RW = ''
    for i in range(128):
        if i < 32:
            MM[i] = -1
        for j in range(5):
            PT1[i][j] = -1
            PT2[i][j] = -1
            PT3[i][j] = -1
            PT4[i][j] = -1
    print("Select page replacement type (1-4):")
    print("1-RAND\n2-FIFO\n3-LRU\n4-PER")
    alg = int(input())
    # rewind(file)
    while True:
        line = file.readline()
        if not line:
            break
        #process, addr, RW = map(int, line.split())
        process, addr, RW = line.split()
        process = int(process)
        addr = int(addr)

        location = (addr >> 9) - 1
        if process == 1:
            if PT1[location][0] == -1:   						 # if location in PT is empty
                faults += 1
                memLoc = scanMM(MM)   						 # try to find empty location in memory
                if memLoc > 31:   							 # if memory is full
                    memLoc = replacement(alg, counter, PT1)   			 # use replacement algorithm to select a victim page
                MM[memLoc] = (location + 1)   						 # make algorithm to store value
                PT1[location][0] = memLoc   			 # translation
                if RW == 'W':
                    PT1[location][1] = 1   			 # dirty bit
                elif RW == 'R':
                    PT1[location][1] = 0
                PT1[location][2] = 1   				 # reference bit
            else:
                value = process * (location + 1)
                memLoc = PT1[location][0]
                if value != MM[memLoc]:
                    memLoc = replacement(alg, counter, PT1)
                    faults += 1
                    disk += 1   								 # number of disk references
                    PT1[location][0] = memLoc   			 # translation
                    if RW == 'W':
                        PT1[location][1] = 1   			 # dirty bit
                        disk += 1
                        dpw += 1   							 # number of dirty page writes
                    elif RW == 'R':
                        PT1[location][1] = 0
        elif process == 2:
            if PT2[location][0] == -1:   				 # if location in PT is empty
                faults += 1
                memLoc = scanMM(MM)   				 # try to find empty location in memory
                if memLoc > 31:   					 # if memory is full
                    memLoc = replacement(alg, counter, PT2)   		 # use replacement algorithm to select a victim page
                MM[memLoc] = process*(location + 1)   						 # make algorithm to store value
                PT2[location][0] = memLoc   			 # translation
                if RW == 'W':
                    PT2[location][1] = 1   			 # dirty bit
                elif RW == 'R':
                    PT2[location][1] = 0
                PT2[location][2] = 1   				 # reference bit
            else:
                value = process * (location + 1)
                memLoc = PT2[location][0]
                if value != MM[memLoc]:
                    memLoc = replacement(alg, counter, PT2)
                    faults += 1
                    disk += 1   								 # number of disk references
                    PT2[location][0] = memLoc   			 # translation
                    if RW == 'W':
                        PT2[location][1] = 1   			 # dirty bit
                        disk += 1
                        dpw += 1   							 # number of dirty page writes
                    elif RW == 'R':
                        PT2[location][1] = 0
        elif process == 3:
            if PT3[location][0] == -1:   				 # if location in PT is empty
                faults += 1
                memLoc = scanMM(MM)   				 # try to find empty location in memory
                if memLoc > 31:   					 # if memory is full
                    memLoc = replacement(alg, counter,  PT3)   		 # use replacement algorithm to select a victim page
                MM[memLoc] = process*(location + 1)   						 # make algorithm to store value
                PT3[location][0] = memLoc   			 # translation
                if RW == 'W':
                    PT3[location][1] = 1   			 # dirty bit
                elif RW == 'R':
                    PT3[location][1] = 0
                PT3[location][2] = 1   				 # reference bit
            else:
                value = process * (location + 1)
                memLoc = PT3[location][0]
                if value != MM[memLoc]:
                    memLoc = replacement(alg, counter, PT3)
                    faults += 1
                    disk += 1   								 # number of disk references
                    PT3[location][0] = memLoc   			 # translation
                    if RW == 'W':
                        PT3[location][1] = 1   			 # dirty bit
                        disk += 1
                        dpw += 1   							 # number of dirty page writes
                    elif RW == 'R':
                        PT3[location][1] = 0
        
        elif process == 4:
            if PT4[location][0] == -1:   				 # if location in PT is empty
                faults += 1
                memLoc = scanMM(MM)   				 # try to find empty location in memory
                if memLoc > 31:   					 # if memory is full
                    memLoc = replacement(alg, counter, PT4)   		 # use replacement algorithm to select a victim page
                MM[memLoc] = process*(location + 1)   						 # make algorithm to store value
                PT4[location][0] = memLoc   			 # translation
                if RW == 'W':
                    PT4[location][1] = 1   			 # dirty bit
                elif RW == 'R':
                    PT4[location][1] = 0
                PT4[location][2] = 1   				 # reference bit
            else:
                value = process * (location + 1)
                memLoc = PT4[location][0]
                if value != MM[memLoc]:
                    memLoc = replacement(alg, counter, PT4)
                    faults += 1
                    disk += 1   								 # number of disk references
                    PT4[location][0] = memLoc   			 # translation
                    if RW == 'W':
                        PT4[location][1] = 1   			 # dirty bit
                        disk += 1
                        dpw += 1   							 # number of dirty page writes
                    elif RW == 'R':
                        PT4[location][1] = 0
        counter += 1
        if counter > 31:
            counter = 0
    print("Number of page faults:", faults)
    print("Number of disk references:", disk)
    print("Number of dirty page writes:", dpw)

if __name__ == "__main__":
    main()


