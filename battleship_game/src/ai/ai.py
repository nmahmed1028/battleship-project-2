import random #could use this for easy and medium
from ..board_mechanics.player import Player
from ..board_mechanics.board import Board
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, WHITE, BLACK, RED, GREEN, BLUE, GRAY, DARK_GRAY, PLAYER_BOARD_OFFSET_X, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, BUTTON_RECT, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE

class AI(Player): #initialize AI as a Player object so it can play like one
    def __init__(self, name: str, numberOfShips: int) -> None:
        super().__init__(name, numberOfShips)

    def attack_pattern(self, opponent_board: Board): #this attack pattern picks a random ship, used for easy + med
        valid_move = False
        while not valid_move:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if not opponent_board.getTile(x, y).isHit():
                valid_move = True
        print(f"attack at {(chr(ord('A') + x)), y+1}")
        return x, y

    '''def difficulty_level(self, player_board): #takes in player's ship board for hard difficulty
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
            raise ValueError("Invalid input")'''
    

class EasyAI(AI):
    def __init__(self, numberOfShips: int) -> None:
        super().__init__("Easy AI", numberOfShips)
    
    def attack_pattern(self, opponent_board: Board):
        return super().attack_pattern(opponent_board)


class MediumAI(AI):
    def __init__(self, numberOfShips: int) -> None:
        super().__init__("Medium AI", numberOfShips)
        self.last_hits = None
    
    def attack_pattern(self, opponent_board: Board):
        if self.last_hits: #if 
            x, y = self.last_hits[-1]
            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #checking orthogonal positions
                newx, newy = x + i, y + j
                if 0 <= newx < COLS and 0 <= newy < ROWS and not opponent_board.getTile(newx, newy).isHit(): #if position is valid and not already hit
                    print(f"attack at {newx, newy}")
                    return newx, newy
        return super().attack_pattern(opponent_board) #else default to normal attack pattern (random attack)
    
class HardAI(AI):
    def __init__(self, numberOfShips: int, opponent_board: Board) -> None:
        super().__init__("AI-ham", numberOfShips)
        self.known_targets = [] #stores locations that have ships in them

        for x in range(ROWS): #iterate through opponent board
            for y in range(COLS):
                if opponent_board.getTile(x, y).getPiece(): #check if ship at location
                    self.known_targets.append((x, y)) #if so, add location to known targets
    
    def attack_pattern(self, opponent_board: Board):
        for x, y in self.known_targets: #only iterates through known targets
            if not opponent_board.getTile(x, y).isHit(): #if position isn't hit yet
                print(f"attack at {(chr(ord('A') + x)), y+1}")
                return x, y
        
