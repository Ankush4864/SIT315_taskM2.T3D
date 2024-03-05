import queue
import threading
import heapq
import time
import random

# Global constants
NUM_TRAFFIC_SIGNALS = 10
NUM_TOP_CONGESTED = 5
NUM_PRODUCERS = 3
NUM_CONSUMERS = 2
BUFFER_CAPACITY = 100

# Bounded buffer queue
bounded_buffer = queue.Queue(maxsize=BUFFER_CAPACITY)

# Sorted list for top congested locations
top_congested = []

def generate_traffic_data():
    timestamp = time.time()
    traffic_light_id = random.randint(1, NUM_TRAFFIC_SIGNALS)
    num_cars_passed = random.randint(1, 100)
    return timestamp, traffic_light_id, num_cars_passed

def producer():
    while True:
        # Simulate generating traffic signal data
        data = generate_traffic_data()

        # Put data into the bounded buffer
        bounded_buffer.put(data)
        print(f"Producer produced: {data}")

        # Wait for 5 minutes
        time.sleep(5 * 60)

def consumer():
    while True:
        # Read from the bounded buffer
        data = bounded_buffer.get()

        # Process data to identify congested locations
        heapq.heappush(top_congested, (-data[2], data[1]))  # Using negative count for min heap behavior
        if len(top_congested) > NUM_TOP_CONGESTED:
            heapq.heappop(top_congested)
        print(f"Consumer consumed: {data}")
        bounded_buffer.task_done()

# Create and start producer threads
for _ in range(NUM_PRODUCERS):
    threading.Thread(target=producer, daemon=True).start()

# Create and start consumer threads
for _ in range(NUM_CONSUMERS):
    threading.Thread(target=consumer, daemon=True).start()

# Simulate for a certain duration
simulation_duration = 3600  # 1 hour in seconds
time.sleep(simulation_duration)

# Print the top N congested locations
print("Top Congested Locations:")
for count, location in sorted(top_congested, reverse=True):
    print(f"Traffic Light {location}: {abs(count)} cars passed by")
