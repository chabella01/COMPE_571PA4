#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int replacement(int alg, int counter, int PT[][5]){
    int victim;
    
    if(alg == 1) {   				 //RAND
   	 victim = rand() % 32;
    }
    
    else if(alg == 2){   			 //FIFO
   	 victim = counter;
    }
    
    else if(alg == 3){   			 //LRU
    
    }
    
    else if(alg == 4){   			 //PER
    
    }
    
    return victim;
}

int scanMM(int MM[]){
    int i = 0;
    int x = 0;
    
    for(i = 0; i < 32; i++){
		if(MM[i] != -1){
			x += 1;
		}
    }
    
    return x;
}

int main(int argc, char *argv[]){
    FILE *file = fopen(argv[1], "r");
    srand(0);
    int PT1[128][5];   		 //0-translation 1-dirty bit 2-reference bit 3-time 4-freq used
    int PT2[128][5];
    int PT3[128][5];
    int PT4[128][5];
    int MM[32];
    int process, addr, location, reference, dirty, value, alg, memLoc;
    int faults = 0;   	 //# of page faults
    int disk = 0;   	 //# of disk references
    int dpw = 0;   	 //# of disk page writes
    int counter = 0;
    char RW;
    
    for(int i = 0; i < 128; i++){
   	 if(i < 32){
   		 MM[i] = -1;
   	 }
   	 for(int j = 0; j < 5; j++){
   		 PT1[i][j] = -1;
   		 PT2[i][j] = -1;
   		 PT3[i][j] = -1;
   		 PT4[i][j] = -1;
   	 }
    }
    
    printf("Select page replacement type (1-4):\n");
    printf("1-RAND\n2-FIFO\n3-LRU\n4-PER\n");
    scanf("%d", &alg);
    
    //rewind(file);
    
    while(!feof(file)){
   	 fscanf(file, "%d %d %c", &process, &addr, &RW);
   	 location = (addr >> 9) - 1;
   	 //printf("%d\t%d %c\n", process, addr, RW);   	 //just a test
   	 if(process == 1){
   		 if(PT1[location][0] == -1){   						 //if location in PT is empty
   			 faults++;
   			 memLoc = scanMM(MM);   						 //try to find empty location in memory
   			 if(memLoc > 31){   							 //if memory is full
   				 memLoc = replacement(alg, counter, PT1);   			 //use replacement algorithm to select a victim page
   			 }
   			 MM[memLoc] = (location + 1);   						 //make algorithm to store value
   			 PT1[location][0] = memLoc;   			 //translation
   			 if(RW == 'W'){
   				 PT1[location][1] = 1;   			 //dirty bit
   			 }
   			 else if(RW == 'R'){
   				 PT1[location][1] = 0;
   			 }
   			 PT1[location][2] = 1;   				 //reference bit
   			 
   		 }
   		 else{
   			 value = process * (location + 1);
   			 memLoc = PT1[location][0];
   			 if(value != MM[memLoc]){
   				 memLoc = replacement(alg, counter, PT1);
   				 faults++;
   				 disk++;   								 //# of disk references
   				 PT1[location][0] = memLoc;   			 //translation
   				 if(RW == 'W'){
   					 PT1[location][1] = 1;   			 //dirty bit
   					 disk++;
   					 dpw++;   							 //# of dirty page writes
   				 }
   				 else if(RW == 'R'){
   					 PT1[location][1] = 0;
   				 }
   			 }
   		 }   								 
   	 }
   	 
   	 else if(process == 2){
   		 if(PT2[location][0] == -1){   				 //if location in PT is empty
   			 faults++;
   			 memLoc = scanMM(MM);   				 //try to find empty location in memory
   			 if(memLoc > 31){   					 //if memory is full
   				 memLoc = replacement(alg, counter, PT2);   		 //use replacement algorithm to select a victim page
   			 }
   			 MM[memLoc] = process*(location + 1);   						 //make algorithm to store value
   			 PT2[location][0] = memLoc;   			 //translation
   			 if(RW == 'W'){
   				 PT2[location][1] = 1;   			 //dirty bit
   			 }
   			 else if(RW == 'R'){
   				 PT2[location][1] = 0;
   			 }
   			 PT2[location][2] = 1;   				 //reference bit
   			 
   		 }
   		 else{
   			 value = process * (location + 1);
   			 memLoc = PT2[location][0];
   			 if(value != MM[memLoc]){
   				 memLoc = replacement(alg, counter, PT2);
   				 faults++;
   				 disk++;   								 //# of disk references
   				 PT2[location][0] = memLoc;   			 //translation
   				 if(RW == 'W'){
   					 PT2[location][1] = 1;   			 //dirty bit
   					 disk++;
   					 dpw++;   							 //# of dirty page writes
   				 }
   				 else if(RW == 'R'){
   					 PT2[location][1] = 0;
   				 }
   			 }
   		 }
   	 }
   	 
   	 else if(process == 3){
   		 if(PT3[location][0] == -1){   				 //if location in PT is empty
   			 faults++;
   			 memLoc = scanMM(MM);   				 //try to find empty location in memory
   			 if(memLoc > 31){   					 //if memory is full
   				 memLoc = replacement(alg, counter,  PT3);   		 //use replacement algorithm to select a victim page
   			 }
   			 MM[memLoc] = process*(location + 1);   						 //make algorithm to store value
   			 PT3[location][0] = memLoc;   			 //translation
   			 if(RW == 'W'){
   				 PT3[location][1] = 1;   			 //dirty bit
   			 }
   			 else if(RW == 'R'){
   				 PT3[location][1] = 0;
   			 }
   			 PT3[location][2] = 1;   				 //reference bit
   			 
   		 }
   		 else{
   			 value = process * (location + 1);
   			 memLoc = PT3[location][0];
   			 if(value != MM[memLoc]){
   				 memLoc = replacement(alg, counter, PT3);
   				 faults++;
   				 disk++;   								 //# of disk references
   				 PT3[location][0] = memLoc;   			 //translation
   				 if(RW == 'W'){
   					 PT3[location][1] = 1;   			 //dirty bit
   					 disk++;
   					 dpw++;   							 //# of dirty page writes
   				 }
   				 else if(RW == 'R'){
   					 PT3[location][1] = 0;
   				 }
   			 }
   		 }
   	 }
   	 
   	 else if(process == 4){
   		 if(PT4[location][0] == -1){   				 //if location in PT is empty
   			 faults++;
   			 memLoc = scanMM(MM);   				 //try to find empty location in memory
   			 if(memLoc > 31){   					 //if memory is full
   				 memLoc = replacement(alg, counter, PT4);   		 //use replacement algorithm to select a victim page
   			 }
   			 MM[memLoc] = process*(location + 1);   						 //make algorithm to store value
   			 PT4[location][0] = memLoc;   			 //translation
   			 if(RW == 'W'){
   				 PT4[location][1] = 1;   			 //dirty bit
   			 }
   			 else if(RW == 'R'){
   				 PT4[location][1] = 0;
   			 }
   			 PT4[location][2] = 1;   				 //reference bit
   			 
   		 }
   		 else{
   			 value = process * (location + 1);
   			 memLoc = PT4[location][0];
   			 if(value != MM[memLoc]){
   				 memLoc = replacement(alg, counter, PT4);
   				 faults++;
   				 disk++;   								 //# of disk references
   				 PT4[location][0] = memLoc;   			 //translation
   				 if(RW == 'W'){
   					 PT4[location][1] = 1;   			 //dirty bit
   					 disk++;
   					 dpw++;   							 //# of dirty page writes
   				 }
   				 else if(RW == 'R'){
   					 PT4[location][1] = 0;
   				 }
   			 }
   		 }
   	 }
   	 counter++;
   	 if(counter > 31){
   		 counter = 0;
   	 }
    }
    
    printf("Number of page faults: %d\nNumber of disk references: %d\nNumber of dirty page writes: %d\n", faults, disk, dpw);

    return 0;
}
