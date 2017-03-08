# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import os
import psutil
import time
from threading import Thread
from settings import Settings

class Consumption():
    def __init__(self):
        self.pid = os.getpid()
        self.proc = psutil.Process(self.pid)
        self.ConsumptionFormatted_CPU = 0.0
        self.ConsumptionFormatted_Memory = 0.0
        self.pool_CPU = True
        self.pool_Memory = True

    def start_pooling(self):
        self.thread_cpu = Thread(target=self.get_consumption_cpu, args=())
        self.thread_cpu.start()

        self.thread_memory = Thread(target=self.get_consumption_memory, args=())
        self.thread_memory.start()

    def stop_pooling(self):
        self.pool_CPU = False
        self.pool_Memory = False

    def get_consumption(self):
        consumption = ''
        if self.ConsumptionFormatted_CPU != '':
            consumption += 'CPU: ' + str(self.ConsumptionFormatted_CPU)
        if self.ConsumptionFormatted_Memory != '':
            consumption += (', ' if consumption != '' else '') + 'Memory: ' + str('%.2f' % self.ConsumptionFormatted_Memory)
        return consumption

    def get_consumption_cpu(self):
        while self.pool_CPU:
            self.ConsumptionFormatted_CPU = str(self.proc.cpu_percent(interval=Settings.Consumption_Interval_CPU))
            time.sleep(Settings.Consumption_Interval_CPU)

    def get_consumption_memory(self):
        while self.pool_Memory:
            mem = self.proc.memory_full_info()
            self.ConsumptionFormatted_Memory = mem.rss / (1024.0 * 1024.0)
            time.sleep(Settings.Consumption_Interval_Memory)
