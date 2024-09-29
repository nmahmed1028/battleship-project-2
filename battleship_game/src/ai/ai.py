import random #could use this for easy and medium
from ..board_mechanics.player import Player
from ..board_mechanics.board import Board
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, WHITE, BLACK, RED, GREEN, BLUE, GRAY, DARK_GRAY, PLAYER_BOARD_OFFSET_X, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, BUTTON_RECT, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE
from ..ai.dialogue import easy_hit,easy_lose,easy_miss,easy_sink,easy_win,med_hit,med_lose,med_miss,med_sink,med_win,hard_hit,hard_lose,hard_sink,hard_win

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
        self.dialogue_hit = easy_hit
        self.dialogue_miss = easy_miss
        self.dialoge_sink = easy_sink
        self.dialogue_win = easy_win
        self.dialogue_lose = easy_lose
    
    def attack_pattern(self, opponent_board: Board):
        return super().attack_pattern(opponent_board)


class MediumAI(AI):
    def __init__(self, numberOfShips: int) -> None:
        super().__init__("Medium AI", numberOfShips)
        self.last_hits = None
        self.dialogue_hit = med_hit
        self.dialogue_miss = med_miss
        self.dialoge_sink = med_sink
        self.dialogue_win = med_win
        self.dialogue_lose = med_lose
    
    def attack_pattern(self, opponent_board: Board):
        if self.last_hits: #if 
            x, y, hit = self.last_hits[-1]
            if len(self.last_hits) > 1: #if there's more than one hit
                x2, y2, hit2 = self.last_hits[-2]
                newx = x
                newy = y
                walkRow = x2 == x
                backwards = not hit
                max_attempts = 10  # Maximum number of attempts before giving up
                attempt = 0
                while attempt < max_attempts:
                    if backwards:
                        if walkRow:
                            newy = newy - 1 if y2 < y else newy + 1
                        else:
                            newx = newx - 1 if x2 < x else newx + 1
                    else: 
                        if walkRow:
                            newy = newy + 1 if y2 < y else newy - 1
                        else:
                            newx = newx + 1 if x2 < x else newx - 1
                    
                    if (0 <= newx < COLS and 0 <= newy < ROWS) and not opponent_board.getTile(newx, newy).isHit():
                        print(f"attack at {(chr(ord('A') + newx)), newy+1}")
                        return newx, newy
                    elif not (0 <= newx < COLS and 0 <= newy < ROWS):
                        backwards = not backwards
                    
                    attempt += 1
                
                # If we've exhausted all attempts, fall back to random attack
                return super().attack_pattern(opponent_board)
            else:
                for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #checking orthogonal positions
                    newx, newy = x + i, y + j
                    if 0 <= newx < COLS and 0 <= newy < ROWS and not opponent_board.getTile(newx, newy).isHit(): #if position is valid and not already hit
                        print(f"attack at {(chr(ord('A') + newx)), newy+1}")
                        return newx, newy
        return super().attack_pattern(opponent_board) #else default to normal attack pattern (random attack)
    
class HardAI(AI):
    def __init__(self, numberOfShips: int, opponent_board: Board) -> None:
        super().__init__("AI-ham", numberOfShips)
        self.known_targets = [] #stores locations that have ships in them
        self.dialogue_hit = hard_hit
        self.dialogue_sink = hard_sink
        self.dialogue_win = hard_win
        self.dialogue_lose = hard_lose
    
    def update_targets(self, opponent_board: Board):
        self.known_targets = []
        for x in range(ROWS): #iterate through opponent board
            for y in range(COLS):
                if opponent_board.getTile(x, y).getPiece(): #check if ship at location
                    self.known_targets.append((x, y)) #if so, add location to known targets

    def attack_pattern(self, opponent_board: Board):
        for x, y in self.known_targets: #only iterates through known targets
            if not opponent_board.getTile(x, y).isHit(): #if position isn't hit yet
                print(f"attack at {(chr(ord('A') + x)), y+1}")
                return x, y
        
