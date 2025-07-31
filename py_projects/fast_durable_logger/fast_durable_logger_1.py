#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 18:33:26 2025

@author: yajingliu
"""

import threading
import queue # thread safe
import os
import time

class EventLogWriter:
    
    def __init__(self, file_path: str, batch_size: int):
        self.file_path = file_path     
        self.batch_size = batch_size
        self.flush_interval_sec = 1
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
        
    def _Timeout(self):
        self.timeout = True
        
    def _flush(self):
        last_flush_time = time.time()
        while self.running or not self.log_queue.empty():
            # print("_polling")
            batch_logs = []
            self.timeout = False
            timer = threading.Timer(self.flush_interval_sec, self._Timeout)
            timer.start()
            
            while len(batch_logs) < self.batch_size and not self.timeout:
                    if not self.log_queue.empty():
                        batch_logs.append(self.log_queue.get())
            
            if batch_logs:
                with open(self.file_path, "a") as f:
                    f.write("\n".join(batch_logs) + "\n")
                    f.flush()
                    os.fsync(f.fileno())
                    last_flush_time = time.time()
            time.sleep(self.sleep_time_sec)
            
            
    def Close(self):
        self.running = False
        self.logger_thread.join()
            
        
if __name__ == "__main__":
    log_file_path = "log_file_new_2.txt"
    logger = EventLogWriter(log_file_path, 10)
    
    threads = []
    for i in range(11):
        message = f"Message: {i}"
        thread = threading.Thread(target=logger.AppendEvent, 
                                  args=(message,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads[::-1]:
        thread.join()
        
    logger.Close()
        
    with open(log_file_path, "r") as f:
        for line in f:
            print(line)
    
    
    

