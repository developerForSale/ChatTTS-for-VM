import subprocess


class RSVExecutor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RSVExecutor, cls).__new__(cls)
        return cls._instance

    def __init__(self, message_handler=None):
        self._process = None
        self._handler_func = message_handler

    @classmethod
    def get_executor(cls):
        return cls()

    def message_handler(self, message):
        if self._handler_func is not None:
            self._handler_func(message.decode("utf-8"))

    def start_process(self, *args):
        self._process = subprocess.Popen(*args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.send_out_runtime_message()

    def send_out_runtime_message(self):
        while True:
            stdout = self._process.stdout.readline()
            if stdout:
                self.message_handler(stdout)
            stderr = self._process.stderr.readline()
            if stderr:
                self.message_handler(stderr)

            if self._process.poll() is not None:
                self._process = None
                break
