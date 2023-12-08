import random

class PageTableEntry:
    def __init__(self):
        self.physical_page_number = None
        self.dirty = False
        self.referenced = False

class ProcessMemory:
    def __init__(self):
        self.page_table = [PageTableEntry() for _ in range(128)]  # 128 entries

# class PhysicalMemory:
#     def __init__(self, size):
#         self.size = size
#         self.pages = {}  # empty to map virtual page to physical page
#         self.queue = []  # For FIFO page replacement
class PhysicalMemory:
    def __init__(self, size):
        self.size = size
        self.pages = {}  # Dictionary to map virtual page to physical page
        self.page_list = []  # List of pages for random selection

    def load_page(self, virtual_page, process_number):
        # Evict a page if memory is full
        if len(self.pages) >= self.size:
            self.evict_page()

        physical_page = len(self.pages)  # Assign next available physical page number
        self.pages[(process_number, virtual_page)] = physical_page
        self.page_list.append((process_number, virtual_page))
        return physical_page

    def evict_page(self):
        # Randomly select a page to evict
        evicted_page = random.choice(self.page_list)
        self.page_list.remove(evicted_page)
        del self.pages[evicted_page]
    
    def is_full(self):
        return len(self.pages) >= self.size

    def get_random_page(self):
        return random.choice(self.page_list)
    
class Statistics:
    def __init__(self):
        self.page_faults = 0
        self.disk_references = 0
        self.dirty_page_writes = 0

def get_virtual_page_number(address):
    return address >> 9

def get_offset(address):
    return address & 0x1FF

def process_memory_references(file_path, physical_memory, stats):
    processes = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            process_number = int(parts[0])
            address = int(parts[1])
            operation = parts[2]

            if process_number not in processes:
                processes[process_number] = ProcessMemory()

            page_number = get_virtual_page_number(address)
            offset = get_offset(address)

            page_table_entry = processes[process_number].page_table[page_number]

            if page_table_entry.physical_page_number is None:
                # Page fault occurs
                stats.page_faults += 1
                stats.disk_references += 1

                # Before loading a new page, check if the page to be evicted is dirty
                if physical_memory.is_full():
                    evicted_process, evicted_page = physical_memory.get_random_page()
                    evicted_page_table_entry = processes[evicted_process].page_table[evicted_page]
                    if evicted_page_table_entry.dirty:
                        stats.dirty_page_writes += 1
                        stats.disk_references += 1
                        evicted_page_table_entry.dirty = False  # Reset dirty bit after writing back

                # Load the new page
                page_table_entry.physical_page_number = physical_memory.load_page(page_number, process_number)

            if operation == 'W':
                page_table_entry.dirty = True

            print(f"Process {process_number}, Address: {address}, Page: {page_number}, Offset: {offset}, Operation: {operation}")


# initialize physical memory and statistics
physical_memory = PhysicalMemory(32)
stats = Statistics()

# Process the memory references
process_memory_references('data1.txt', physical_memory, stats)

# Print statistics
print(f"Total Page Faults: {stats.page_faults}")
print(f"Total Disk References: {stats.disk_references}")
print(f"Total Dirty Page Writes: {stats.dirty_page_writes}")
