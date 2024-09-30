import random #import random module, could use this for easy and medium
from ..board_mechanics.player import Player # imports player class from the board_mechanics
from ..board_mechanics.board import Board # imports board class from board_mechanics
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, WHITE, BLACK, RED, GREEN, BLUE, GRAY, DARK_GRAY, PLAYER_BOARD_OFFSET_X, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, BUTTON_RECT, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE # imports various configuration values screen dimensions, colors, cell sizes, and font settings from config module
from ..ai.dialogue import easy_hit,easy_lose,easy_miss,easy_sink,easy_win,med_hit,med_lose,med_miss,med_sink,med_win,hard_hit,hard_lose,hard_sink,hard_win,hard_miss # imports dialogue options for different AI difficulty levels from ai.dialogue module

# defines an AI class that inherits from Player class, so it can function as a player in the game
class AI(Player): #initialize AI as a Player object so it can play like one
    def __init__(self, name: str, numberOfShips: int) -> None: # initializes AI with name and number of ships
        super().__init__(name, numberOfShips) # calls player class constructor to initialize AI attributes

    # defines attack pattern method for AI; this picks a random coordinate, used for easy and medium difficulty levels
    def attack_pattern(self, opponent_board: Board): # this attack pattern picks a random ship, used for easy + med
        valid_move = False # set flag for whether AI's move is valid
        while not valid_move: # continue until valid move is found
            x = random.randint(0, COLS - 1) # randomly pick a column within the board range
            y = random.randint(0, ROWS - 1) # randomly pick row within board range
            if not opponent_board.getTile(x, y).isHit(): # check if selected tile hasn't been hit yet
                valid_move = True # if valid, exit loop
        print(f"attack at {(chr(ord('A') + x)), y+1}") # output ai's attack coordinates in readable form
        return x, y # return selected coordinates for the attack

# define EasyAI class that inherits from AI class
class EasyAI(AI): # defines class 
    def __init__(self, numberOfShips: int) -> None: # initializes EasyAI
        super().__init__("Easy AI", numberOfShips) # calls AI constructor, naming it "Easy AI"
        # sets dialogue responses for different in-game events
        self.dialogue_hit = easy_hit # for easy ai hit 
        self.dialogue_miss = easy_miss # for easy ai miss
        self.dialogue_sink = easy_sink # for easy at sink 
        self.dialogue_win = easy_win # for easy ai win
        self.dialogue_lose = easy_lose # for easy ai loss
    
    # defines attack pattern method for EasyAI, using the parent class's attack pattern
    def attack_pattern(self, opponent_board: Board): # defines attack pattern method
        return super().attack_pattern(opponent_board) # Use the AI's random attack method

# defines MediumAI class that inherits from the AI class
class MediumAI(AI): # defines MediumAI class 
    def __init__(self, numberOfShips: int) -> None: # initialize MediumAI with set number of ships
        super().__init__("Medium AI", numberOfShips) # calls AI constructor, naming this AI "Medium AI"
        self.last_hits = None # stores last hits made by the AI for more strategic targeting
        # sets dialogue responses for different in-game events
        self.dialogue_hit = med_hit # for medium ai hit 
        self.dialogue_miss = med_miss # for medium ai miss
        self.dialogue_sink = med_sink # for medium ai sink 
        self.dialogue_win = med_win # for medium ai win 
        self.dialogue_lose = med_lose # for medium ai loss
    

    # defines more advanced attack pattern method, based on previous hits 
    def attack_pattern(self, opponent_board: Board): # defines medium ai attack pattern
        if self.last_hits: # if there are previous hits, attempt a targeted attack
            x, y, hit = self.last_hits[-1] # gets most recent hit 
            if len(self.last_hits) > 1: #if there's more than one hit, perform directional attack 
                x2, y2, hit2 = self.last_hits[-2] # gets second to last hit 
                newx = x # initializes new attack coordinates 
                newy = y # initializes new attack coordinates 
                walkRow = x2 == x # check if hits were in same row 
                backwards = not hit # reverse direction if last hit was a miss
                max_attempts = 10  # max number of attempts before giving up
                attempt = 0 # initialze attempt count
                while attempt < max_attempts: # try max number of attempts 
                    if backwards: # if going backward 
                        if walkRow: # if along the row 
                            newy = newy - 1 if y2 < y else newy + 1 # move to previous/next column
                        else: # if  along column 
                            newx = newx - 1 if x2 < x else newx + 1 # move to previous/next row
                    else: # going forward 
                        if walkRow: # if along the row 
                            newy = newy + 1 if y2 < y else newy - 1 # move to next/previous column
                        else: # if along column
                            newx = newx + 1 if x2 < x else newx - 1 # move to next/previous row
                    
                    if (0 <= newx < COLS and 0 <= newy < ROWS) and not opponent_board.getTile(newx, newy).isHit(): # check if new coordinates are valid and haven't been hit
                        print(f"attack at {(chr(ord('A') + newx)), newy+1}") # output ai's atttack coordinates 
                        return newx, newy # return new attack coordinates 
                    elif not (0 <= newx < COLS and 0 <= newy < ROWS): # if coords out of bounds 
                        backwards = not backwards # switch directions 
                    
                    attempt += 1 # increment attempt count 
                
                # If we've exhausted all attempts, fall back to random attack
                return super().attack_pattern(opponent_board)
            else: # if theres only one hit, try attacking adjacent tiles
                for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # checking orthogonal positions
                    newx, newy = x + i, y + j # calculate new coordinates 
                    if 0 <= newx < COLS and 0 <= newy < ROWS and not opponent_board.getTile(newx, newy).isHit(): # if position is valid and not already hit
                        print(f"attack at {(chr(ord('A') + newx)), newy+1}") # output ai's atttack coordinates
                        return newx, newy # return new attack coordinates
        return super().attack_pattern(opponent_board) # else default to normal attack pattern (random attack)
    
# defines HardAI class that inherits from the AI class  
class HardAI(AI): # defines hard ai 
    def __init__(self, numberOfShips: int, opponent_board: Board) -> None: # initialize HardAI with ships and opponent board
        super().__init__("AI-ham", numberOfShips) # Call the AI constructor, "AI-ham"
        self.known_targets = [] # stores locations that have ships in them
         # sets dialogue responses for different in-game events
        self.dialogue_hit = hard_hit # for hard ai hit 
        self.dialogue_miss = hard_miss # for har ai miss
        self.dialogue_sink = hard_sink # for hair ai sink 
        self.dialogue_win = hard_win # for hard ai win
        self.dialogue_lose = hard_lose # for hard ai loss
    
    # updates list of known target positions based on the opponent's board
    def update_targets(self, opponent_board: Board): # defines upadate_targets function
        self.known_targets = [] # clear known targets list
        for x in range(ROWS): #iterate through opponent board
            for y in range(COLS): # loop through all columns of opponent's board
                if opponent_board.getTile(x, y).getPiece(): # check if ship at location
                    self.known_targets.append((x, y)) # if so, add location to known targets

    # define the attack pattern for HardAI, prioritizing known targets
    def attack_pattern(self, opponent_board: Board): # define the attack pattern for HardAI
        for x, y in self.known_targets: # only iterates through known targets
            if not opponent_board.getTile(x, y).isHit(): # if position isn't hit yet
                print(f"attack at {(chr(ord('A') + x)), y+1}") # output ai's atttack coordinates 
                return x, y # return new attack coordinates
        
