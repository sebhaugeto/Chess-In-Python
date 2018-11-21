import os
import copy
os.chdir("/Users/SebastianHaugeto/Google Drive/00_Indøk/Fag/03_ITGK/Øvinger/Øving 10/05_SJAKK")
from sjakk_classes import *

class Chess:
    def __init__(self):
        #intro 
        pass

    def play(self):
        play_board = Chessboard()
        statement = ""
        while play_board.play:
            clear_output()
            print()
            print(f"  {' '*play_board.space}{statement:^38}")
            play_board.print_board()
            move = play_board.user_input()
            piece,toPos = move
            toCol,toRow = toPos
            if toCol != "q" or toRow != "q":
            #Test for check
                test_board = copy.deepcopy(play_board)
                test_piece = copy.deepcopy(piece)
                #Update test board
                test_board.board[7-test_piece.position[1]][test_piece.position[0]] = " "
                test_board.board[7-toRow][toCol] = test_piece
                #Update test piece
                test_piece.position = (toCol,toRow)
                if isinstance(test_board.in_check(),King) and play_board.warnings < 1:
                    king = test_board.in_check()
                    if king.color == test_piece.color and test_piece.label == "king":
                        statement = f"Your king is checked at that position! \n              This is your last warning."
                        play_board.warnings += 1
                        continue
                    elif king.color == test_piece.color:
                        statement = "Your king is checked! This is your last warning."
                        play_board.warnings += 1
                        continue
                
            #If legal move:
                if piece.check(toPos,play_board):
                    play_board.warnings = 0
                    statement = ""
                    #Update board
                    play_board.board[7-piece.position[1]][piece.position[0]] = " "
                    play_board.board[7-toRow][toCol] = piece
                    #Update piece
                    piece.position = (toCol,toRow)
                    play_board.moves += 1
                    #If pawn reaches other side:
                    if isinstance(piece,Pawn):
                        piece = turn_queen(piece)
                    #Check for win
                    play_board.check_win()
                
            #If not legal move:
                elif not piece.check(toPos,play_board):
                    statement = (f"Not a legal move!")
        clear_output()

        #Results:
        play_board.print_board()
        print()
        if play_board.winner == "Black":
            print(f"{Color.BOLD}{Color.UNDERLINE}White player{Color.END} is victoriuos!")
            print("Congratulations! \(^O^)/")
            print(f"It took {play_board.moves} moves to finish the game.")

        elif play_board.winner == "White":
            print(f"{Color.BOLD}{Color.UNDERLINE}White player{Color.END} is victoriuos!")
            print("Congratulations! \(^O^)/")
            print(f"It took {play_board.moves} moves to finish the game.")

        print()
        print("Thanks for playing!")
        print("By @sebhaugeto")
        print()

game = Chess()
game.play()



