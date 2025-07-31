#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 10:49:58 2025

@author: yajingliu
"""

import queue # thread safe, thus no lock required
import threading
import os
import time


class EventWriter:
    
    def __init__(self, file_path: str, batch_size: int = 5):
        self.file_path = file_path
        self.batch_size = batch_size
        self.log_queue = queue.Queue()
        self.running = True
         
        self.writer = threading.Thread(target = self._flush, daemon=True)
        self.writer.start()
        
        
    def append_event(self, data: str):
        print("append: ", data)
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log_queue.put(f"{ts}: {data}")

        
    def _flush(self):
        while self.running or not self.log_queue.empty():
            print("\nFLUSH!\n")
            batch = []
            while len(batch) < self.batch_size and not self.log_queue.empty():
                log = self.log_queue.get()
                batch.append(log)
                
            if batch:
                with open(self.file_path, 'a') as f:
                    f.write("\n".join(batch) + '\n')
                    f.flush()
                    os.fsync(f.fileno())
            time.sleep(1)
        
    def print_logs(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                print("Log: ", line)
    
    def stop(self):
        self.running = False
        self.writer.join()
        
import asyncio
import aiofile
        
        
class AsyncEventWriter:
    
    def __init__(self, file_path: str, batch_size: int = 5):
        self.file_path = file_path
        self.batch_size = batch_size
        self.log_queue = asyncio.Queue()
        self.running = True
         
        self.log_task = asyncio.create_task(self._flush())
        
        
    async def append_event(self, data: str):
        print("append: ", data)
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        await self.log_queue.put(f"{ts}: {data}")

        
    async def _flush(self):
        while self.running or not self.log_queue.empty():
            print("\nFLUSH!\n")
            batch = []
            while len(batch) < self.batch_size and not self.log_queue.empty():
                batch.append(await self.log_queue.get())
                
                
            if batch:
                with open(self.file_path, 'a') as f:
                    f.write("\n".join(batch) + '\n')
                    f.flush()
                    os.fsync(f.fileno()) 
            await asyncio.sleep(1)
        
    def print_logs(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                print("Log: ", line)
    
    async def stop(self):
        self.running = False
        await self.log_task

# if __name__ == "__main__":
#     base_dir = os.getcwd()
#     event_writer = EventWriter(f"{base_dir}/log.txt")
    
#     for i in range(10):
#         event_writer.append_event(f"Message: {i}")
#         # time.sleep(0.2)
    
#     event_writer.stop()
#     event_writer.print_logs()
   
    
async def main():
    base_dir = os.getcwd()
    async_event_writer = AsyncEventWriter(f"{base_dir}/log_3.txt")
        
    for i in range(15):
        await async_event_writer.append_event(f"Message: {i}")
        await asyncio.sleep(0.2)
        
    await async_event_writer.stop()
    
    async_event_writer.print_logs()
