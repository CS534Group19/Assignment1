# Author: Oliver Schulman
# Updated: 2/9/2023
# Refactoring: Cutter Beck

import csv
import sys
import time
import random
import math
from initialization import Initialization
from new_board import *


# TODO NEED to incorporate runtime here somehow
# TODO get an explanation of this code so it can be paired down and centralized to use our board structure as we have to mesh this with greedy and sidemove hill climbing


def main():
    # Hill Climbing param order -> board_file_name.csv run_time
    # Params stored in sys.argv array, sys.argv[0] is the name of the Python file being executed
    # arg_board_csv = str(sys.argv[1])
    # arg_run_time = float(sys.argv[2])

    # Boards for testing
    # Professor Beck's boards
    BOARD_1 = "./documentation/test_boards/board1.csv" # not solvable according to https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
    BOARD_2 = "./documentation/test_boards/board2.csv" # solvable according to https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

    # Cutter Beck's boards
    BOARD_3 = "./documentation/test_boards/board3.csv" # ~0.2 seconds, 4 moves, 8 nodes, 18 cost, branching factor 1.7
    BOARD_4 = "./documentation/test_boards/board4.csv" # ~22 seconds, 6 moves, 52 nodes, 26 cost, branching factor 1.9
    BOARD_5 = "./documentation/test_boards/board5.csv" # ~418.7 seconds, or ~7 min, 5 moves, 25 nodes, 60 cost, branching factor 1.9
    BOARD_6 = "./documentation/test_boards/board6.csv" # ~10.5 seconds, 3 moves, 14 nodes, 18 cost, branching factor 2.4
    BOARD_7 = "./documentation/test_boards/board7.csv" # ~3.8 seconds, 4 moves, 14 nodes, 46 cost, branching factor 1.9

    arg_board_csv = BOARD_3
    arg_run_time = 30

    # Read file and create starting board
    startingboard = []

    with open(arg_board_csv) as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            startingboard = startingboard + row

    #Sort strings into integers for sorting

    for i in range(0, len(startingboard)) :
        if startingboard[i] != 'B':
            startingboard[i] = int(startingboard[i])

    #Create 2 possible goal states
    frontboard = list(startingboard)
    backboard = list(startingboard)

    #Replace blank spaces with arbitary integer to go in the front or back of puzzle depending on win state
    for j, item in enumerate(frontboard):
        if item == 'B':
            frontboard[j] = 0

    for q, item in enumerate(backboard):
        if item == 'B':
            backboard[q] = 1000

    #Sort boards to match their win state

    frontboard.sort()
    backboard.sort()

    #Pick Win State and Continuously calculate distance
    if getFrontManhattanDistance(startingboard, frontboard) > getBackManhattanDistance(startingboard, backboard):
        winState = backboard
    else:
        winState = frontboard
   
    print("Initial Manhatten Distance")
    print (CalculateDistance(startingboard, backboard, frontboard, winState))
    
    tic = time.perf_counter()
    newBoard = solution_SimulatedAnnealing(startingboard, backboard, frontboard, winState)
    toc = time.perf_counter()
    print(newBoard)
    print(f"\nSearch took {toc - tic:0.4f} seconds")

    # tic = time.perf_counter()
    # Count += 1
    # inProccessBoard = solution_SimulatedAnnealing(startingboard, backboard, frontboard, winState)
    # if FAILED:
    #         result += "Failed!"
    # else:
    #         for col in range(len(inProccessBoard)):
    #          result += str(inProccessBoard[col]) + " "
    # result += "\n"
    
    # toc = time.perf_counter()
    # print(f"\nSearch took {toc - tic:0.4f} seconds")
    # result += "Success rate: " + str(Count / float(Count)) + '\n'

    # print (result)


#Calculate Weighted Manhattan Distance for each win state
def getFrontManhattanDistance(anyboard, frontboard):
    totaldistance = 0
    for i in range(len(anyboard)):
        sideLength = math.sqrt(len(anyboard))
        if (anyboard[i] != 0 and anyboard[i] != 1000 and anyboard[i] != 'B'):
            index = frontboard.index(anyboard[i]) + 1            
            
            boardx = (i+1)%sideLength
            winx = index%sideLength
            if boardx == 0:
                boardx = sideLength
            if winx == 0:
                winx = sideLength

            xdistance = abs(boardx - winx)
            ydistance = abs((i+1) - boardx - index + winx) / sideLength

            totaldistance += anyboard[i] * (xdistance + ydistance)
            
    return totaldistance

