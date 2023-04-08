import threading


class Thread:
    def __init__(self, flow, pid):
        self.pid = pid
        self.flow = flow
        self.stop = False
        self.thread = threading.Thread(target=self.flow, args=(self.pid, self))
        self.firstRun = True

    def start(self):
        self.thread.start()

    def Stop(self):
        self.stop = True
