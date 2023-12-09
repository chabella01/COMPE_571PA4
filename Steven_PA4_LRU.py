import time

class PageTableEntry:
    def __init__(self):
        self.physical_page_number = None
        self.dirty = False
        self.referenced = False

class ProcessMemory:
    def __init__(self):
        self.page_table = [PageTableEntry() for _ in range(128)]  # 128 entries

class PhysicalMemory:
    def __init__(self, size):
        self.size = size
        self.pages = {}  # Map virtual page to (physical page, last used time, is dirty)
        self.next_physical_page = 0  # Initialize the next physical page number

    def load_page(self, virtual_page, process_number, is_dirty):
        # Evict a page if memory is full
        if len(self.pages) >= self.size:
            self.evict_page()

        physical_page = self.next_physical_page
        self.pages[(process_number, virtual_page)] = (physical_page, time.time(), is_dirty)
        self.next_physical_page += 1
        return physical_page
    def evict_page(self):
        # Evict the oldest page (FIFO)
        oldest_time = time.time()
        lru_page = None
        for page, (physical_page, last_used_time, is_dirty) in self.pages.items():
            if last_used_time < oldest_time:
                oldest_time = last_used_time
                lru_page = page

        # Evict the LRU page
        if lru_page is not None:
            del self.pages[lru_page]

    def update_page_access(self, process_number, virtual_page, is_write):
        if (process_number, virtual_page) in self.pages:
            physical_page, _, is_dirty = self.pages[(process_number, virtual_page)]
            self.pages[(process_number, virtual_page)] = (physical_page, time.time(), is_dirty or is_write)

    def is_full(self):
        return len(self.pages) >= self.size

    def get_lru_page_info(self):
        # Find the least recently used page
        oldest_time = time.time()
        lru_page = None
        for page, (physical_page, last_used_time, is_dirty) in self.pages.items():
            if last_used_time < oldest_time:
                oldest_time = last_used_time
                lru_page = page

        # Return information about the LRU page
        if lru_page is not None:
            return {
                'process_number': lru_page[0],
                'virtual_page': lru_page[1],
                'is_dirty': self.pages[lru_page][2]
            }
        return None    

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
            is_write = operation == 'W'
            page_table_entry = processes[process_number].page_table[page_number]

            # Check if the page is in physical memory
            if page_table_entry.physical_page_number is None:
                # Page fault occurs
                stats.page_faults += 1
                stats.disk_references += 1

                # Check for a dirty page before eviction
                if physical_memory.is_full():
                    evicted_page_info = physical_memory.get_lru_page_info()
                    if evicted_page_info and evicted_page_info['is_dirty']:
                        stats.dirty_page_writes += 1
                        stats.disk_references += 1

                # Load the new page
                page_table_entry.physical_page_number = physical_memory.load_page(page_number, process_number, is_write)
            else:
                physical_memory.update_page_access(process_number, page_number, is_write)

            if is_write:
                page_table_entry.dirty = True

            print(f"Process {process_number}, Address: {address}, Page: {page_number}, Operation: {operation}")


# initialize physical memory and statistics
physical_memory = PhysicalMemory(32)
stats = Statistics()

# Process the memory references
process_memory_references('data1.txt', physical_memory, stats)

# Print statistics
print(f"Total Page Faults: {stats.page_faults}")
print(f"Total Disk References: {stats.disk_references}")
print(f"Total Dirty Page Writes: {stats.dirty_page_writes}")

