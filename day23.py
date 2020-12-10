from intcodecomputer import IntCodeComputer
from collections import defaultdict
from queue import Queue, Empty
from threading import Thread
from time import sleep


def get_input():
    return parse_input(open('day23input.txt').read())


def parse_input(s):
    return [int(x) for x in s.split(',')]


class Router:
    def __init__(self):
        self.from_computers = {}
        self.to_computers = {}
        self.raw_packets = defaultdict(lambda: [])
        self.idle = False
        self.idle_cycles = 0
        self.nat_value = None
        self.prev_y_sent_to_0 = None

    def get_queue_to_computer(self, address):
        self.to_computers[address] = Queue()
        self.to_computers[address].put(address)
        return self.to_computers[address]

    def get_queue_from_computer(self, address):
        self.from_computers[address] = Queue()
        return self.from_computers[address]

    def execute(self):
        while True:
            self.idle = True
            # Get ints from each queue, add them to raw_packets
            for address, q in self.from_computers.items():
                try:
                    x = q.get(block=False)
                    self.idle = False
                    self.idle_cycles = 0
                    self.raw_packets[address].append(x)
                except Empty:
                    pass
            # Process completed packets
            for from_addr, pkt in self.raw_packets.copy().items():
                if len(pkt) != 3:
                    continue
                to_addr = pkt[0]
                x = pkt[1]
                y = pkt[2]
                if to_addr == 255:
                    if not self.nat_value:
                        print(f"Part 1 solution: {y}")
                    self.nat_value = (x, y)
                try:
                    dest = self.to_computers[to_addr]
                except:
                    pass
                else:
                    dest.put(x)
                    dest.put(y)
                del(self.raw_packets[from_addr])
            # Check whether all computers have emptied their inbound queues
            for q in self.to_computers.values():
                if not q.empty():
                    self.idle = False
            # keep track of how long we've been idle
            if self.idle:
                sleep(1)
                self.idle_cycles += 1

            # If we've been idle for 5 seconds, assume network activity is quiet
            if self.idle_cycles >= 5 and self.nat_value:
                x, y = self.nat_value
                print(f"NAT sent {(x, y)} to address 0")
                if y == self.prev_y_sent_to_0:
                    print(f"Part 2 solution: {y}")
                self.to_computers[0].put(x)
                self.to_computers[0].put(y)
                self.prev_y_sent_to_0 = y
                self.idle_cycles = 0


def start_computers():
    program = get_input()
    router = Router()
    computers = []
    for addr in range(50):
        computers.append(
            IntCodeComputer(program.copy(),
                            router.get_queue_to_computer(addr),
                            router.get_queue_from_computer(addr),
                            default_input=-1))
    threads = []
    threads.append(Thread(target=router.execute))
    for computer in computers:
        threads.append(Thread(target=computer.execute, kwargs={'blocking': False}))
    for thread in threads:
        thread.start()
    return router, threads

