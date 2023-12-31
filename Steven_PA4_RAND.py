import random

class PageTableEntry:
    def __init__(self):
        self.physical_page_number = None
        self.dirty = False
        self.referenced = False
        self.accessed_time = None

class ProcessMemory:
    def __init__(self):
        self.page_table = [PageTableEntry() for _ in range(128)]

class PhysicalMemory:
    def __init__(self, size):
        self.size = size
        self.pages = {}
        self.page_list = []

    def load_page(self, virtual_page, process_number):
        if len(self.pages) >= self.size:
            self.evict_page()
        physical_page = len(self.pages)
        self.pages[(process_number, virtual_page)] = physical_page
        self.page_list.append((process_number, virtual_page))
        return physical_page

    def evict_page(self):
        evicted_page = random.choice(self.page_list)
        evicted_entry = processes[evicted_page[0]].page_table[evicted_page[1]]
        if evicted_entry.dirty:
            stats.dirty_page_writes += 1
        self.page_list.remove(evicted_page)
        del self.pages[evicted_page]

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
                page_table_entry = processes[process_number].page_table[page_number]
                if page_table_entry.physical_page_number is None:
                    stats.page_faults += 1
                    stats.disk_references += 1
                    page_table_entry.physical_page_number = physical_memory.load_page(page_number, process_number)
                if operation == 'W':
                    page_table_entry.dirty = True
                print(f"Process {process_number}, Address: {address}, Page: {page_number}, Operation: {operation}")
    except IOError:
        print("Error reading file")

physical_memory = PhysicalMemory(32)
stats = Statistics()
process_memory_references('data1.txt', physical_memory, stats)

print(f"Total Page Faults: {stats.page_faults}")
print(f"Total Disk References: {stats.disk_references}")
print(f"Total Dirty Page Writes: {stats.dirty_page_writes}")
