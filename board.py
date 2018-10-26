        #!/usr/bin/python
import string
import os
import sys
import random
class Gameboard():
    '''This class creates the game boards and includes the majority of gameplay functions'''
    def __init__(self, navy, player = True):
        '''self.player changes how the bard is printed, so the player doesn't see the enemy ships
        self.column and self.row can be changed to any size, but may cause issue it there are more
        columns than letter in the alphabet'''
        self.navy = navy
        self.letters = string.ascii_uppercase
        self.player = player
        self.columns = 10
        self.rows = 10
        self.row = list(' |' * self.columns)
        self.board = []
        for times in range(self.rows):
            self.board.append(self.row[:])
        self.possible_spaces = []
        for letter in self.letters[:self.columns]:
            for num in range(self.rows):
                self.possible_spaces.append(f'{letter}{str(num+1)}')
    def coor_to_loc(self, coordinates):
        '''This function returns the original typed location, based on a coordinate'''
        return f'{self.letters[int(coordinates[0]/2)]}{coordinates[1]+1}'
    def set_navy_locations(self):
        '''This is here because Navy() is unaware of the board (though I could have passed it as a parameter'''
        for ship in self.navy.ships:
            for coor in ship.get_coordinates():
                ship.set_location(self.coor_to_loc(coor))
    def is_valid_location(self, location):
        '''Check that the location is an available space'''
        if location in self.possible_spaces:
            return True
        elif location == '':
            return None
        else:
            print(f'{location} is not a valid location.')
            return False


    def is_valid_direction(self, coordinates, direction, ship_length):
        '''Check that with these coordinate and orientation, that the ship will stay on the board'''
        if direction == '':
            return None
        if direction in [ 'V', 'v', 'Vertical', 'vertical']:
            if coordinates[1] + ship_length-1 < self.rows:
                return True
            else:
                return False 
        if direction in ['h', 'H', 'horizontal', 'Horizontal']:
            if coordinates[0] + (ship_length-1)*2 <= (self.columns-1)*2:
                return True
            else:
                return False 
        else:
            print('Invalid Direction.')
            return False

    def get_coordinates(self, location):
        '''Takes a location (a5, e10, etc...) and converts it to a coordinate.
        Check for the first characters index in self.letters, then multiply by two to account for the |'s
        take the remaining characters as an integer, but decrement by one to it aligns with the array properly.'''
        self.coordinates = []
        if len(location) == 3:
            self.coordinates.append(self.letters.index(location[0])*2)
            num = int(''.join(location[1:]))
            self.coordinates.append(num-1)
        else:
            for coordinate in location:
                if coordinate in self.letters:
                    self.coordinates.append(self.letters.index(coordinate)*2)
                if coordinate.isdigit() and int(coordinate) in list(range(self.rows+1)):
                    self.coordinates.append(int(coordinate)-1)
        return self.coordinates
    
    def get_board(self):
        '''Prints board when called. Determines which board is being printed and calls corresponding get_ships() function.'''
        index = 1
        print(f'{("|".join(list(self.letters[0:self.columns]))+"|").rjust(self.columns+25)}')
        for x in self.board:
            row = f'{str(index)} '
            if self.player:
                self.get_ships()
            else:
                self.get_oppo_ships()
            for y in x:
                row = row + y
            print(row.rjust(self.columns+25))
            index += 1
    
    def get_ships(self):
        '''Adds X's and O's for the players ships on their board.'''
        for coor in self.navy.ship_coordinates():
            self.board[coor[1]][coor[0]] = self.navy.get_ship_at_coordinate(coor).get_status()[f'{coor}']

    def get_oppo_ships(self):
        '''Only prints X's where computer's ships have been hit, omits spaces that have not been discovered by the player. '''
        for coor in self.navy.ship_coordinates():
            if self.navy.get_ship_at_coordinate(coor).get_status()[f'{coor}'] == 'X':
                self.board[coor[1]][coor[0]] = 'X' #opponent_navy.get_ship_at_coordinate(coor).get_status()[f'{coor}']

    def place_ship(self, ship):
        '''Used to place a player ship.
        checks that all input are valid locations, will fit on the board and doesn't cross any other ships.
        If these checks pass, it appends those coordinates to the ship and then reprints the board with the new ship on it '''
        length = ship.get_length()
        location = ''
        direction = '' 
        coordinates = [0,0]
        space_clear = []
        while (False in space_clear) or (not self.is_valid_location(location) ) or (not self.is_valid_direction(coordinates, direction, ship.get_length())):
            location = ''
            direction = ''
            space_clear = []
            while (len(location) < 2) or (not self.is_valid_location(location)):
                location = input(f'Where would you like to place the end of the {ship.get_ship().ship_name}? ').upper()
            coordinates = self.get_coordinates(location)
            while direction not in ['H', 'V']:
                direction = input(f'Place the {ship.get_ship().ship_name} (H)orizontal or (V)ertical? ').upper() 
            clear_screen()
            if not self.is_valid_direction(coordinates, direction, ship.get_length()):
                clear_screen()
                print('Ship placed off board.')
                self.get_board()
            if (self.is_valid_location(location) ) and (self.is_valid_direction(coordinates, direction, ship.get_length())): 
                ship_coordinates = []
                for pos in range(length):
                    if direction in ['h', 'H', 'horizontal', 'Horizontal']:
                        ship_coordinates.append([coordinates[0]+2*pos,coordinates[1]])
                    if direction in [ 'V', 'v', 'Vertical', 'vertical']:
                        ship_coordinates.append([coordinates[0],coordinates[1]+(pos)])
                for coor in ship_coordinates:
                    if coor in self.navy.ship_coordinates():
                        print(f'That space is occupied by the {navy.get_ship_at_coordinate(coor).ship_name}.')
                        self.get_board()
                        space_clear.append(False)
            else:
                continue
                        
                
        ship.add_coordinate(ship_coordinates)
        self.get_board() 

    def miss(self,coordinates):
        '''This shows where the player targeted but missed on the game board.
        When editing game board 2d array, y-axis comes first because each row is an element.'''
            self.board[coordinates[1]][coordinates[0]] = 'O'

