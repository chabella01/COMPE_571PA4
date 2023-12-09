#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define PROCESSORS 4
#define ENTRIES 128
#define PAGEBYTES 512
int main()
{
	int process, virtualAddress, vpn, randomIndex;
	int pageFault = 0, referenceBitCounter = 0, dirtyBitCounter = 0;
	int emptyMem = -1;
	int pageTables[PROCESSORS][ENTRIES][2];
	int mainMemory[32];
	char operation;
	FILE *file = fopen("data1.txt", "r");
	srand(0);

	for(int i = 0; i < PROCESSORS; i++){
	        for(int j = 0; j < ENTRIES; j++)
	                pageTables[i][j][0] = -1;
        }

        for(int i = 0; i < 32; i++)
        	mainMemory[i] = 0;
        
	while(1)
	{
		fscanf(file, "%d %d %c", &process, &virtualAddress, &operation);

		if(feof(file) == 1)
			break;

		vpn = virtualAddress >> 9;

		if(operation == 'W')
	                pageTables[process - 1][vpn - 1][1] = 1;
                        

		if(mainMemory[pageTables[process - 1][vpn - 1][0]] != (vpn + PAGEBYTES) * process)
		{
                	pageFault++;
                        referenceBitCounter++;
                        for(int i = 31; i >= 0; i--)
			{
                        	if(mainMemory[i] == 0)
                                                emptyMem = i;                                        
                        }
                        if(emptyMem != -1)
			{
                        	pageTables[process - 1][vpn - 1][0] = emptyMem;
                                mainMemory[emptyMem] = process * (vpn + PAGEBYTES);
                                emptyMem = -1;
                        }
                        else
			{
				randomIndex = (int)(rand() % 32);
                                pageTables[process - 1][vpn - 1][0] = randomIndex;
                                if(mainMemory[randomIndex] <= 640)					// 512 + 128 = size of page entry bytes
				{
                                	if(pageTables[0][mainMemory[randomIndex] - PAGEBYTES - 1][1] == 1)
					{
                                        	referenceBitCounter++;
                                                dirtyBitCounter++;
                                        }
                                }
                                else if(mainMemory[randomIndex] <= 1280)
				{
                                	if(pageTables[1][(mainMemory[randomIndex] / 2) - PAGEBYTES - 1][1] == 1){
                                        	referenceBitCounter++;
                                                dirtyBitCounter++;
                                        }
                                }
                                else if(mainMemory[randomIndex] <= 1920)
				{
                                	if(pageTables[2][(mainMemory[randomIndex] / 3) - PAGEBYTES - 1][1] == 1)
					{
                                        	referenceBitCounter++;
                                                dirtyBitCounter++;
                                        }
                                }
				else
				{
					if(pageTables[3][(mainMemory[randomIndex] / 4) - PAGEBYTES - 1][1] == 1)
					{
						referenceBitCounter++;
						dirtyBitCounter++;
					}
				}
				mainMemory[randomIndex] = process * (vpn + PAGEBYTES);
			}
			if(operation == 'R')
				pageTables[process - 1][vpn - 1][1] = 0;                                
		}	
	}
	printf("Total number of page faults       : %d\n", pageFault);
	printf("Total number of disk accesses     : %d\n", referenceBitCounter);
	printf("Total number of dirty page writes : %d\n", dirtyBitCounter);
	fclose(file);
	return 0;
}
