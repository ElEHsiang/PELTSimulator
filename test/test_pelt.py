import unittest
import pelt.pelt as pt

class PeltTestCase(unittest.TestCase):
    def test_task_util(self):
        t = pt.Task(0, "thread", 512)
        want = 512
        self.assertEqual(t.util, want)
    
    def test_task_run(self):
        # start from util 0, run 10 ms
        t = pt.Task(0, "thread", 0)
        t.run(32)

        want = 512
        self.assertEqual(t.util, want)

        # start from util 0, run 32 ms
        t = pt.Task(0, "thread", 0)
        t.run(32)

        want = 512
        self.assertEqual(t.util, want)

        # start from util 512, run 10 ms
        t = pt.Task(0, "thread", 512)
        t.run(10)

        want = 611
        self.assertEqual(t.util, want)

        # start from util 512, run 32 ms
        t = pt.Task(0, "thread", 512)
        t.run(32)

        want = 768
        self.assertEqual(t.util, want)

    def test_task_sleep(self):
        # start from util 1024, sleep 10 ms
        t = pt.Task(0, "thread", 1024)
        t.sleep(10)

        want = 824
        self.assertEqual(t.util, want)

        # start from util 1024, sleep 10 ms
        t = pt.Task(0, "thread", 1024)
        t.sleep(32)

        want = 511
        self.assertEqual(t.util, want)

        # start from util 512, sleep 10 ms
        t = pt.Task(0, "thread", 512)
        t.sleep(10)

        want = 412
        self.assertEqual(t.util, want)

        # start from util 512, sleep 32 ms
        t = pt.Task(0, "thread", 512)
        t.sleep(32)

        want = 255
        self.assertEqual(t.util, want)
        pass

    def test_task_history(self):
        t = pt.Task(0, "thread", 0)
        t.run(8)

        want_history_len = 3
        self.assertEqual(len(t.util_history), want_history_len)
        self.assertEqual(len(t.time_history), want_history_len)

        want_util_t0 = 0
        want_util_t1 = 85
        want_util_t2 = 163
        self.assertEqual(t.util_history[0], want_util_t0)
        self.assertEqual(t.util_history[1], want_util_t1)
        self.assertEqual(t.util_history[2], want_util_t2)

        want_time_t0 = 0
        want_time_t1 = 4
        want_time_t2 = 8
        self.assertEqual(t.time_history[0], want_time_t0)
        self.assertEqual(t.time_history[1], want_time_t1)
        self.assertEqual(t.time_history[2], want_time_t2)
        