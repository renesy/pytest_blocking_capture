import time
import signal

class MyImp():
    def __init__(self):
        signal.signal(signal.SIGINT, self.handler)
        self.running = True

    def handler(self, signum, frame):
        self.running = False
        print('\nStopping..')

    def run(self):
        print('running')
        return True

    def run_always(self):
        print('Running forever', end='')
        while self.running:
            print('.', end='', flush=True)
            time.sleep(1)
        print('Stopped')
