#!/usr/bin/python
import string
import os
class Gameboard():
    def __init__(self):
        self.letters = string.ascii_uppercase
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
    
    def is_valid_location(self, location):
        if location in self.possible_spaces:
            return True
        elif location == '':
            return None
        else:
            print(f'{location} is not a valid location.')
            return False


    def is_valid_direction(self, coordinates, direction, ship_length):
        if direction == '':
            return None
        if direction in [ 'V', 'v', 'Vertical', 'vertical']:
            if coordinates[0] + ship_length-1 < self.rows:
                return True
            else:
                return False 
        if direction in ['h', 'H', 'horizontal', 'Horizontal']:
            if coordinates[1] + (ship_length-1)*2 <= (self.columns-1)*2:
                return True
            else:
                return False 
        else:
            print('Invalid Direction.')
            return False

    def get_coordinates(self, location):
        self.coordinates = []
        for coordinate in location:
            if coordinate in self.letters:
                self.coordinates.append(self.letters.index(coordinate)*2)
            if coordinate.isdigit() and int(coordinate) in list(range(self.rows+1)):
                self.coordinates.insert(0,int(coordinate)-1)
        return self.coordinates
    
    def get_board(self):
        index = 1
        print(f'{("|".join(list(self.letters[0:self.columns]))+"|").rjust(self.columns+25)}')
        for x in self.board:
            row = f'{str(index)} '
            self.get_ships()
            for y in x:
                row = row + y
            print(row.rjust(self.columns+25))
            index += 1
    
    def get_ships(self):
        for coor in navy.ship_coordinates():
            self.board[coor[0]][coor[1]] = navy.get_ship_at_coordinate(coor).get_status()[f'{coor}']
    
    def place_ship(self, ship):
        length = ship.get_length()
        location = ''
        direction = '' 
        coordinates = [0,0]
        space_clear = []
        while (False in space_clear) or (not self.is_valid_location(location) ) or (not self.is_valid_direction(coordinates, direction, ship.get_length())): 
            space_clear = []
            while len(location) < 2:
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
                    if direction in [ 'V', 'v', 'Vertical', 'vertical']:
                        ship_coordinates.append([coordinates[0]+pos,coordinates[1]])
                    if direction in ['h', 'H', 'horizontal', 'Horizontal']:
                        ship_coordinates.append([coordinates[0],coordinates[1]+(pos*2)])
                for coor in ship_coordinates:
                    if coor in navy.ship_coordinates():
                        print(f'That space is occupied by the {navy.get_ship_at_coordinate(coor).ship_name}.')
                        self.get_board()
                        space_clear.append(False)
            else:
                continue
                        
                
        ship.add_coordinate(ship_coordinates)
        self.get_board() 

    def place_x(self,coordinates):
        for coor in coordinates:
            self.board[coor[0]][coor[1]*2] = 'O'

class Ship():
    def __init__(self, name):
        self.status = {}
        self.ship_name = name
        self.coordinates = []
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
        if self.status[f'{coordinates}'] == 'X':
            print('Already Hit.')
        else:
            self.status[f'{coordinates}'] = 'X'
            self.health -= 1
            self.get_damage()
    def add_coordinate(self, coordinates):
        for coor in coordinates:
            self.coordinates.append(coor)
            self.status[f'{coor}'] = 'O'
    def get_coordinates(self):
        return self.coordinates
    def get_status(self):
        return self.status
    def has_sunk(self):
        if self.health == 0:
            return True
    def get_damage(self):
        if self.health == 0:
            print(f'{self.get_ship().ship_name} has sunk.')
        else:
            return self.health

class Navy():
    def __init__(self):
        self.ships = []
        self.ships.append(Ship('Destroyer'))
        self.ships.append(Ship('Cruiser'))
        self.ships.append(Ship('Submarine'))
        self.ships.append(Ship('Battleship'))
        self.ships.append(Ship('Aircraft Carrier'))
    def describe_navy(self):
        for ship in self.ships:
            if ship.has_sunk():
                print(f'{ship.ship_name} has sunk.')
                print()
            else:
                print(ship.ship_name)
                print('Coordinates: '+ str(ship.get_coordinates()))
                print('Health: '+ str(ship.get_damage()) + '/' + str(ship.get_length()))
                print(list(ship.get_status().values()))
                print()
    def get_ship_at_coordinate(self, coordinates):
        for ship in self.ships:
            if coordinates in ship.get_coordinates():
                return ship.get_ship()
    def ship_coordinates(self):
        all_ship_coordinates = []
        for ship in self.ships:
            for coor in ship.get_coordinates():
                all_ship_coordinates.append(coor)
        return all_ship_coordinates

def clear_screen():
    os.system('clear')

clear_screen()
board = Gameboard()
navy = Navy()
board.get_board()
for ship in navy.ships:
    board.place_ship(ship)
while True:
    loc = input('Fire at which location? (Press \'s\' for Status) ').upper()
    if loc == 'Q':
        break
    if loc == 'S':
        clear_screen()
        navy.describe_navy()
        board.get_board()
        continue
    coordinates = board.get_coordinates(loc)
    clear_screen()
    if navy.get_ship_at_coordinate(coordinates):
        print('Hit!')
        navy.get_ship_at_coordinate(coordinates).set_damage(coordinates)
    else:
        print('Miss.')
    board.get_board()
