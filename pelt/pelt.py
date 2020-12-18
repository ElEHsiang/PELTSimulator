LOAD_AVG_MAX = 47742
SCHED_CAPACITY_SCALE = 1024
SCHED_TICK_MS = 4

HALFLIFE_TIME = 32
Y = pow(0.5, 1/HALFLIFE_TIME)

def decay(util_sum, duration):
    return util_sum * (Y ** duration)

def accumulate_segment(duration):
    return sum([int(SCHED_CAPACITY_SCALE * (Y ** n)) for n in range(duration)])

class Task:
    def __init__(self, pid:int, comm: str, init_util: int = 0, scaler=None):
        self.pid = pid
        self.comm = comm
        self.util = init_util
        self._util_sum = init_util * LOAD_AVG_MAX // SCHED_CAPACITY_SCALE
        self.scaler = scaler
        self.util_history = [self.util]
        self.time = 0
        self.time_history = [0]

    def _get_scale(self):
        scale = 1
        if self.scaler:
            scale = self.scaler.get_scale()

        return scale

    def run(self, duration: int):
        scale = self._get_scale()
        duration = duration * scale

        ticks = duration // SCHED_TICK_MS
        remain = duration % SCHED_TICK_MS

        for _ in range(ticks):
            self._run(SCHED_TICK_MS)

        if remain:
            self._run(remain)

    def _run(self, duration: int):
        remain_util_sum = decay(self._util_sum, duration)
        new_util_sum = accumulate_segment(duration)

        self._util_sum = remain_util_sum + new_util_sum
        self._update_util(duration)

    def sleep(self, duration: int):
        scale = self._get_scale()
        duration = duration * scale

        ticks = duration // SCHED_TICK_MS
        remain = duration % SCHED_TICK_MS

        for _ in range(ticks):
            self._sleep(SCHED_TICK_MS)

        if remain:
            self._sleep(remain)

    def _sleep(self, duration: int):
        self._util_sum = decay(self._util_sum, duration)
        self._update_util(duration)

    def __str__(self):
        return f"pid: {self.pid}\n" \
                f"comm: {self.comm}\n" \
                f"util: {self.util}\n"

    def _update_util(self, duration: int):
        self.util = int(self._util_sum * SCHED_CAPACITY_SCALE // LOAD_AVG_MAX)
        self.util_history.append(self.util)

        self.time += duration
        self.time_history.append(self.time)

    def clear_history(self):
        self.util_history = [self.util]
        self.time = 0
        self.time_history = [0]