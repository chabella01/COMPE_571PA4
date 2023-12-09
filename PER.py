class PageTableEntry:
    def __init__(self):
        self.physical_page_number = None
        self.dirty = False
        self.referenced = False
        self.accessed_time = None  # Track last access time

class ProcessMemory:
    def __init__(self):
        self.page_table = [PageTableEntry() for _ in range(128)]  # 128 entries

class PhysicalMemory:
    def __init__(self, size):
        self.size = size
        self.frames = [None] * size  # Use an array to represent physical memory frames
        self.queue = []  # For FIFO page replacement

    def load_page(self, virtual_page, process_number):
        if len(self.queue) >= self.size:
            self.evict_page()
        physical_page = len(self.queue)
        self.frames[physical_page] = (process_number, virtual_page)
        self.queue.append((process_number, virtual_page))
        return physical_page

    def evict_page(self):
        evicted_process, evicted_page = self.queue.pop(0)
        for i, (proc, page) in enumerate(self.frames):
            if proc == evicted_process and page == evicted_page:
                self.frames[i] = None

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
    try:
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
                    stats.page_faults += 1
                    stats.disk_references += 1
                    page_table_entry.physical_page_number = physical_memory.load_page(page_number, process_number)
                if operation == 'W':
                    page_table_entry.dirty = True
                print(f"Process {process_number}, Address: {address}, Page: {page_number}, Offset: {offset}, Operation: {operation}")
    except IOError:
        print("Error reading file")

# Initialize physical memory and statistics
physical_memory = PhysicalMemory(32)
stats = Statistics()
processes = {}  # Dictionary to track process memory

# Process the memory references
process_memory_references('data1.txt', physical_memory, stats)

# Print statistics
print(f"Total Page Faults: {stats.page_faults}")
print(f"Total Disk References: {stats.disk_references}")
print(f"Total Dirty Page Writes: {stats.dirty_page_writes}")