def getBackManhattanDistance(anyboard, backboard):
    totaldistance = 0
    for i in range(len(anyboard)):
        sideLength = math.sqrt(len(anyboard))
        if (anyboard[i] != 0 and anyboard[i] != 1000 and anyboard[i] != 'B'):
            index = backboard.index(anyboard[i]) + 1

            boardx = (i+1)%sideLength
            winx = index%sideLength

            if boardx == 0:
                boardx = sideLength
            if winx == 0:
                winx = sideLength

            xdistance = abs(boardx - winx)
            ydistance = abs((i+1) - boardx - index + winx) / sideLength

            totaldistance += anyboard[i] * (xdistance + ydistance)
    return totaldistance


def CalculateDistance(board, backboard, frontboard, winState):
    if winState == backboard:
        return getBackManhattanDistance(board, backboard)
    else:
        return getFrontManhattanDistance(board, frontboard)

#Hill Climbing Alg with Simulated Annealing
def hillClimbing(anyBoard, backboard, frontboard, winState, count):

 #Set Temperature for Annealing
 temp = len(anyBoard)
 decay = 0.995

 #Blank Spaces
 for i in range(len(anyBoard)):
        if anyBoard[i] == 1000 or anyBoard[i] == 0 or anyBoard[i] == 'B':
            break

 d = 0
 d = CalculateDistance(anyBoard, backboard, frontboard, winState)
 temp = temp * decay
 if (temp < 0.3):
     temp = 0.3

 sideLength = math.sqrt(len(anyBoard))
 sideLength = int(sideLength)
 while True:
     randCase = random.randint(1,5)
     if randCase == 1:
            if i >= sideLength:
                upMove = anyBoard
                upMove[i] = anyBoard[i-sideLength]
                upMove[i-sideLength] = 'B'
                if (CalculateDistance(upMove, backboard, frontboard, winState) < d):
                    return upMove
                else:
                    deltaE = CalculateDistance(upMove, backboard, frontboard, winState) - d
                    acceptProbability = min(math.exp(deltaE / temp), 1)
                    if random.random() <= acceptProbability:
                        return upMove
     elif randCase == 2:
            if i < (sideLength * sideLength - sideLength):
                downMove = anyBoard
                downMove[i] = anyBoard[i+sideLength]
                downMove[i+sideLength] = 'B'
                if CalculateDistance(downMove, backboard, frontboard, winState) < d:
                    return downMove
                else:
                    deltaE = CalculateDistance(downMove, backboard, frontboard, winState) - d
                    acceptProbability = min(math.exp(deltaE / temp), 1)
                    if random.random() <= acceptProbability:
                        return downMove
     elif randCase == 3:
            if i%sideLength != 0:
                leftMove = anyBoard
                leftMove[i] = anyBoard[i-1]
                leftMove[i-1] = 'B'
                if (CalculateDistance(leftMove, backboard, frontboard, winState) < d):
                    return leftMove
                else:
                    deltaE = CalculateDistance(leftMove, backboard, frontboard, winState) - d
                    acceptProbability = min(math.exp(deltaE / temp), 1)
                    if random.random() <= acceptProbability:
                        return leftMove
     else:    
            if (i+1)%sideLength != 0:
                rightMove = anyBoard
                rightMove[i] = anyBoard[i+1]
                rightMove[i+1] = 'B'
                if CalculateDistance(rightMove, backboard, frontboard, winState) < d:
                    return rightMove
                else:
                    deltaE = CalculateDistance(rightMove, backboard, frontboard, winState) - d
                    acceptProbability = min(math.exp(deltaE / temp), 1)
                    if random.random() <= acceptProbability:
                        return rightMove
                    
 return anyBoard


def solution_SimulatedAnnealing(board, backboard, frontboard, winState):
    # the success rate will increase by increasing the maxRound
    maxRound = 10000000
    count = 0
    originalboard = board

    while True:
        collisionNum = CalculateDistance(board, backboard, frontboard, winState)
        if collisionNum == 0:
            print("Move Count (Total Nodes Visited)")
            print (count)
            print("Moves in Solution (Node Depth)")
            print(count%1000)
            print("Branching Factor")
            print((count)**(1/count%1000))
            print("Final Board")
            return board
        if count%1000 == 0:
            board = originalboard
        board = hillClimbing(board, backboard, frontboard, winState, count)
        count += 1
        if(count >= maxRound):
            print("Could not complete in time")
            return board


if __name__ == '__main__':
    main()