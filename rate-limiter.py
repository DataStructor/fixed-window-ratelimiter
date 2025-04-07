import time
from collections import defaultdict

class FixedWindowRateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_counts = defaultdict(int)
        self.window_start_times = defaultdict(float)

    def hit(self, client_identifier):
        current_time = time.time()

        if client_identifier not in self.window_start_times or current_time - self.window_start_times[client_identifier] >= self.time_window:
            self.window_start_times[client_identifier] = current_time
            self.request_counts[client_identifier] = 0

        self.request_counts[client_identifier] += 1

        if self.request_counts[client_identifier] > self.max_requests:
            return False
        else:
            return True

if __name__ == '__main__':
    limiter = FixedWindowRateLimiter(max_requests=5, time_window=10)

    print("Client A:")
    for i in range(7):
        client_id = "client_a"
        if limiter.hit(client_id):
            print(f"Request {i+1} from {client_id} - Allowed")
        else:
            print(f"Request {i+1} from {client_id} - Rate Limited!")
        time.sleep(1)

    print("\nClient B:")
    for i in range(3):
        client_id = "client_b"
        if limiter.hit(client_id):
            print(f"Request {i+1} from {client_id} - Allowed")
        else:
            print(f"Request {i+1} from {client_id} - Rate Limited!")
        time.sleep(2)

    time.sleep(10)

    print("\nClient A again (after window reset):")
    for i in range(3):
        client_id = "client_a"
        if limiter.hit(client_id):
            print(f"Request {i+1} from {client_id} - Allowed")
        else:
            print(f"Request {i+1} from {client_id} - Rate Limited!")
        time.sleep(1)