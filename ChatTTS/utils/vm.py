import logging
import subprocess


class RSVExecutor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RSVExecutor, cls).__new__(cls)
        return cls._instance

    def __init__(self, event_handler=None):
        self._process = None
        self._handler_func = event_handler

    @classmethod
    def get_executor(cls):
        return cls()

    def event_handler(self, event, level):
        if self._handler_func is not None:
            self._handler_func(event.decode("utf-8"), level)

    def start_process(self, *args):
        self._process = subprocess.Popen(
            [args[0], *args[1:]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.send_out_runtime_event()

    def send_out_runtime_event(self):
        while True:
            stdout = self._process.stdout.readline()
            if stdout:
                self.event_handler(stdout, logging.INFO)
            stderr = self._process.stderr.readline()
            if stderr:
                self.event_handler(stderr, logging.ERROR)

            if self._process.poll() is not None:
                self._process = None
                break
