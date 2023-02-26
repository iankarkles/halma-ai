# Python Standard Library imports
import tkinter as tk

class Menu(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Initialize parent tk class
        tk.Tk.__init__(self, *args, **kwargs)

        # Save metadata
        self.title("Halma Project -  IART 2023/MECD - FEUP")
        self.wm_iconbitmap("feup.ico")
        self.resizable(False, False)
        self.configure(bg="#fff")

        # Create menu buttons
        self.button_font = "Helvetica 16"
        self.button_bg = "#fff"
        self.button_fg = "#333"
        self.button_width = 20
        self.button_height = 2

        self.single_player_button = tk.Button(self, text="Human vs. AI Player",
            font=self.button_font, bg=self.button_bg, fg=self.button_fg,
            width=self.button_width, height=self.button_height,
            command=self.show_difficulty_screen)
        self.single_player_button.grid(row=0, column=0)

        self.multi_player_button = tk.Button(self, text="Human vs. Human",
            font=self.button_font, bg=self.button_bg, fg=self.button_fg,
            width=self.button_width, height=self.button_height)
        self.multi_player_button.grid(row=1, column=0)

        self.exit_button = tk.Button(self, text="Exit",
            font=self.button_font, bg=self.button_bg, fg=self.button_fg,
            width=self.button_width, height=self.button_height,
            command=self.quit)
        self.exit_button.grid(row=2, column=0)

        # Create another frame for difficulty selection
        self.difficulty_frame = tk.Frame(self, bg="#fff")
        self.difficulty_frame.grid(row=0, column=1, rowspan=3)

        # Create difficulty buttons
        self.difficulty_button_font = "Helvetica 14"
        self.difficulty_button_bg = "#fff"
        self.difficulty_button_fg = "#333"
        self.difficulty_button_width = 10
        self.difficulty_button_height = 2

        self.easy_button = tk.Button(self.difficulty_frame, text="Easy",
            font=self.difficulty_button_font, bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg, width=self.difficulty_button_width,
            height=self.difficulty_button_height)
        
        self.medium_button = tk.Button(self.difficulty_frame, text="Medium",
            font=self.difficulty_button_font, bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg, width=self.difficulty_button_width,
            height=self.difficulty_button_height)
        
        self.hard_button = tk.Button(self.difficulty_frame, text="Hard",
            font=self.difficulty_button_font, bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg, width=self.difficulty_button_width,
            height=self.difficulty_button_height)
        
    def show_difficulty_screen(self):
        # Create a new window for difficulty selection
        self.difficulty_window = tk.Toplevel(self)
        self.difficulty_window.title("Select Difficulty")
        self.resizable(False, False)

        # Add buttons for difficulty selection
        easy_button = tk.Button(self.difficulty_window, text="Easy",
            font=self.difficulty_button_font, bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg, width=self.difficulty_button_width,
            height=self.difficulty_button_height)
        easy_button.grid(row=0, column=0)
        medium_button = tk.Button(self.difficulty_window, text="Medium",
            font=self.difficulty_button_font, bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg, width=self.difficulty_button_width,
            height=self.difficulty_button_height)
        medium_button.grid(row=1, column=0)
        hard_button = tk.Button(self.difficulty_window, text="Hard",
            font=self.difficulty_button_font, bg=self.difficulty_button_bg,
            fg=self.difficulty_button_fg, width=self.difficulty_button_width,
            height=self.difficulty_button_height)
        hard_button.grid(row=2, column=0)

