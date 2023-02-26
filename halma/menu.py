import tkinter as tk
import subprocess


class Menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up the main window
        self.title("Halma Project -  IART 2023/MECD - FEUP")
        self.wm_iconbitmap("feup.ico")
        self.resizable(False, False)
        self.configure(bg="#fff")

        # Create the menu buttons
        self.create_buttons()
    
        def open_halma(self, difficulty):
        # Close difficulty window
            self.quit()
        # Return the difficulty to the main argument
            Menu().open_halma(difficulty=difficulty)


    def create_buttons(self):
        self.button_font = "Helvetica 16"
        self.button_bg = "#fff"
        self.button_fg = "#333"
        self.button_width = 20
        self.button_height = 2

        self.single_player_button = tk.Button(
            self,
            text="Human vs. AI Player",
            font=self.button_font,
            bg=self.button_bg,
            fg=self.button_fg,
            width=self.button_width,
            height=self.button_height,
            command=self.show_difficulty_screen,
        )
        self.single_player_button.grid(row=0, column=0)

        self.multi_player_button = tk.Button(
            self,
            text="Human vs. Human",
            font=self.button_font,
            bg=self.button_bg,
            fg=self.button_fg,
            width=self.button_width,
            height=self.button_height,
            command=lambda: self.open_halma(difficulty="multi"),
        )
        self.multi_player_button.grid(row=1, column=0)

        self.exit_button = tk.Button(
            self,
            text="Exit",
            font=self.button_font,
            bg=self.button_bg,
            fg=self.button_fg,
            width=self.button_width,
            height=self.button_height,
            command=self.quit,
        )
        self.exit_button.grid(row=2, column=0)

    def show_difficulty_screen(self):
        # Close main menu
        self.withdraw()

        # Create a new window for difficulty selection
        DifficultyScreen(self)

    def start_game(self, difficulty):
        # TODO: Implement start_game method
        pass


class DifficultyScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set up the difficulty window
        self.title("Select Difficulty")
        self.resizable(False, False)

        # Create the difficulty buttons
        self.create_buttons()

    def create_buttons(self):
        self.difficulty_button_font = "Helvetica 14"
        self.difficulty_button_bg = "#fff"
        self.difficulty_button_fg = "#333"
        self.difficulty_button_width = 10
        self.difficulty_button_height = 2

        self.easy_button = tk.Button(
            self,
            text="Easy",
            font=self.difficulty_button_font,
            bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg,
            width=self.difficulty_button_width,
            height=self.difficulty_button_height,
            command=lambda: self.open_halma(difficulty="easy"),
        )
        self.easy_button.grid(row=0, column=0)

        self.medium_button = tk.Button(
            self,
            text="Medium",
            font=self.difficulty_button_font,
            bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg,
            width=self.difficulty_button_width,
            height=self.difficulty_button_height,
            command=lambda: self.open_halma(difficulty="medium"),
        )
        self.medium_button.grid(row=1, column=0)

        self.hard_button = tk.Button(
            self,
            text="Hard",
            font=self.difficulty_button_font,
            bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg,
            width=self.difficulty_button_width,
            height=self.difficulty_button_height,
            command=lambda: self.open_halma(difficulty="hard"),
        )
        self.hard_button.grid(row=2, column=0)

    def open_halma(self, difficulty):
        # Close difficulty window
        self.quit()
        # Return the difficulty to the main argument
        Menu().open_halma(difficulty=difficulty)

