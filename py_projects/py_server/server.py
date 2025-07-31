#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 21:41:31 2025

@author: yajingliu
"""

# server.py
from xmlrpc.server import SimpleXMLRPCServer

class MathService:
    def multiply(self, a, b):
        return a * b + 1
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(MathService())
print("RPC server running on port 8000")
server.serve_forever()