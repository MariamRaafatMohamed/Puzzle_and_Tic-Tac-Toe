import customtkinter as ctk
from tkinter import messagebox
import heapq
import time
import copy
import random

class PuzzleSolver:
    def __init__(self, initial_state):
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.initial_state = initial_state

    def manhattan_distance(self, state):
        distance = 0
        for i in range(9):
            if state[i] == 0:
                continue
            goal_pos = state[i] - 1 if state[i] != 0 else 8
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def get_neighbors(self, state):
        neighbors = []
        zero_idx = state.index(0)
        row, col = divmod(zero_idx, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append(new_state)
        return neighbors

    def a_star(self):
        start_time = time.time()
        open_set = []
        heapq.heappush(open_set, (0 + self.manhattan_distance(self.initial_state), 0, self.initial_state, []))
        closed_set = set()
        while open_set:
            _, moves, state, path = heapq.heappop(open_set)
            state_tuple = tuple(state)
            if state == self.goal_state:
                end_time = time.time()
                return path + [state], moves, end_time - start_time
            if state_tuple in closed_set:
                continue
            closed_set.add(state_tuple)
            for neighbor in self.get_neighbors(state):
                neighbor_tuple = tuple(neighbor)
                if neighbor_tuple in closed_set:
                    continue
                g = moves + 1
                h = self.manhattan_distance(neighbor)
                f = g + h
                heapq.heappush(open_set, (f, g, neighbor, path + [state]))
        end_time = time.time()
        return None, 0, end_time - start_time


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        self.root.geometry("400x500")
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.initial_state = self.generate_solvable_state()
        self.current_state = self.initial_state[:]
        self.solver = PuzzleSolver(self.current_state)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.solution = None
        self.current_step = 0
        self.manual_moves = 0
        self.solving = False

        # Main grid
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Puzzle grid
        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.pack(pady=10)

        for i in range(3):
            for j in range(3):
                value = self.current_state[i * 3 + j]
                text = str(value) if value != 0 else " "
                button = ctk.CTkButton(self.grid_frame, text=text, font=('Arial', 24), width=80, height=80,
                                       fg_color=("#3A7EBF", "#1F538D"),
                                       command=lambda row=i, col=j: self.click_tile(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.solve_button = ctk.CTkButton(self.button_frame, text="Solve", font=('Arial', 14),
                                          command=self.start_solving)
        self.solve_button.grid(row=0, column=0, padx=5)

        self.home_button = ctk.CTkButton(self.button_frame, text="Back", font=('Arial', 14),
                                         fg_color="gray30", hover_color="gray25", command=self.go_to_home)
        self.home_button.grid(row=0, column=1, padx=5)

        # Stats labels
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self.stats_frame.pack(pady=10)

        self.moves_label = ctk.CTkLabel(self.stats_frame, text="Moves: 0", font=('Arial', 12))
        self.moves_label.grid(row=0, column=0, padx=10)

        self.time_label = ctk.CTkLabel(self.stats_frame, text="Time: 0.0000s", font=('Arial', 12))
        self.time_label.grid(row=0, column=1, padx=10)

        # End game frame
        self.end_game_frame = ctk.CTkFrame(self.main_frame)
        self.end_game_frame.pack(pady=10)

    def generate_solvable_state(self):
        while True:
            state = list(range(9))
            random.shuffle(state)
            inversions = 0
            for i in range(9):
                for j in range(i + 1, 9):
                    if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                        inversions += 1
            if inversions % 2 == 0:
                return state

    def click_tile(self, row, col):
        if self.solving:
            return
        zero_idx = self.current_state.index(0)
        zero_row, zero_col = divmod(zero_idx, 3)
        if (abs(row - zero_row) + abs(col - zero_col)) == 1:
            clicked_idx = row * 3 + col
            self.current_state[zero_idx], self.current_state[clicked_idx] = self.current_state[clicked_idx], \
                self.current_state[zero_idx]
            self.manual_moves += 1
            self.update_board()
            if self.current_state == self.goal_state:
                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {self.manual_moves} moves!")
                self.solving = True
                self.solve_button.configure(state="disabled")
                self.show_end_game_buttons()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                value = self.current_state[i * 3 + j]
                text = str(value) if value != 0 else " "
                self.buttons[i][j].configure(text=text)

    def start_solving(self):
        if self.solving:
            return
        self.solving = True
        self.solve_button.configure(state="disabled")
        self.solver = PuzzleSolver(self.current_state)
        self.solution, moves, solve_time = self.solver.a_star()
        if self.solution is None:
            messagebox.showinfo("Result", "No solution found!")
            self.solving = False
            self.solve_button.configure(state="normal")
            return
        self.moves_label.configure(text=f"Moves: {moves}")
        self.time_label.configure(text=f"Time: {solve_time:.4f}s")
        self.current_step = 0
        self.animate_solution()

    def animate_solution(self):
        if self.current_step >= len(self.solution):
            messagebox.showinfo("Result", "Puzzle solved by AI!")
            self.show_end_game_buttons()
            return
        self.current_state = self.solution[self.current_step][:]
        self.update_board()
        self.current_step += 1
        self.root.after(500, self.animate_solution)

    def show_end_game_buttons(self):
        for widget in self.end_game_frame.winfo_children():
            widget.destroy()

        end_label = ctk.CTkLabel(
            self.end_game_frame,
            text="Game Over! What would you like to do?",
            font=('Arial', 12)
        )
        end_label.pack(pady=5)

        play_again_btn = ctk.CTkButton(
            self.end_game_frame,
            text="Play Again",
            font=('Arial', 14),
            fg_color="green",
            hover_color="darkgreen",
            command=self.reset_game
        )
        play_again_btn.pack(pady=5)

    def go_to_home(self):
        self.root.destroy()
        new_root = ctk.CTk()
        app = GameMenu(new_root)
        new_root.mainloop()

    def reset_game(self):
        self.initial_state = self.generate_solvable_state()
        self.current_state = self.initial_state[:]
        self.solver = PuzzleSolver(self.current_state)
        self.solution = None
        self.current_step = 0
        self.manual_moves = 0
        self.solving = False
        self.solve_button.configure(state="normal")
        for widget in self.end_game_frame.winfo_children():
            widget.destroy()
        self.moves_label.configure(text="Moves: 0")
        self.time_label.configure(text="Time: 0.0000s")
        self.update_board()


# Tic-Tac-Toe Game Logic Class
class TicTacToeGame:
    def __init__(self):
        self.board = [" " for _ in range(9)]

    def check_winner(self, player):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == player for i in combo) for combo in win_combinations)

    def is_board_full(self):
        return " " not in self.board

    def minimax(self, board, is_maximizing):
        if self.check_winner("O"): return 1
        if self.check_winner("X"): return -1
        if self.is_board_full(): return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def best_move(self):
        best_score = -float("inf")
        move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        if move is not None:
            self.board[move] = "O"
        return move

    def make_move(self, index, player):
        if self.board[index] == " ":
            self.board[index] = player
            return True
        return False

    def reset(self):
        self.board = [" " for _ in range(9)]


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (AI vs You)")
        self.root.geometry("400x500")
        self.game = TicTacToeGame()
        self.buttons = []
        self.x_color = "#FF5555"
        self.o_color = "#5555FF"

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.pack(pady=10)

        for i in range(9):
            btn = ctk.CTkButton(self.grid_frame, text=" ", font=('Arial', 24), width=80, height=80,
                                fg_color=("#3A7EBF", "#1F538D"), command=lambda i=i: self.on_click(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.home_button = ctk.CTkButton(self.button_frame, text="Back", font=('Arial', 14),
                                         fg_color="gray30", hover_color="gray25", command=self.go_to_home)
        self.home_button.pack(padx=5)

        self.end_game_frame = ctk.CTkFrame(self.main_frame)
        self.end_game_frame.pack(pady=10)

    def on_click(self, i):
        if self.game.make_move(i, "X"):
            self.buttons[i].configure(text="X", text_color=self.x_color)
            self.buttons[i].configure(state="disabled")
            if not self.check_game_over():
                ai_move = self.game.best_move()
                if ai_move is not None:
                    self.buttons[ai_move].configure(text="O", text_color=self.o_color)
                    self.buttons[ai_move].configure(state="disabled")
                    self.check_game_over()

    def check_game_over(self):
        if self.game.check_winner("X"):
            messagebox.showinfo("Game Over", "You win!")
            self.disable_all()
            self.show_end_game_buttons()
            return True
        elif self.game.check_winner("O"):
            messagebox.showinfo("Game Over", "AI wins!")
            self.disable_all()
            self.show_end_game_buttons()
            return True
        elif self.game.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw.")
            self.disable_all()
            self.show_end_game_buttons()
            return True
        return False

    def show_end_game_buttons(self):
        for widget in self.end_game_frame.winfo_children():
            widget.destroy()

        end_label = ctk.CTkLabel(
            self.end_game_frame,
            text="Game Over! What would you like to do?",
            font=('Arial', 12)
        )
        end_label.pack(pady=5)

        play_again_btn = ctk.CTkButton(
            self.end_game_frame,
            text="Play Again",
            font=('Arial', 14),
            fg_color="green",
            hover_color="darkgreen",
            command=self.reset_game
        )
        play_again_btn.pack(pady=5)

    def go_to_home(self):
        self.root.destroy()
        new_root = ctk.CTk()
        app = GameMenu(new_root)
        new_root.mainloop()

    def disable_all(self):
        for btn in self.buttons:
            btn.configure(state="disabled")

    def reset_game(self):
        self.game.reset()
        for btn in self.buttons:
            btn.configure(text=" ", state="normal", text_color="white")
        for widget in self.end_game_frame.winfo_children():
            widget.destroy()

class GameMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Selection")
        self.root.geometry("300x300")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.main_frame, text="Choose a Game", font=('Arial', 20))
        self.label.pack(pady=20)

        self.puzzle_btn = ctk.CTkButton(self.main_frame, text="8-Puzzle", font=('Arial', 16), width=200,
                                        command=self.start_puzzle)
        self.puzzle_btn.pack(pady=10)

        self.tictactoe_btn = ctk.CTkButton(self.main_frame, text="Tic-Tac-Toe", font=('Arial', 16), width=200,
                                           command=self.start_tictactoe)
        self.tictactoe_btn.pack(pady=10)

        # Theme toggle
        self.theme_frame = ctk.CTkFrame(self.main_frame)
        self.theme_frame.pack(pady=10)

        self.theme_label = ctk.CTkLabel(self.theme_frame, text="Theme:", font=('Arial', 12))
        self.theme_label.pack(side="left", padx=5)

        self.theme_switch = ctk.CTkSwitch(
            self.theme_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(side="left", padx=5)

        # Set initial theme
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

    def toggle_theme(self):
        theme = self.theme_switch.get()
        ctk.set_appearance_mode(theme)

    def start_puzzle(self):
        self.root.destroy()
        puzzle_root = ctk.CTk()
        PuzzleGUI(puzzle_root)
        puzzle_root.mainloop()

    def start_tictactoe(self):
        self.root.destroy()
        tictactoe_root = ctk.CTk()
        TicTacToeGUI(tictactoe_root)
        tictactoe_root.mainloop()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Default to dark mode
    root = ctk.CTk()
    app = GameMenu(root)
    root.mainloop()
