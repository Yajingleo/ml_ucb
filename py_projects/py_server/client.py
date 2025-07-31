#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 21:42:43 2025

@author: yajingliu
"""

import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
print("Multiply 3*5:", proxy.multiply(3, 5))
print("Divide 10/2:", proxy.divide(10, 2))