#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from boardstate import *
from copy import deepcopy
from evaluate import *
from gomoku import Gomoku


class gomokuAI(object):
    
    ## currentstate is just black or white
    def __init__(
        self,
        gomoku,
        currentState,
        depth,
        ):

        self.__gomoku = gomoku
        self.__currentState = currentState
        self.__depth = depth
        self.__currentI = -1
        self.__currentJ = -1

    def set_board(
        self,
        i,
        j,
        state,
        ):

        self.__gomoku.set_chessboard_state(i, j, state)

    def has_neighbor(
        self,
        state,
        i,
        j,
        ):
        '''
        This returns if a specific point on the board has
        neighbors or not. Neighbors are defined as pieces
        within 2 empty intersections.
        '''
        #exhaustive search for four axes
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),
                      (1, -1)], [(-1, -1), (1, 1)]]
        for axis in directions:
            for (xdirection, ydirection) in axis:

                if xdirection != 0 and (j + xdirection < 0 or j
                        + xdirection >= N):
                    break
                if ydirection != 0 and (i + ydirection < 0 or i
                        + ydirection >= N):
                    break
                if self.__gomoku.get_chessMap()[i + ydirection][j
                        + xdirection] != BoardState.EMPTY:
                    return True

                if xdirection != 0 and (j + xdirection * 2 < 0 or j
                        + xdirection * 2 >= N):
                    break

                if ydirection != 0 and (i + ydirection * 2 < 0 or i
                        + ydirection * 2 >= N):
                    break

                if self.__gomoku.get_chessMap()[i + ydirection * 2][j
                        + xdirection * 2] != BoardState.EMPTY:
                    return True

        return False

    def direction_count(
        self,
        i,
        j,
        xdirection,
        ydirection,
        state,
        ):
        '''
        This counts how many connected pieces are on a specific
        direction. Returns the counted number.
        '''

        count = 0
        fiveStore=[]#7022
        for step in range(1, 5):  # look four more steps on a certain direction
            if xdirection != 0 and (j + xdirection * step < 0 or j
                                    + xdirection * step >= N):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i
                                    + ydirection * step >= N):
                break
            if self.__gomoku.get_chessMap()[i + ydirection * step][j
                    + xdirection * step] == state:
                count += 1
                fiveStore.append((i+ydirection * step,j + xdirection*step))#7022
                
            else:
                break
        return count,fiveStore

    def direction_pattern(
        self,
        i,
        j,
        xdirection,
        ydirection,
        state,
        ):
        '''
        Returns the pattern with length 6 to evaluate later
        '''

        pattern = []
        fourStore=[]#7022
        for step in range(-1, 5):  # generate a list with len 10
            if xdirection != 0 and (j + xdirection * step < 0 or j
                                    + xdirection * step >= N):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i
                                    + ydirection * step >= N):
                break

            pattern.append(self.__gomoku.get_chessMap()[i + ydirection
                           * step][j + xdirection * step])
            
            fourStore.append((i+ydirection * step,j + xdirection*step))

        return pattern,fourStore

    def has_checkmate(
        self,
        state,
        i,
        j,
        ):
        '''
        Checkmate means five in a row.
        '''
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),
                      (1, -1)], [(-1, -1), (1, 1)]]

        for axis in directions:
            axis_count = 1
            fiveSpots=[]#7022
            for (xdirection, ydirection) in axis:
                '''
                axis_count += self.direction_count(i, j, xdirection,
                        ydirection, state)
                '''
                transfer_axis_count, transfer_fiveSpots= self.direction_count(i, j, xdirection,
                        ydirection, state)#7022
                
                axis_count += transfer_axis_count#7022
                
                fiveSpots += transfer_fiveSpots#7022
                
                if axis_count >= 5:
                    
                    print('Five in a row:','(',i,',',j,') with',fiveSpots)#7022
                    
                    return True
        return False

    def has_check(
        self,
        state,
        i,
        j,
        ):
        '''
        Check means a unblocked four.
        Double-three should also be a check, but it's not added yet.
        '''
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),
                      (1, -1)], [(-1, -1), (1, 1)]]

        for axis in directions:
            currentPattern = []
            fourStore=[]#7022
            for (xdirection, ydirection) in axis:
                
                #????why double add??????
                '''
                currentPattern += self.direction_pattern(i, j,
                        xdirection, ydirection, state)
                '''
                transfer_currentPattern, transfer_foureSpots= self.direction_pattern(i, j,
                        xdirection, ydirection, state)#7022
                
                currentPattern += transfer_currentPattern#7022
                
                fourStore += transfer_foureSpots#7022
                
              
                
                if len(currentPattern) > 2:
                    currentPattern[1] = state
                if enum_to_string(currentPattern) == WHITE_6PATTERNS[0]:
                    
                    return True, fourStore #7022
                
                if enum_to_string(currentPattern) == BLACK_6PATTERNS[0]:
                    
                    return True, fourStore#7022
                
        return False, fourStore#7022

    def opponent_has_checkmate(self, state):
        '''
        Check if opponent has checkmate.
        '''
        vectors = []

        #exhaustive search

        for i in range(N):
            vectors.append(self.__gomoku.get_chessMap()[i])

        for j in range(N):
            vectors.append([self.__gomoku.get_chessMap()[i][j] for i in
                           range(N)])

        vectors.append([self.__gomoku.get_chessMap()[x][x] for x in
                       range(N)])
        for i in range(1, N - 4):
            v = [self.__gomoku.get_chessMap()[x][x - i] for x in
                 range(i, N)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[y - i][y] for y in
                 range(i, N)]
            vectors.append(v)

        vectors.append([self.__gomoku.get_chessMap()[x][N - x - 1]
                       for x in range(N)])
        for i in range(4, N - 1):
            v = [self.__gomoku.get_chessMap()[x][i - x] for x in
                 range(i, -1, -1)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[x][N - x + N - i - 2]
                 for x in range(N - i - 1, N)]
            vectors.append(v)

        #checkmate
        for vector in vectors:
            temp = enum_to_string(vector)
            if state == BoardState.BLACK:
                for pattern in WHITE_5PATTERNS:
                    if sublist(pattern, temp):
                        return True
            if state == BoardState.WHITE:
                for pattern in BLACK_5PATTERNS:
                    if sublist(pattern, temp):
                        return True
        return False

    def generate(self):
        '''
        Generate a list of available points for searching.
        '''
        ## store the nodes
        frontierList = []
        for i in range(N):
            for j in range(N):
                ## just consider empty 
                if self.__gomoku.get_chessMap()[i][j] \
                    != BoardState.EMPTY:
                    continue  # only search for available spots
                if not self.has_neighbor(self.__gomoku.get_chessMap()[i][j],
                        i, j):
                    continue

                if self.__currentState == BoardState.WHITE:
                    nextState = BoardState.BLACK
                else:
                    nextState = BoardState.WHITE

                #depth -1 every time
                
                #### first parameter of gomoku is the state of whole board 
                nextPlay = gomokuAI(deepcopy(self.__gomoku), nextState,
                                    self.__depth - 1)
                nextPlay.set_board(i, j, self.__currentState)

                frontierList.append((nextPlay, i, j))

        # Degree Heuristcs, Sort points based on their evaluation

        frontierScores = []
        for node in frontierList:
            frontierScores.append(self.evaluate_point(node[1], node[2]))

        frontierZipped = zip(frontierList, frontierScores)
        frontierSorted = sorted(frontierZipped, key=lambda t: t[1])
        (frontierList, frontierScores) = zip(*frontierSorted)
        return frontierList

    def negate(self):
        return -self.evaluate()

    def evaluate(self):
        '''
        Return the board score for Minimax Search.
        '''
        #exhaustive search
        vectors = []
        
        #row
        for i in range(N):
            vectors.append(self.__gomoku.get_chessMap()[i])

        #column
        for j in range(N):
            vectors.append([self.__gomoku.get_chessMap()[i][j] for i in
                           range(N)])
        
        vectors.append([self.__gomoku.get_chessMap()[x][x] for x in
                       range(N)])
       
        #
        for i in range(1, N - 4):
            # y=x dialogue below
            v = [self.__gomoku.get_chessMap()[x][x - i] for x in
                 range(i, N)]
            vectors.append(v)
            # y=x dialogue above
            v = [self.__gomoku.get_chessMap()[y - i][y] for y in
                 range(i, N)]
            vectors.append(v)

        vectors.append([self.__gomoku.get_chessMap()[x][N - x - 1]
                       for x in range(N)])

        
        
        for i in range(4, N - 1):
            v = [self.__gomoku.get_chessMap()[x][i - x] for x in
                 range(i, -1, -1)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[x][N - x + N - i - 2]
                 for x in range(N - i - 1, N)]
            vectors.append(v)

        board_score = 0

       
        
        for v in vectors:
            score = evaluate_vector(v)
            if self.__currentState == BoardState.WHITE:
                board_score += score['black'] - score['white']
            else:
                board_score += score['white'] - score['black']
        return board_score

    def evaluate_point(self, i, j):
        '''
        Return a point score for Degree Heuristics.
        '''
        vectors = []
        vectors.append(self.__gomoku.get_chessMap()[i])
        vectors.append([self.__gomoku.get_chessMap()[i][j] for i in
                       range(N)])

        if j > i:
            v = [self.__gomoku.get_chessMap()[x][x + j - i] for x in
                 range(0, N - j + i)]
            vectors.append(v)
        elif j == i:

            vectors.append([self.__gomoku.get_chessMap()[x][x] for x in
                           range(N)])
        elif j < i:

            v = [self.__gomoku.get_chessMap()[x + i - j][x] for x in
                 range(0, N - i + j)]
            vectors.append(v)

        if i + j == N - 1:
            vectors.append([self.__gomoku.get_chessMap()[x][N - 1 - x]
                           for x in range(N)])
        elif i + j < N - 1:

            v = [self.__gomoku.get_chessMap()[x][N - 1 - x - abs(i
                 - j)] for x in range(N - abs(i - j))]
            vectors.append(v)
        elif i + j > N - 1:

            vectors.append([self.__gomoku.get_chessMap()[x][N - 1 - x
                           + i + j - N + 1] for x in range(i + j - N
                           + 1, N)])

        point_score = 0
        for v in vectors:
            score = evaluate_vector(v)
            if self.__currentState == BoardState.WHITE:
                point_score += score['white']
            else:
                point_score += score['black']
        return point_score

    def alpha_beta_prune(
        self,
        ai,
        alpha=-10000000,
        
        ## why it is 10000000
        beta=10000000,
        ):
        ## 
        
        steps=[]#7022
        
        if ai.__depth <= 0:
            ## negate min max score
            score = ai.negate()
            location=((None,None))##7022
            #print('Terminal-Node:','board-score',score*(-1),'node-depth:',ai.__depth)#7022
            return score,location##7022
        
        # only use the first 20 nodes

        # for (nextPlay, i, j) in ai.generate()[:20]:
        for (nextPlay, i, j) in ai.generate():
            '''
            print('father-node\'s beta-alpha:',beta,'&',alpha,'move:','(',i,',',j,')','player:',ai.__currentState,'node-depth', \
                  nextPlay.__depth)#7022
            '''
            ## negate alpha???
            ## Since '-' every time it is different
            ## why - beta, - alpha
                                                         
            transfer_steps=[]
            
            transfer_score, transfer_location = self.alpha_beta_prune(nextPlay, -beta, -alpha)##7022
            temp_score=-transfer_score
            
            transfer_steps += transfer_location#7022
            #print('--------',temp_score,'!!!!beta-alpha',beta,alpha,' loc:',i,'-',j, \
                  #nextPlay.__currentState,nextPlay.__depth)
                  
            
                
            if temp_score > beta:
                #print(temp_score,'> beta',beta)#7022
                transfer_steps.append((i,j))#7022
                
                if nextPlay.__depth==1:   #7022
                    steps.append(transfer_steps)  #7022
                    return beta,steps##7022
                else:
                    return beta,transfer_steps##7022
                
            if temp_score > alpha:
                #print(temp_score,'> alpha:',alpha)#7022
                alpha = temp_score
                (ai.__currentI, ai.__currentJ) = (i, j)
                
                transfer_steps.append((i,j))#7022
                
                if nextPlay.__depth==1:   #7022
                    steps.append(transfer_steps)  #7022
                else:
                    steps=transfer_steps
        return alpha,steps ##7022
    
        ## no alpha > beta
    
        
    def first_step(self):
        #AI plays in the center
        self.__gomoku.set_chessboard_state(7, 7, self.__currentState)
        return True

    def one_step(self):
        
        # ????? why not use ''generate' function
        for i in range(N):
            for j in range(N):
                if self.__gomoku.get_chessMap()[i][j] \
                    != BoardState.EMPTY:
                    continue  # only search for available spots

                ## ??i ,j is a position which could be five in a row,-----!!!1
                if self.has_checkmate(self.__currentState, i, j):
                    print ('has checkmate')
                    self.__gomoku.set_chessboard_state(i, j,
                            self.__currentState)
                    return True
                ##  without neighbor, jump this position
                if not self.has_neighbor(self.__gomoku.get_chessMap()[i][j],
                        i, j):
                    continue
                ## Firstly check self, then check opponent ???
                '''
                if self.has_check(self.__currentState
                '''
                TrueOrFalse_hasCheck, fourStore=self.has_check(self.__currentState, i, j)#7022
                if TrueOrFalse_hasCheck:
                    print ('has check, checking if opponent already has one...')

                    if self.opponent_has_checkmate(self.__currentState) \
                        is True:

                        print ('not safe, searching other moves...')
                    elif self.opponent_has_checkmate(self.__currentState) \
                        is False:
                        ## set a move
                        print ('safe')
                        print('unbroken four in a row:',fourStore)#####7022
                        #-------!!!!
                        self.__gomoku.set_chessboard_state(i, j,
                                self.__currentState)
                        return True
       
        # node is just a class
        node = gomokuAI(self.__gomoku, self.__currentState,
                        self.__depth)
        #???????????? will next step be changed
        score,steps = self.alpha_beta_prune(node)#7022
        print('steps',steps)#7022
        (i, j) = (node.__currentI, node.__currentJ)
        print ('score',score,' loc:',i,'-',j)
        # ??? is the next step an empty position
        if not i is None and not j is None:
            if self.__gomoku.get_chessboard_state(i, j) \
                != BoardState.EMPTY:
                self.one_step()
            else:
                self.__gomoku.set_chessboard_state(i, j,
                        self.__currentState)
                return True
        return False
