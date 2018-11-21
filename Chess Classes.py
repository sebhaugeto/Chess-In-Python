#!/usr/bin/env python
"""
Contains all classes necessary for the chess game.
#x in code = x-axis in visual representation
#0,1,2,3,4,5,6,7
#y in code = y-axis in visual representation
#0,1,2,3,4,5,6,7
"""

__author__ = '@sebhaugeto' #Check me out on Instagram!

import pickle
import random

class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def clear_output():
    for i in range(30):
        print()

def turn_queen(pawn):
        col,row = pawn.position
        if pawn.color == "white" and row == 7:
            return Queen(col,row,'white')
        elif pawn.color == "black" and row == 0:
            return Queen(col,row,'black')
        else:
            return pawn

class Chessboard:
    def __init__(self):       
        color1 = "white"
        color2 = "black"
        self.board = [
        [Rook(0,7,color2), Knight(1,7,color2), Bishop(2,7,color2), Queen(3,7,color2), King(4,7,color2), Bishop(5,7,color2), Knight(6,7,color2), Rook(7,7,color2)],
        [Pawn(0,6,color2), Pawn(1,6,color2), Pawn(2,6,color2), Pawn(3,6,color2), Pawn(4,6,color2), Pawn(5,6,color2), Pawn(6,6,color2), Pawn(7,6,color2)],
        [" "]*8,
        [" "]*8,
        [" "]*8,
        [" "]*8,
        [Pawn(0,1,color1), Pawn(1,1,color1), Pawn(2,1,color1), Pawn(3,1,color1), Pawn(4,1,color1), Pawn(5,1,color1), Pawn(6,1,color1), Pawn(7,1,color1)],
        [Rook(0,0,color1), Knight(1,0,color1), Bishop(2,0,color1), Queen(3,0,color1), King(4,0,color1), Bishop(5,0,color1), Knight(6,0,color1), Rook(7,0,color1)],
        ]
        #white = 0 and black = 1
        self.killed = [[],[]]
        self.space = 5
        self.play = True
        self.winner = ""
        self.moves = 0
        self.warnings = 0
    
    def print_board(self):
        s = self.space
        print()
        print(f"{' '*s}      a   b   c   d   e   f   g   h ")
        print(f"{' '*s}    {'-'*33} {' '*s} {' '.join([n.symbol for n in self.killed[1]])}")
        for i in range(8):
            print(f"{' '*s}  {abs(i-8)} | {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]} | {self.board[i][3]} | {self.board[i][4]} | {self.board[i][5]} | {self.board[i][6]} | {self.board[i][7]} |  {abs(i-8)}")
            print(f"{' '*s}    {'-'*33} ")
        print(f"{' '*s}      a   b   c   d   e   f   g   h {' '*s}   {' '.join([n.symbol for n in self.killed[0]])}")
        print()
    
    def in_check(self):
        kings = []
        for row in self.board:
            for piece in row:
                if isinstance(piece,King):
                    kings.append(piece)
        for king in kings:      
            col,row = king.position
            #Check for enemies horizontally (right and left Way)
            for W in [(1,0),(-1,7)]:
                for column in range(col+W[0],(7-W[1]),W[0]):
                    piece = self.board[7-row][column]
                    if piece == " ":
                        continue
                    elif piece.label in ["rook","queen"] and piece.color != king.color:
                        return king
                    #If not right enemy piece or empty tile:
                    else:
                        break
            #Check for enemies vertically (up and down Way):
            for W in [(1,0),(-1,7)]:
                for myrow in range(row+W[0],(7-W[1]),W[0]):
                    piece = self.board[7-myrow][col]
                    if piece == " ":
                        continue
                    elif piece.label in ["rook","queen"] and piece.color != king.color:
                        return king
                    #If not right enemy piece or empty tile:
                    else:
                        break
            #Check for horses (up and down + left and right):
            for up_down in [1,-1]:
                for left_right in [2,-2]:
                    if 0 < 7-row + up_down < 8 and 0 < col + left_right < 7:
                        piece = self.board[7-row + up_down][col + left_right]
                        if piece == " ":
                            continue
                        elif piece.label == "knight" and piece.color != king.color:
                            return king
            for up_down in [2,-2]:
                for left_right in [1,-1]:
                    if 0 < 7-row + up_down < 8 and 0 < col + left_right < 7:
                        piece = self.board[7-row + up_down][col + left_right]
                        if piece == " ":
                            continue
                        elif piece.label == "knight" and piece.color != king.color:
                            return king

            #Check diagonally:
            for up_down in [(0,1),(7,-1)]:
                for right_left in [1,-1]:
                    #print(f"kingrow: {row} kingcol: {col}")
                    myrow = row
                    for mycol in range(col+right_left,(7-up_down[0]),up_down[1]):
                        myrow += up_down[1]
                        if 0 < 7-myrow < 8 and 0 < mycol < 8:
                            piece = self.board[7-myrow][mycol]
                            #If pawn or king:
                            if piece == " ":
                                    continue
                            elif piece.label in ["pawn","king"] and piece.color != king.color:
                                if piece.color == "white" and piece.label == "pawn" and myrow - row == 1:
                                    return king
                                elif piece.color == "black" and piece.label == "pawn" and row - myrow == 1:
                                    return king
                                elif piece.label == "king" and abs(myrow-row) == 1:
                                    return king
                            #If bishop or queen
                            elif piece.label in ["bishop","queen"] and piece.color != king.color:
                                return king
                        #If not right enemy piece or empty tile:
                        else:
                            break
        return None
       
    def check_win(self):
        for i in [0,1]:
            for piece in self.killed[i]:
                if piece.label == "king" and piece.color == "white":
                    self.play = False
                    self.winner = "Black"
                elif piece.label == "king" and piece.color == "black":
                    self.play = False
                    self.winner = "White"

    def user_input(self):
        print("              'l' = load, 'q' = quit")
        print()
        s = self.space
        
        switch = True
        switch2 = True
        while switch:
            piece = input("Choose your piece: ")
            try:
                if len(piece) == 2 and piece[0] in ["a","b","c","d","e","f","g","h"] and int(piece[1]) in range(1,9):
                    fromCol = ord(piece[0])-ord("a")
                    fromRow = int(piece[1]) - 1
                    if self.board[7-fromRow][fromCol] == " ":
                        print(f"There's no piece at {piece}! ")
                        continue
                    else:
                        piece = self.board[7-fromRow][fromCol]
                        switch = False
                #Load a board
                if piece == "l":
                    try:
                        with open("saved_chess", "rb") as f:
                            print()
                            print(f"  {' '*s}{'Previous board opened!':^38}")
                            self.board = pickle.load(f)
                            self.killed = pickle.load(f)
                            self.moves= pickle.load(f)
                            self.print_board()
                    except FileNotFoundError:
                        print("No saved board!")
                
                #If user wants to quit
                elif piece == "q":
                    switch = False
                    switch2 = False
                    self.play = False
            
            except FileNotFoundError:
                print("No saved board in memory!")
            except:
                print("Invalid input.")
    
        while switch2:
            pos = input(f"Move {Color.BOLD} {piece.color} {piece.label} {Color.END} {piece.symbol} to: ")
            try:
                if len(pos) == 2 and pos[0] in ["a","b","c","d","e","f","g","h"] and int(pos[1]) in range(1,9):
                    fromCol = ord(pos[0]) - ord('a')
                    fromRow = int(pos[1]) - 1
                    pos = (fromCol,fromRow)
                    switch2 = False
                #Load a board
                elif pos == "l":
                    try:
                        with open("saved_chess", "rb") as f:
                            print()
                            print(f"  {' '*s}{'Previous board opened!':^38}")
                            self.board = pickle.load(f)
                            self.killed = pickle.load(f)
                            self.moves = pickle.load(f)
                            self.print_board()
                    except FileNotFoundError:
                        pass
                elif pos == "q":
                        switch2 = False
                        self.play = False

            except FileNotFoundError:
                print("No saved board in memory! ")
            except:
                print("Invalid Input! ")

        #Auto-save board after each round
        with open("saved_chess","wb") as f:
            pickle.dump(self.board,f)
            pickle.dump(self.killed,f)
            pickle.dump(self.moves,f)

        if not self.play:
            return ["q",["q","q"]]
        else:
            return [piece,pos]
        
