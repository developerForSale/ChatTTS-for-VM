import subprocess
import uuid


class RSVExecutor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RSVExecutor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._process = None
            self._handler_func = None
            self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    def set_handler_func(self, func):
        self._handler_func = func

    def event_handler(self, event: str, group_id: str):
        if self._handler_func is not None:
            self._handler_func(event, group_id)

    def send_out_runtime_event(self):
        new_group_id = str(uuid.uuid4())
        while True:
            stdout = self._process.stdout.readline()
            if stdout:
                self.event_handler(stdout.decode("utf-8"), new_group_id)

            if self._process.poll() is not None:
                self._process = None
                break

    def start_process(self, *args):
        self._process = subprocess.Popen([args[0], *args[1:]], stdout=subprocess.PIPE)
        self.send_out_runtime_event()