class Ship():
    '''This class defines all of the ships in game, plus their attributes.'''
    def __init__(self, name):
        self.status = {}
        self.ship_name = name
        self.coordinates = []
        self.location = []
        self.length = 0
        if self.ship_name == "Destroyer":
            self.length = 2
        elif self.ship_name == 'Cruiser':
            self.length = 3
        elif self.ship_name == 'Submarine':
            self.length = 3
        elif self.ship_name == 'Battleship':
            self.length = 4
        elif self.ship_name == 'Aircraft Carrier':
            self.length = 5
        self.health = self.length 

    def get_ship(self):
        return self
    def get_length(self):
        return self.length
    def set_damage(self, coordinates):
        '''Checks to see if this location was already hit, if not sets it to damaeged and calls get_damage() to see if it sank'''
        if self.status[f'{coordinates}'] == 'X':
            print('Already Hit.')
        else:
            self.status[f'{coordinates}'] = 'X'
            self.health -= 1
            self.get_damage()
    def add_coordinate(self, coordinates):
        '''Take coordinates list and associates them with this ship.'''
        for coor in coordinates:
            self.coordinates.append(coor)
            self.status[f'{coor}'] = 'O'
    def set_location(self, loc):
        self.location.append(loc)
    def get_location(self):
        return self.location
    def get_coordinates(self):
        return self.coordinates
    def get_status(self):
        return self.status
    def has_sunk(self):
        if self.health == 0:
            return True
        else:
            return False
    def get_damage(self):
        if self.health == 0:
            print(f'{self.get_ship().ship_name} has sunk.')
        else:
            return self.health

