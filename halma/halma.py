# Python Standard Library imports
import sys
import time
import math
import random

# Custom module imports
from board import Board
from tile import Tile
from menu import Menu


class Halma():


    def __init__(self, b_size=8, t_limit=60, c_player=Tile.P_RED):
        self.menu = Menu()
        self.menu.mainloop()

        dificulty = self.menu.difficulty

        if dificulty == "easy":
            self.ply_depth = 1
            self.ab_enabled = False
            self.ai_player = False
        elif dificulty == "medium":
            self.ply_depth = 3
            self.ab_enabled = True
            self.ai_player = False
        elif dificulty == "hard":
            self.ply_depth = 5
            self.ab_enabled = True
            self.ai_player = False
        elif dificulty == "multi":
            c_player = None
            self.ab_enabled = False
            self.ply_depth = 'None'
            self.ai_player = False
        elif dificulty == "ai_vs_ai":
            self.ply_depth = 1
            self.ai_player = True
            pass
            ## Insert Parameters for AI vs AI
        
        
        # TODO: Create an AI vs AI mode
        # TODO: Create a more advanced AI through different evaluation functions and successor functions
        
        self.menu.destroy()


        # Create initial board
        board = [[None] * b_size for _ in range(b_size)]
        for row in range(b_size):
            for col in range(b_size):

                if row + col < 4:
                    element = Tile(2, 2, 0, row, col)
                elif row + col > 2 * (b_size - 3):
                    element = Tile(1, 1, 0, row, col)
                else:
                    element = Tile(0, 0, 0, row, col)

                board[row][col] = element

        

        # Save member variables
        self.b_size = b_size
        if self.ai_player == True:
            pass
        else:
            self.ai_player = False
        self.current_player = Tile.P_GREEN
        self.t_limit = t_limit
        self.c_player = c_player
        self.board_view = Board(board)
        self.board = board
        self.selected_tile = None
        self.valid_moves = []
        self.computing = False
        self.total_plies = 0
        self.ab_enabled = True
        self.is_game_over = False

        self.r_goals = [t for row in board
                        for t in row if t.tile == Tile.T_RED]
        self.g_goals = [t for row in board
                        for t in row if t.tile == Tile.T_GREEN]

        self.board_view.set_status_color("#757575" if
            self.current_player == Tile.P_RED else "#757575")
        

        if self.ai_player == True:
                    self.play()
        elif self.c_player == self.current_player:
            self.execute_computer_move()
        


        self.board_view.add_click_handler(self.tile_clicked)
        self.board_view.draw_tiles(board=self.board)  # Refresh the board

        # Print initial program info
        print("Halma Solver Basic Information")
        print("==============================")
        print("AI opponent enabled:", "no" if self.c_player is None else "yes")
        print("A-B pruning enabled:", "yes" if self.ab_enabled else "no")
        print("Turn time limit:", self.t_limit)
        print("Max ply depth:", self.ply_depth)
        print()

        self.board_view.mainloop()  # Begin tkinter main loop

    def tile_clicked(self, row, col):

        if self.computing:  # Block clicks while computing
            return

        new_tile = self.board[row][col]

        # If we are selecting a friendly piece
        if new_tile.piece == self.current_player:

            self.outline_tiles(None)  # Reset outlines

            # Outline the new and valid move tiles
            new_tile.outline = Tile.O_MOVED
            self.valid_moves = self.get_moves_at_tile(new_tile,
                self.current_player)
            self.outline_tiles(self.valid_moves)

            # Update status and save the new tile
            self.board_view.set_status("Tile `" + str(new_tile) + "` selected")
            self.selected_tile = new_tile

            self.board_view.draw_tiles(board=self.board)  # Refresh the board

        # If we already had a piece selected and we are moving a piece
        elif self.selected_tile and new_tile in self.valid_moves:

            self.outline_tiles(None)  # Reset outlines
            self.move_piece(self.selected_tile, new_tile)  # Move the piece

            # Update status and reset tracking variables
            self.selected_tile = None
            self.valid_moves = []
            self.current_player = (Tile.P_RED
                if self.current_player == Tile.P_GREEN else Tile.P_GREEN)

            self.board_view.draw_tiles(board=self.board)  # Refresh the board

            # If there is a winner to the game
            winner = self.find_winner()
            if winner:
                self.board_view.set_status("The " + ("blue"
                    if winner == Tile.P_GREEN else "yellow") + " player has won!")
                self.current_player = None

            elif self.c_player is not None:
                self.execute_computer_move()

        else:
            self.board_view.set_status("Invalid move attempted")

    def minimax(self, depth, player_to_max, max_time, a=float("-inf"),
                b=float("inf"), maxing=True, prunes=0, boards=0):

        # Bottomed out base case
        if depth == 0 or self.find_winner() or time.time() > max_time:
            return self.utility_distance(player_to_max), None, prunes, boards

        # Setup initial variables and find moves
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_next_moves((Tile.P_RED
                    if player_to_max == Tile.P_GREEN else Tile.P_GREEN))

        # For each move
        for move in moves:
            for to in move["to"]:

                # Bail out when we're out of time
                if time.time() > max_time:
                    return best_val, best_move, prunes, boards

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = Tile.P_NONE
                to.piece = piece
                boards += 1

                # Recursively call self
                val, _, new_prunes, new_boards = self.minimax(depth - 1,
                    player_to_max, max_time, a, b, not maxing, prunes, boards)
                prunes = new_prunes
                boards = new_boards

                # Move the piece back
                to.piece = Tile.P_NONE
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    a = max(a, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    b = min(b, val)

                if self.ab_enabled and b <= a:
                    return best_val, best_move, prunes + 1, boards

        return best_val, best_move, prunes, boards
    
    #def play(self):
    #    counter = 0
    #    while not self.is_game_over == True:
    #        if counter % 2 == 0:
    #            self.execute_computer_move_ai_vs_ai()
    #        else:
    #            self.execute_computer_move()
    #        counter += 1
    def play(self):
        counter = 0
        while not self.is_game_over == True:
            if counter % 2 == 0:
                self.execute_computer_move_ai_vs_ai()
            else:
                self.execute_computer_move()
            counter += 1
            print(counter)
    

    def execute_computer_move(self):

        # Print out search information
        current_turn = (self.total_plies // 2) + 1
        print("Turn", current_turn, "Computation")
        print("=================" + ("=" * len(str(current_turn))))
        print("Executing search ...", end=" ")
        sys.stdout.flush()

        # self.board_view.set_status("Computing next move...")
        self.computing = True
        self.board_view.update()
        max_time = time.time() + self.t_limit

        # Execute minimax search
        start = time.time()
        _, move, prunes, boards = self.minimax(self.ply_depth,
            self.c_player, max_time)
        end = time.time()

        # Print search result stats
        print("complete")
        print("Time to compute:", round(end - start, 4))
        print("Total boards generated:", boards)
        print("Total prune events:", prunes)

        # Move the resulting piece
        self.outline_tiles(None)  # Reset outlines
        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]
        self.move_piece(move_from, move_to)

        self.board_view.draw_tiles(board=self.board)  # Refresh the board

        winner = self.find_winner()
        if winner:
            self.board_view.set_status("The " + ("blue"
                if winner == Tile.P_GREEN else "yellow") + " player has won!")
            self.board_view.set_status_color("#212121")
            self.current_player = None
            self.current_player = None

            print()
            print("Final Stats")
            print("===========")
            print("Final winner:", "blue"
                if winner == Tile.P_GREEN else "yellow")
            print("Total # of plies:", self.total_plies)

        else:  # Toggle the current player
            self.current_player = (Tile.P_RED
                if self.current_player == Tile.P_GREEN else Tile.P_GREEN)

        self.computing = False
        print()
    
    def execute_computer_move_ai_vs_ai(self):
    # determine the current player
        #counter = 0
        #if counter % 2 == 0:
        #    self.current_player = Tile.P_GREEN
        #else:
        #    self.current_player = Tile.P_RED
        #counter += 1
        if self.is_game_over == False:
            if self.current_player == Tile.P_GREEN:
                self.c_player = Tile.P_GREEN
            else:
                self.c_player = Tile.P_RED
        # Print out search information
            current_turn = (self.total_plies // 2) + 1
            print("Turn", current_turn, "Computation")
            print("=================" + ("=" * len(str(current_turn))))
            print("Executing search ...", end=" ")
            sys.stdout.flush()

            self.ply_depth = random.randint(1, 3)

            # self.board_view.set_status("Computing next move...")
            self.computing = True
            self.board_view.update()
            max_time = time.time() + self.t_limit

            # Execute minimax search
            start = time.time()
            _, move, prunes, boards = self.minimax(self.ply_depth,
                self.c_player, max_time)
            end = time.time()

            # Print search result stats
            print("complete")
            print("Time to compute:", round(end - start, 4))
            print("Total boards generated:", boards)
            print("Total prune events:", prunes)

            # Move the resulting piece
            try:
                self.outline_tiles(None)  # Reset outlines
                move_from = self.board[move[0][0]][move[0][1]]
                move_to = self.board[move[1][0]][move[1][1]]
                self.move_piece(move_from, move_to)
            except:
                pass

            self.board_view.draw_tiles(board=self.board)  # Refresh the board

            winner = self.find_winner()
            if winner:
                self.board_view.set_status("The " + ("blue"
                    if winner == Tile.P_GREEN else "yellow") + " player has won!")
                self.board_view.set_status_color("#212121")
                self.current_player = None
                self.current_player = None

                print()
                print("Final Stats")
                print("===========")
                print("Final winner:", "blue"
                    if winner == Tile.P_GREEN else "yellow")
                print("Total # of plies:", self.total_plies)
                self.is_game_over = True
            else:
                pass
                # recursively call play() to continue the game
                #self.current_player = self.c_player
                #self.play()
        else:
            print("Game is over")



    def get_next_moves(self, player=1):

        moves = []  # All possible moves
        for col in range(self.b_size):
            for row in range(self.b_size):

                curr_tile = self.board[row][col]

                # Skip board elements that are not the current player
                if curr_tile.piece != player:
                    continue

                move = {
                    "from": curr_tile,
                    "to": self.get_moves_at_tile(curr_tile, player)
                }
                moves.append(move)

        return moves

    def get_moves_at_tile(self, tile, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = tile.loc[0]
        col = tile.loc[1]

        # List of valid tile types to move to
        valid_tiles = [Tile.T_NONE, Tile.T_GREEN, Tile.T_RED]
        if tile.tile != player:
            valid_tiles.remove(player)  # Moving back into your own goal
        if tile.tile != Tile.T_NONE and tile.tile != player:
            valid_tiles.remove(Tile.T_NONE)  # Moving out of the enemy's goal

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent tiles

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                # Handle moves out of/in to goals
                new_tile = self.board[new_row][new_col]
                if new_tile.tile not in valid_tiles:
                    continue

                if new_tile.piece == Tile.P_NONE:
                    if adj:  # Don't consider adjacent on subsequent calls
                        moves.append(new_tile)
                    continue

                # Check jump tiles

                new_row = new_row + row_delta
                new_col = new_col + col_delta

                # Skip checking degenerate values
                if (new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                # Handle returning moves and moves out of/in to goals
                new_tile = self.board[new_row][new_col]
                if new_tile in moves or (new_tile.tile not in valid_tiles):
                    continue

                if new_tile.piece == Tile.P_NONE:
                    moves.insert(0, new_tile)  # Prioritize jumps
                    self.get_moves_at_tile(new_tile, player, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):
    

        # Handle trying to move a non-existant piece and moving into a piece
        if from_tile.piece == Tile.P_NONE or to_tile.piece != Tile.P_NONE:
            self.board_view.set_status("Invalid move")
            return

        # Move piece
        to_tile.piece = from_tile.piece
        from_tile.piece = Tile.P_NONE

        # Update outline
        to_tile.outline = Tile.O_MOVED
        from_tile.outline = Tile.O_MOVED

        self.total_plies += 1

        self.board_view.set_status_color("#757575" if
            self.current_player == Tile.P_RED else "#757575")
        self.board_view.set_status("Piece moved from `" + str(from_tile) +
            "` to `" + str(to_tile) + "`, " + ("blue's" if
            self.current_player == Tile.P_RED else "yellow's") + " turn...")

    def find_winner(self):

        if all(g.piece == Tile.P_GREEN for g in self.r_goals):
            return Tile.P_GREEN
        elif all(g.piece == Tile.P_RED for g in self.g_goals):
            return Tile.P_RED
        else:
            return None

    def outline_tiles(self, tiles=[], outline_type=Tile.O_SELECT):

        if tiles is None:
            tiles = [j for i in self.board for j in i]
            outline_type = Tile.O_NONE

        for tile in tiles:
            tile.outline = outline_type

    def utility_distance(self, player):

        def point_distance(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0

        for col in range(self.b_size):
            for row in range(self.b_size):

                tile = self.board[row][col]

                if tile.piece == Tile.P_GREEN:
                    distances = [point_distance(tile.loc, g.loc) for g in
                                 self.r_goals if g.piece != Tile.P_GREEN]
                    value -= max(distances) if len(distances) else -50

                elif tile.piece == Tile.P_RED:
                    distances = [point_distance(tile.loc, g.loc) for g in
                                 self.g_goals if g.piece != Tile.P_RED]
                    value += max(distances) if len(distances) else -50

        if player == Tile.P_RED:
            value *= -1

        return value


if __name__ == "__main__":

    halma = Halma()
