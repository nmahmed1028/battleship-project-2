import random #could use this for easy and medium
from game_mechanics import attack, place_ships

class AI:
    def __init__(self, difficulty) -> None:
        self.difficulty = difficulty.lower()
        #initialize AI's player board (place ships randomly but legally)

    def difficulty_level(self, player_board): #takes in player's ship board for hard difficulty
        if self.difficulty == "easy":
            #select random square and attack
            pass
        elif self.difficulty == "medium":
            #same as easy but check if it hit something
            #if it did then attack in orthogonally adjacent spaces to find other hits
            pass
        elif self.difficulty == "hard":
            #picks a player ship and hits it
            #attacks same ship till sunk then moves to another one
            #might be easier to go in order of smallest to biggest 
            pass
        else:
            raise ValueError("Invalid input")