class Navy():
    '''Holds all the ship objects'''
    def __init__(self):
        self.ships = []
        self.ships.append(Ship('Destroyer'))
        self.ships.append(Ship('Cruiser'))
        self.ships.append(Ship('Submarine'))
        self.ships.append(Ship('Battleship'))
        self.ships.append(Ship('Aircraft Carrier'))
    def is_navy_sunk(self):
        '''Win condition check, if all ships are sunk after any turn then game over'''
        ships = []
        for ship in self.ships:
            ships.append(ship.has_sunk())
        if False in ships:
            return False
        else:
            return True

    def describe_navy(self):
        '''Provides status output for the navy, only used by player to see their ships and statuses'''
        for ship in self.ships:
            if ship.has_sunk():
                print(f'{ship.ship_name} has sunk.')
                print()
            else:
                print(ship.ship_name)
                print('Health: '+ str(ship.get_damage()) + '/' + str(ship.get_length()))
                print(f'Location: {ship.get_location()}')
                #print(ship.get_status().values())))
                print()
    def get_ship_at_coordinate(self, coordinates):
        '''Uses ship_coordinates() to retrieve a list of all the ships coordinates and then returns a particular ship
        at a specific coordinate'''
        for ship in self.ships:
            if coordinates in ship.get_coordinates():
                return ship.get_ship()
    def ship_coordinates(self):
        '''Makes a list of all coordinates currently filled by ships.'''
        all_ship_coordinates = []
        for ship in self.ships:
            for coor in ship.get_coordinates():
                all_ship_coordinates.append(coor)
        return all_ship_coordinates
    def place_navy(self, gameboard):
        '''This function automatically places all the ships in the navy.
        Used to place the computer's ships. Uses the same logic as the player ship placement function.
        Could be added as an option for the player. '''
        available = gameboard.possible_spaces
        HV = ['H', 'V']
        for ship in self.ships:
            loc = ''
            dir = ''
            coor = []
            space_clear = []
            while not gameboard.is_valid_location(loc) or not gameboard.is_valid_direction(coor, dir, ship.get_length()) or False in space_clear:
                space_clear = []
                loc = random.choice(available)
                coor = gameboard.get_coordinates(loc)
                dir = random.choice(HV)
                ship_coordinates = []
                for pos in range(ship.get_length()):
                    if dir in ['h', 'H', 'horizontal', 'Horizontal']:
                        ship_coordinates.append([coor[0]+2*pos,coor[1]])
                    if dir in [ 'V', 'v', 'Vertical', 'vertical']:
                        ship_coordinates.append([coor[0],coor[1]+(pos)])
                for coord in ship_coordinates:
                    if coord in self.ship_coordinates():
                        #print(f'That space is occupied by the {self.get_ship_at_coordinate(coord).ship_name}.')
                        space_clear.append(False)

            ship.add_coordinate(ship_coordinates)

