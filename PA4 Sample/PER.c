int unref0 = -1;
int unref1 = -1;
int ref0 = -1;
int ref1 = -1;
int location, PTE, p;									//location is index for main memory, PTE is index for the page table

if{
	//loop through memory to find empty slot
}
else{
	for(i = 31; i >= 0; i++){
		//process number * (VPN+512)
		//PT1 limits 512-640, PT2 (641-1280), PT3 1281-1920
		if((mainMemory[i] >= 512) && (mainMemory[i] <= 640)){
			p = 1;
		}
		if((mainMemory[i] >= 641) && (mainMemory[i] <= 1280)){
			p = 2;
		}
		if((mainMemory[i] >= 1281) && (mainMemory[i] <= 1920)){
			p = 3;
		}
		if((mainMemory[i] >= 1921)){
			p = 4;
		}
		
		if(p == process){
			PTE = (mem[i] / p) - 512;
			d_bit = pageTables[process][PTE][1];			//dirty bit
			r_bit = pageTables[process][PTE][2];			//reference bit
			
			if((r_bit == 0) && (d_bit == 0)){
				unref0 = i;
			}
			
			else if((r_bit == 0) && (d_bit == 1)){
				unref1 = i;
			}
			
			else if((r_bit == 1) && (d_bit == 0)){
				ref0 = i;
			}
			
			else if((r_bit == 1) && (d_bit == 1)){
				ref1 = i;
			}
		}
	}

	if(unref0 == -1){
		if(unref1 == -1){
			if(ref0 == -1){
				location = ref1;
			}
			else{
				location = ref0;
			}
		}
		else{
			location = unref1;
		}
	}
	else{
		location = unref0;
	}
}