class Pawn:
    def __init__(self,col,row,color):
        self.position = (col,row)
        self.label = "pawn"
        if color == "white":
            self.symbol = "♟"
            self.color = "white"
            self.index = 0
        elif color == "black":
            self.symbol = "♙"
            self.color = "black"
            self.index = 1

    def __str__(self):
        return self.symbol

    def check(self,move_to,chessboard):
        fromCol,fromRow = self.position
        toCol,toRow = move_to
        target = chessboard.board[7-toRow][toCol]
        #print(".check:")
        #print(fromCol,fromRow)
        #printt(toCol,toRow)
        #If white and move is down
        if self.color == "white" and fromRow > toRow:
            return False
        #If black and move is up
        elif self.color == "black" and fromRow < toRow:
            return False
        #If enemey to the right or left
        elif abs(toCol - fromCol) == 1 and abs(toRow - fromRow) == 1:
            if target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
        #If in the starting position
        elif abs(toRow - fromRow) == 2 and toCol == fromCol and target == ' ':
            if fromRow == 1 and self.color == "white":
                return True
            elif fromRow == 6 and self.color == "black":
                return True
        #If not in the starting position
        elif abs(toRow - fromRow) == 1 and toCol == fromCol and target == ' ':
            return True
        #If invalid input
        else:
            return False

