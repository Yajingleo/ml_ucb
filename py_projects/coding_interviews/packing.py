#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 08:18:15 2025

@author: yajingliu
"""

import collections
import itertools
import copy

SHAPES = {
  "A" : [[1]],
  "B" : [[1, 1], [1, 1]],
  "C" : [[1, 1, 1]],
  "D" : [[1, 0], [1, 1], [1, 0]],
  "E" : [[0, 1, 0], [1, 1, 1]]
}

def add(matrix, x, y, shape, ind) -> bool:
    for i in range(len(shape)):
      for j in range(len(shape[0])):
        if x + i >= len(matrix) or y + j >= len(matrix[0]):
            return False
        if matrix[x + i][y + j] != 0 and shape[i][j] != 0:
            return False
        
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] != 0:
                matrix[x + i][y + j] = ind + 1
    return True

def remove(matrix, x, y, shape) -> bool:
    for i in range(len(shape)):
      for j in range(len(shape[0])):
        if x + i >= len(matrix) or y + j >= len(matrix[0]):
            return False
        if matrix[x + i][y + j] == 0 and shape[i][j] != 0:
            return False
        if shape[i][j] != 0 and matrix[x + i][y + j] > 0:
            matrix[x + i][y + j] = 0
    return True


def dfs(matrix, x, y, letters, ind, results): 
    if len(results) > 0:
        return 
    
    if ind == len(letters):
        results.append(copy.deepcopy(matrix))
        return 
    
    if ind > len(letters):
        return 
    
    shape = SHAPES[letters[ind]]
        
    for x1, y1 in itertools.product(range(len(matrix)), range(len(matrix[0]))):
        if (x1, y1) < (x, y):
            continue
        
        if results:
            continue
        
        if not add(matrix, x1, y1, shape, ind):
            continue 
        
        dfs(matrix, 0, 0, letters, ind + 1, results)
        remove(matrix, x1, y1, shape)

def find_packing(m, n, letters):
    matrix = [[0 for _ in range(n)] for _ in range(m)]
    results = []
    dfs(matrix, 0, 0, letters, 0, results)
    return results
            
        
if __name__ == "__main__":
    m = 4
    n = 4
    letters = ['A', 'B', 'C', 'D']
    results = find_packing(m, n, letters)
    print(f"\nResults: {results}")
        
        
        
        
        
        
        
