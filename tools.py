import time

class Timer():
    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.elapsed = None

    def start(self, txt):
        self.start_time = time.perf_counter()
        self.stop_time = None
        self.elapsed = None
        print(f'{txt} started')

    def stop(self, txt):
        if self.start_time is None:
            raise ValueError('Timer not started')
        self.stop_time = time.perf_counter()
        self.elapsed = self.stop_time - self.start_time
        print(f'{txt} ended. Elapsed time: {self.elapsed:0.3f}')