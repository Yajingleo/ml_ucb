#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 19:52:30 2025

@author: yajingliu
"""

class BoardSet:

  def __init__(self, board):
    self.box = set()
    self.obstacle = set()
    self.m = len(board)
    self.n = len(board[0])

    for i in range(self.m):
        for j in range(self.n):
            if board[i][j] == '*':
                self.obstacle.add((i, j))
            elif board[i][j] == '#':
                self.box.add((i, j))

  def get_neighbor(self, i, j):
    neighbors = []
    for i1 in range(i - 1, i + 2):
        for j1 in range(j - 1, j + 2):
            if i1 >= 0 and i1 < self.m and j1 >= 0 and \
                j1 < self.n and (i1, j1) != (i, j):
                neighbors.append((i1, j1))
    return neighbors

  def increment(self):
    new_box = set()
    to_explode = set()
    for i, j in self.box:
        if i >= self.m - 1:
            new_box.add((i, j))
        elif all((i1, j) in self.box for i1 in range(i + 1, self.m)):
            new_box.add((i, j))
        elif (i + 1, j) not in self.obstacle:
            new_box.add((i + 1, j))
        else:
            to_explode.add((i + 1, j))
    
    for i, j in to_explode:
        for i1, j1 in self.get_neighbor(i, j):
            if (i1, j1) in new_box:
                new_box.remove((i1, j1))
    self.box = new_box

  def get_board(self):
    board = [['-' for _ in range(self.n)] for _ in range(self.m)]
    for i, j in self.box:
      board[i][j] = '#'
    for i, j in self.obstacle:
      board[i][j] = '*'
    return board
              
def falling_box(board):
  board_set = BoardSet(board)
  for _ in range(board_set.m):
    board_set.increment()
    print_board(board_set.get_board())
    print('\n')
  return board_set.get_board()

def print_board(board):
    for row in board:
        print(row)

if __name__ == "__main__":
    board = [['#', '-', '#', '#', '*'], 
         ['#', '-', '-', '#', '#'],
         ['-', '#', '-', '#', '-'],
         ['-', '-', '#', '-', '#'],
         ['#', '*', '-', '-', '-'],
         ['-', '-', '*', '#', '-']]
    print_board(board)
    print("\n")

    falling_box(board)