#!/usr/bin/python
import string
class Gameboard():
    def __init__(self):
        self.letters = string.ascii_uppercase
        self.columns = 5
        self.rows = 5
        self.row = list('O' * self.columns)
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
        else:
            print(f'{location} is not a valid location.')
            return False


    def is_valid_direction(self, coordinates, direction, ship_length):
        if direction in [ 'V', 'v', 'Vertical', 'vertical']:
            if coordinates[0] + ship_length-1 < self.columns:
                return True
            else:
                print(f'X-Coordinate {coordinates[0]+ship_length} is off the board.')
                return False 
        if direction in ['h', 'H', 'horizontal', 'Horizontal']:
            if coordinates[1] + ship_length-1 < self.rows:
                return True
            else:
                print(f'Y-Coordinate {coordinates[0]+ship_length} is off the board.')
                return False 
        else:
            print('Invalid Direction.')
            return False

    def get_coordinates(self, location):
        self.coordinates = []
        for coordinate in location:
            if coordinate in self.letters:
                self.coordinates.append(self.letters.index(coordinate))
            if coordinate.isdigit() and int(coordinate) in list(range(self.rows+1)):
                self.coordinates.insert(0,int(coordinate)-1)
        return self.coordinates
    
    def get_board(self):
        index = 1
        print(f'{self.letters[0:self.columns].rjust(self.columns+4)}')
        for x in self.board:
            row = f'{str(index)} '
            for y in x:
                row = row + y
            print(row.rjust(self.columns+4))
            index += 1
    
    def place_ship(self, ship):
        length = ship.get_length()
        location = input(f'Where would you like to place the end of the {ship.get_ship()}? ').upper()
        
        while not self.is_valid_location(location):
            location = input(f'Where would you like to place the end of the {ship.get_ship()}? ').upper()
        
            while not self.is_valid_direction(coordinates, direction, ship.get_length()):
                 direction = input(f'Place the {ship.get_ship()} (H)orizontal or (V)ertical? ') 
        coordinates = self.get_coordinates(location)
        direction = input(f'Place the {ship.get_ship()} (H)orizontal or (V)ertical? ') 
        
        
        print(coordinates)
        print('Placement is good.')
        for pos in range(length):
            if direction == 'V':
                self.place_x([coordinates[0]+pos,coordinates[1]])
            if direction == 'H':
                self.place_x([coordinates[0],coordinates[1]+pos])
        self.get_board()

    def place_x(self,coordinates):
        print(coordinates)
        self.board[coordinates[0]][coordinates[1]] = 'X'

class Ship():
    def __init__(self, length):
        self.length = length
        self.status = []
        for x in range(length):
            self.status.append('S')
        if self.length == 2:
            self.ship_name = "Destroyer"
        elif self.length == 3:
            self.ship_name = 'Cruiser'
        elif self.length == 4:
            self.ship_name = 'Battleship'
        elif self.length == 5:
            self.ship_name = 'Aircraft Carrier'
    def get_ship(self):
        return self.ship_name
    def get_length(self):
        return self.length
    def set_damage(self, position):
        self.status[position] = 'X'
    def get_damage(self):
        damaged = self.status.count('X')
        print(f'{self.get_ship()} {self.status}\nDamage: {damaged}/{self.length}')
        if damaged == self.length:
            print(f'{self.get_ship()} has sunk.')


class Navy():
    def __init__(self):
        self.ships = []
        self.ships.append(Ship(2))
        self.ships.append(Ship(3))
        self.ships.append(Ship(4))
    def describe_navy(self):
        for ship in self.ships:
            ship.get_damage()

board = Gameboard()
navy = Navy()
navy.describe_navy()
for ship in navy.ships:
    board.place_ship(ship)
navy.ships[1].set_damage(1)

navy.ships[1].set_damage(2)
navy.describe_navy()

while 1:
    loc = input('Input a spot on the board. ').upper()
    while not board.is_valid_location(loc):
        print('Location does not exist.')
        loc = input('Input a spot on the board. ').upper()
    board.place_x(board.get_coordinates(loc))
    board.get_board()
#board.place_ship(ships[0])