class Opponent():
    '''Computer opponent object. Initializes the computers Navy and Board. Take mode as a value to choose difficulty/strategy'''
    def __init__(self, mode):
        self.navy = Navy()
        self.mode = mode
        self.board = Gameboard(self.navy, player = False)
        self.navy.place_navy(self.board)
        self.board.set_navy_locations()
        self.available_moves = self.board.possible_spaces.copy()
        self.made_moves = []
        self.next_moves = []

    def get_surrounding(self, location):
        '''This method returns a list of valid locations surrounding a sucessful hit by the computer. '''
        hit_loc = location
        hit_letter = hit_loc[0][0]
        hit_num = int(str(hit_loc[0][1:]))
        letter_index = self.board.letters.index(hit_letter)
        prev_letter = self.board.letters[letter_index-1]
        next_letter = self.board.letters[letter_index+1]
        surroundings = []
        surroundings.append(f'{prev_letter}{hit_num}')
        surroundings.append(f'{hit_letter}{hit_num+1}')
        surroundings.append(f'{next_letter}{hit_num}')
        surroundings.append(f'{hit_letter}{hit_num-1}')
        return surroundings

    def computer_move(self, player_navy):
        if self.mode == 'Easy':
            '''If set to easy, the computer just fires at random, marking off the locations as it goes.'''
            move = random.choice(self.available_moves)
            self.available_moves.pop(self.available_moves.index(move))
            self.made_moves.append(move)
            print(f'\nComputer fired at {move}.')
            coordinates = self.board.get_coordinates(move)
            if player_navy.get_ship_at_coordinate(coordinates):
                print('Hit!')
                player_navy.get_ship_at_coordinate(coordinates).set_damage(coordinates)
            else:
                print('Miss.')
        elif self.mode == 'Hard':
            '''When set to hard, the computer starts by randomly hunting, but when it hits something it builds a list of 
            surrounding targets and first at those before resuming the search.'''
            move = random.choice(self.available_moves)
            if self.made_moves and self.made_moves[-1][1] == 'Hit':
                surroundings = self.get_surrounding(self.made_moves[-1])
                for move in surroundings:
                    if move in self.available_moves and move not in self.next_moves:
                        self.next_moves.append(move)
            if self.next_moves:
                move = self.next_moves.pop()

            self.available_moves.pop(self.available_moves.index(move))
            print(f'\nComputer fired at {move}.')
            coordinates = self.board.get_coordinates(move)
            if player_navy.get_ship_at_coordinate(coordinates):
                print('Hit!')
                player_navy.get_ship_at_coordinate(coordinates).set_damage(coordinates)
                self.made_moves.append([move, 'Hit'])
            else:
                print('Miss.')
                self.made_moves.append([move, 'Miss'])


def clear_screen():
    os.system('clear')

def main():
    '''Game set up. Set difficulty, create user Navy and Board, place ships.'''
    clear_screen()
    difficulty = ''
    while difficulty not in ['H', 'E', 'HARD', 'EASY']:
        difficulty = input('Please enter difficulty, (E)asy or (H)ard. ').upper()
    if difficulty in ['H', 'HARD']:
        computer = Opponent('Hard')
    else:
        computer = Opponent('Easy')
    navy = Navy()
    board = Gameboard(navy)
    computer.board.get_board()
    for ship in navy.ships:
        board.place_ship(ship)
    board.set_navy_locations()
    while True:
        '''Main Loop. Takes a location to fire on. checks if it is on option, then fires. 
        then it allows the computer a turn, finally checks if either navy has sunk, if not reprints target board.'''
        loc = ''
        while loc in ['S', 'O'] or not computer.board.is_valid_location(loc):
            loc = input('Fire at which location?\n'
                        '- Press \'s\' for Status\n'
                        '- Press \'o\' for Opponent board\n' 
                        '- Press \'q\' to Quit.\n').upper()
            if loc == 'O':
                computer.board.get_board()
                continue
            if loc == 'Q':
                sys.exit('Thanks for playing.')
            if loc == 'S':
                clear_screen()
                navy.describe_navy()
                board.get_board()
                #opponent_navy.describe_navy()
                print("Press 'O' to see opponent board.")
                continue
        coordinates = computer.board.get_coordinates(loc)
        clear_screen()
        print(f'You fired at {loc}.')
        if computer.navy.get_ship_at_coordinate(coordinates):
            print('Hit!')
            computer.navy.get_ship_at_coordinate(coordinates).set_damage(coordinates)
        else:
            print('Miss.')
            computer.board.miss(coordinates)
        computer.computer_move(navy)
        if computer.navy.is_navy_sunk():
            clear_screen()
            computer.board.get_board()
            print('You Win!')
            sys.exit('Thanks for playing.')
        if navy.is_navy_sunk():
            clear_screen()
            board.get_board()
            print('You Lose!')
            sys.exit('Thanks for playing.')
        computer.board.get_board()

if __name__ == '__main__':
    main()
