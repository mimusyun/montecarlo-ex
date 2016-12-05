#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

Monte Carlo Simulation Experiment : small mini game example

(Rule)
Two player alternately　takes turns and get a number from either side of the given list.
The game ends when the given list becomes empty.
The sum of the numbers is the score of each player.
If the sum is lager, you win.

(Example)
# Initial State
Given list: [4,2,2,3,1] / Player scores: (0, 0)

Player 1 : Get 4 from LEFT => Scores (4, 0)
List: [2,2,3,1]

Player 2 : Get 1 from RIGHT => Scores (4, 1)
List: [2,2,3]

Player 1 : Get 1 from RIGHT => Scores (7, 4)
List: [2,2]

Player 2 : Get 1 from RIGHT => Scores (7, 6)
List: [2]

Player 2 : Get 1 from LEFT => Scores (9, 6)
List: []

# GAMESET
9 vs 6 => Player1 wins

# Optimized User by Monte Carlo
Every time before picking a side (left or right), Computer User executes simulation with a given number of TRIALs.
Computer User chose the best move to maximize the probability to win the game. 

"""

import random

# Set True if you want to compete with Computer
PLAYER_MODE = True

# Set True if you run the program in debug mode
DEBUG = False

# Number of trials for simulation. The larger number you choose, the stronger Computer User will be
TRIALS = 500000

# Given List for the game
GIVEN_LST = [random.randint(8,10) for r in xrange(15)]

class Base:

    def __init__(self):
        self.lst = []; 
        self.myscore = 0       
        self.yourscore = 0
        self.myturn = True

    def get_left(self):
        """
        Takes a number from left side of the list
        and switch a player
        """
        score = self.lst.pop(0)
        if self.myturn:
            self.myscore += score
        else:
            self.yourscore += score
        self.myturn = not self.myturn
        
    def get_right(self):
        """
        Takes a number from right side of the list
        and switch a player
        """
        score = self.lst.pop()
        if self.myturn:
            self.myscore += score
        else:
            self.yourscore += score
        self.myturn = not self.myturn
        
    def get_myscore(self):
        """
        Returns my scores
        """
        return self.myscore
    
    def get_yourscore(self):
        """
        Returns your scores
        """
        return self.yourscore
        
    def get_scores(self):
        """
        Returns current scores of each player
        """
        return (self.myscore, self.yourscore)



class Simulation(Base):
    
    def __init__(self, lst):
        """ 
        Initializes parameters 
        """
        self.lst = lst        # List used for the simulation
        self.init_lst = lst[:] # List to keep initial state of the list

        self.myscore = 0       
        self.yourscore = 0

        self.myturn = True
        self.trials = TRIALS   # Number of steps for the simulation

    def get_best_move(self):
        """ 
        Gets the best next move. 
        If this returns True, take number from left
        else take number fron right
        """
        result = self.simulation()
        if result:
            return True
        else:
            return False
            
    def trial(self):
        """
        Executes one attempt of simulation
        """ 
        while self.lst:
            rand_num = random.random()
            if rand_num < .5:
                self.get_left()
            else:
                self.get_right()

        if DEBUG:
            if self.get_myscore() > self.get_yourscore():
                print "I win.",
            else:
                print "You win.",
            print "scores =", self.get_scores()
                
    def simulation(self):
        """
        Executes simulation and returns the best next move
        if return True, take number from left
        else, take number fron right
        """

        left_result, right_result = 0, 0
        
        for trial_num in range(self.trials):

            if trial_num%100000 == 0:
                print "SIM TRIAL: ", trial_num, "DONE"

            # Start from left
            self.myturn = True
            self.get_left()
            
            # Run a simulation
            self.trial()
            
            # Get difference between myscore and yourscore
            diff = (self.get_myscore() - self.get_yourscore())
            if diff > 0:
                left_result += diff
            else:
                right_result -= diff

            if DEBUG:
                print "diff =", diff
                print "(left, right) = ", left_result, right_result
            
            # Initialize the list
            self.__init__(self.init_lst[:])

        if DEBUG:
            print "Points: (left, right) = ", left_result, right_result, "\n"

        if left_result >= right_result:
            return True
        else:
            return False


class Game(Base):

    def __init__(self, lst):
        self.lst = lst
        self.myscore = 0
        self.yourscore = 0
        self.myturn = True if random.random() < .5 else False

    def play(self):
        while self.lst:
            print "LIST - ", self.lst
            print ""

            if not PLAYER_MODE:
                if self.next_move(self.lst[:]):
                    self.get_left()
                else:
                    self.get_right()

            else:
                if self.myturn:
                    while True:
                        user_input = raw_input("Choose Left or Right (Type L/R): ")
                        if user_input  == 'L':
                            self.get_left()
                            break
                        elif user_input  == 'R':
                            self.get_right()
                            break
                        else:
                            print "Invalid input! Try again!"
                else:
                    if self.next_move(self.lst[:]):
                        self.get_left()
                    else:
                        self.get_right()

            
            print "(myscore, yourscore) =", self.get_scores(), "\n"

        if self.myscore > self.yourscore:
            print "You win!"
        elif self.myscore == self.yourscore:
            print "Tie!"
        else:
            print "You lose!"

    def next_move(self, lst):
        sim = Simulation(lst[:])
        return sim.get_best_move()

    def print_turn_info(self):
        if self.myturn:
            print "My turn",
        else:
            print "Your turn",
        print self.get_scores()
        print ""

if __name__ == "__main__":
    game = Game(GIVEN_LST)
    game.play()
