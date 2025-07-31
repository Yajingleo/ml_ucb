#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 21:30:49 2025

@author: yajingliu
"""

import threading
import queue # thread safe
import os
import time
import asyncio

class EventLogWriter:
    
    def __init__(self, file_path: str, batch_size: int):
        self.file_path = file_path     
        self.batch_size = batch_size
        self.sleep_time_sec = 1 
        self.log_queue = queue.Queue()
        
        self.running = True
        self.logger_thread = threading.Thread(target = self._flush, 
                                              daemon=True)
        self.logger_thread.start()
        
        
    def AppendEvent(self, message: str):
        # print("LogEvent: ", message)
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log_queue.put(f"{ts}: {message}")
        
        
    def _flush(self):
        while self.running or not self.log_queue.empty():
            batch_logs = []
            for _ in range(self.batch_size):
                if self.log_queue.empty():
                    break
                else:
                    batch_logs.append(self.log_queue.get())
                    
            if len(batch_logs) > 0:
                with open(self.file_path, "a") as f:
                    f.write("\n".join(batch_logs) + "\n")
                    f.flush()
                    os.fsync(f.fileno())
            time.sleep(self.sleep_time_sec)
            
            
    def Stop(self):
        self.running = False
        self.logger_thread.join()
            
        
if __name__ == "__main__":
    log_file_path = "log_file_multi_threading_2.txt"
    logger = EventLogWriter(log_file_path, 10)
    
    threads = []
    for i in range(5):
        message = f"Message: {i}"
        thread = threading.Thread(target=logger.AppendEvent, 
                                  args=(message,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads[::-1]:
        thread.join()
        
    logger.Stop()
        
    with open(log_file_path, "r") as f:
        for line in f:
            print(line)
    
    
    

