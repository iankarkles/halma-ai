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


    def create_buttons(self):
        self.button_font = "Helvetica 16"
        self.button_bg = "#fff"
        self.button_fg = "#333"
        self.button_width = 25
        self.button_height = 2
    

        self.single_player_button = tk.Button(
            self,
            text="Human vs. AI Player - Easy",
            font=self.button_font,
            bg=self.button_bg,
            fg=self.button_fg,
            width=self.button_width,
            height=self.button_height,
            command=lambda: self.open_halma(difficulty="easy"),
        )
        self.single_player_button.grid(row=0, column=0)

        self.single_player_button = tk.Button(
            self,
            text="Human vs. AI Player - Medium",
            font=self.button_font,
            bg=self.button_bg,
            fg=self.button_fg,
            width=self.button_width,
            height=self.button_height,
            command=lambda: self.open_halma(difficulty="medium"),
        )
        self.single_player_button.grid(row=1, column=0)

        self.single_player_button = tk.Button(
            self,
            text="Human vs. AI Player - Hard",
            font=self.button_font,
            bg=self.button_bg,
            fg=self.button_fg,
            width=self.button_width,
            height=self.button_height,
                command=lambda: self.open_halma(difficulty="hard"),
        )
        self.single_player_button.grid(row=2, column=0)

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
        self.multi_player_button.grid(row=3, column=0)

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
        self.exit_button.grid(row=4, column=0)

    def open_halma(self, difficulty):
    # Store the selected difficulty and close the window
        self.difficulty = difficulty
        #self.destroy()
        self.quit()
        return difficulty