class Rook:
    def __init__(self,col,row,color):
        self.position = (col,row)
        self.label = "rook"
        if color == "white":
            self.symbol = "♜"
            self.color = "white"
            self.index = 0
        elif color == "black":
            self.symbol = "♖"
            self.color = "black"
            self.index = 1

    def __str__(self):
        return self.symbol

    def check(self,move_to,chessboard):
        fromCol,fromRow = self.position
        toCol,toRow = move_to
        target = chessboard.board[7-toRow][toCol]
        #print(".check:")
        #print(fromCol,fromRow)
        #printt(toCol,toRow)
        if fromCol == toCol and fromRow == toRow: 
            return False
        #Collision detection, horizontally:
        #Move right
        if fromRow == toRow:
            if fromCol < toCol:
                #Check if clear path up until the end position
                for i in range(fromCol+1,toCol,1):
                    if chessboard.board[7-toRow][i] != " ":
                        return False
        #Move left
            elif fromCol > toCol:
                #Check if clear path up until the end position
                for i in range(fromCol-1,toCol,-1):
                    if chessboard.board[7-toRow][i] != " ":
                        return False
            
            if target != " " and target.color != self.color:
                chessboard.killed[1-self.index].append(target)
                return True
            elif target == " ":
                return True
        #Collision detection, vertically:
        #Move up
        elif fromCol == toCol:
            if fromRow < toRow:
                #Check if clear path up until the end position
                for i in range(fromRow+1,toRow,1):
                    if chessboard.board[7-i][toCol] != " ":
                        return False
                    verti_clear_path = True
        #Move down
            elif fromRow > toRow:
                #Check if clear path up until the end position
                for i in range(fromRow-1,toRow,-1):
                    if chessboard.board[7-i][toCol] != " ":
                        return False
                    verti_clear_path = True
            
            if target != " " and target.color != self.color:
                chessboard.killed[1-self.index].append(target)
                return True
            elif target == " ":
                return True
        else:
            return False

class Queen:
    def __init__(self,x,y,color):
        self.position = (x,y)
        self.label = "queen"
        if color == "white":
            self.symbol = "♛"
            self.color = "white"
            self.index = 0
        elif color == "black":
            self.symbol = "♕"
            self.color = "black"
            self.index = 1

    def __str__(self):
        return self.symbol

    def check(self,move_to,chessboard):
        fromCol,fromRow = self.position
        toCol,toRow = move_to
        target = chessboard.board[7-toRow][toCol]
        if fromCol == toCol and fromRow == toRow: 
            return False
        #Collision detection, horizontally:
        #Move right
        if fromRow == toRow:
            if fromCol < toCol:
                #Check if clear path up until the end position
                for i in range(fromCol+1,toCol,1):
                    if chessboard.board[7-toRow][i] != " ":
                        return False
        #Move left
            elif fromCol > toCol:
                #Check if clear path up until the end position
                for i in range(fromCol-1,toCol,-1):
                    if chessboard.board[7-toRow][i] != " ":
                        return False
            
            if target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
            elif target == " ":
                return True
        #Collision detection, vertically:
        #Move up
        elif fromCol == toCol:
            if fromRow < toRow:
                #Check if clear path up until the end position
                for i in range(fromRow+1,toRow,1):
                    if chessboard.board[7-i][toCol] != " ":
                        return False
            #Move down
            elif fromRow > toCol:
                #Check if clear path up until the end position
                for i in range(fromRow-1,toRow,-1):
                    if chessboard.board[7-i][toCol] != " ":
                        return False
            
            if target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
            elif target == " ":
                return True

        #Collision detection, diagonally. Formula 1: 45 deg. Formula 2: 135 deg.
        if fromRow - fromCol == toRow - toCol or fromRow + fromCol == toRow + toCol:
            #'Up-diagonals'
            if fromRow < toRow:
                if fromCol < toCol:
                    row = fromRow      
                    for col in range(fromCol+1,toCol):
                        row += 1
                        if chessboard.board[7-row][col] != " ":
                            return False
                elif fromCol > toCol:
                    row = fromRow
                    for col in range(fromCol-1,toCol,-1):
                        row += 1
                        if chessboard.board[7-row][col] != " ":
                            return False     
            #'Down-diagonals'
            if fromRow > toRow:
                if fromCol < toCol:
                    row = fromRow      
                    for col in range(fromCol+1,toCol):
                        row -= 1
                        if chessboard.board[7-row][col] != " ":
                            return False
                elif fromCol > toCol:
                    row = fromRow
                    for col in range(fromCol-1,toCol,-1):
                        row -= 1
                        if chessboard.board[7-row][col] != " ":
                            return False    

            #If free path and end position contains piece
            if target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
            elif target == " ":
                return True 
        #Not a valid queen move
        else:
            return False

