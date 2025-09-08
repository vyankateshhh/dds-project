import heapq
from collections import deque

# ---------------- Rider & Driver Classes ----------------
class Rider:
    def __init__(self, rider_id, name):
        self.id = rider_id
        self.name = name

class Driver:
    def __init__(self, driver_id, distance, rating):
        self.id = driver_id
        self.distance = distance
        self.rating = rating

    def __lt__(self, other):
        # Priority: nearest distance first
        # If distance same -> higher rating wins
        if self.distance == other.distance:
            return self.rating > other.rating
        return self.distance < other.distance

# ---------------- Rider Queue (FIFO) ----------------
class RiderQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, rider):
        self.queue.append(rider)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        print("No riders waiting!")
        return None

    def is_empty(self):
        return len(self.queue) == 0

# ---------------- Driver Priority Queue ----------------
class DriverPQ:
    def __init__(self):
        self.heap = []

    def insert(self, driver):
        heapq.heappush(self.heap, driver)

    def extract_min(self):
        if self.heap:
            return heapq.heappop(self.heap)
        print("No drivers available!")
        return None

    def is_empty(self):
        return len(self.heap) == 0

# ---------------- Ride History ----------------
class RideHistory:
    def __init__(self):
        self.history = []

    def add(self, rider_id, driver_id):
        self.history.append((rider_id, driver_id))

    def show(self):
        print("\nRide History:")
        for r, d in self.history:
            print(f"Rider {r} -> Driver {d}")

# ---------------- Main Simulation ----------------
if __name__ == "__main__":
    rq = RiderQueue()
    pq = DriverPQ()
    history = RideHistory()

    # Sample riders
    rq.enqueue(Rider(1, "Alice"))
    rq.enqueue(Rider(2, "Bob"))
    rq.enqueue(Rider(3, "Charlie"))

    # Sample drivers (id, distance, rating)
    pq.insert(Driver(101, 2.5, 4.8))
    pq.insert(Driver(102, 1.2, 4.5))
    pq.insert(Driver(103, 1.2, 4.9))
    pq.insert(Driver(104, 3.0, 4.7))

    # Match riders to drivers
    while not rq.is_empty() and not pq.is_empty():
        rider = rq.dequeue()
        driver = pq.extract_min()

        print(f"Matched Rider {rider.id} ({rider.name}) "
              f"with Driver {driver.id} [Dist={driver.distance}, Rating={driver.rating}]")

        history.add(rider.id, driver.id)

    # Show ride history
    history.show()
print("✅ Python file is working fine!")