class King:
    def __init__(self,x,y,color):
        self.position = (x,y)
        self.label = "king"
        if color == "white":
            self.symbol = '♚'
            self.color = "white"
            self.index = 0
        elif color == "black":
            self.symbol = '♔'
            self.color = "black"
            self.index = 1

    def __str__(self):
        return self.symbol

    def check(self,move_to,chessboard):
        fromCol,fromRow = self.position
        toCol,toRow = move_to
        target = chessboard.board[7-toRow][toCol]
        #print(".check:")
        #print(fromCol,fromRow)
        #printt(toCol,toRow)
        if fromCol == toCol and fromRow == toRow:
            return False
        
        #Check horizontally and vertically
        if abs(toCol - fromCol) == 1 or abs(toRow - fromRow) == 1:
            if target == " ":
                return True
            elif target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
        #Check diagonally
        elif abs(fromCol - toCol) == 1 and abs(fromRow - toRow) == 1:
            if target == " ":
                return True
            elif target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
        else:
            return False

class Knight:
    def __init__(self,x,y,color):
        self.position = (x,y)
        self.label = "knight"
        if color == "white":
            self.symbol = '♞'
            self.color = "white"
            self.index = 0
        elif color == "black":
            self.symbol = '♘'
            self.color = "black"
            self.index = 1

    def __str__(self):
        return self.symbol

    def check(self,move_to,chessboard):
        fromCol,fromRow = self.position
        toCol,toRow = move_to
        target = chessboard.board[7-toRow][toCol]
        #print(".check:")
        #print(xo,yo)
        #print(x,y)
        if target == " ":
            if abs(fromRow - toRow) == 2 and abs(fromCol - toCol) == 1:
                return True
            if abs(fromRow - toRow) == 1 and abs(fromCol - toCol) == 2:
                return True
        elif target != " ":
            if abs(fromRow - toRow) == 2 and abs(fromCol - toCol) == 1 and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
            if abs(fromRow - toRow) == 1 and abs(fromCol - toCol) == 2 and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
        
        else:
            return False

class Bishop:
    def __init__(self,x,y,color):
        self.position = (x,y)
        self.label = "bishop"
        if color == "white":
            self.symbol = '♝'
            self.color = "white"
            self.index = 0
        elif color == "black":
            self.symbol = '♗'
            self.color = "black"
            self.index = 1

    def __str__(self):
        return self.symbol

    def check(self,move_to,chessboard):
        fromCol,fromRow = self.position
        toCol,toRow = move_to
        target = chessboard.board[7-toRow][toCol]
        #print(".check:")
        #print(xo,yo)
        #print(x,y)
        #Collision detection, diagonally. Formula 1: 45 deg. Formula 2: 135 deg.
        if fromRow - fromCol == toRow - toCol or fromRow + fromCol == toRow + toCol:
            #'Up-diagonals'
            if fromRow < toRow:
                if fromCol < toCol:
                    row = fromRow      
                    for col in range(fromCol+1,toCol):
                        row += 1
                        if chessboard.board[7-row][col] != " ":
                            return False
                elif fromCol > toCol:
                    row = fromRow
                    for col in range(fromCol-1,toCol,-1):
                        row += 1
                        if chessboard.board[7-row][col] != " ":
                            return False     
            #'Down-diagonals'
            if fromRow > toRow:
                if fromCol < toCol:
                    row = fromRow      
                    for col in range(fromCol+1,toCol):
                        row -= 1
                        if chessboard.board[7-row][col] != " ":
                            return False
                elif fromCol > toCol:
                    row = fromRow
                    for col in range(fromCol-1,toCol,-1):
                        row -= 1
                        if chessboard.board[7-row][col] != " ":
                            return False    
            #If free path and end position contains piece
            if target != " " and target.color != self.color:
                chessboard.killed[self.index].append(target)
                return True
            elif target == " ":
                return True 
        
        #Not a valid queen move
        else:
            return False
