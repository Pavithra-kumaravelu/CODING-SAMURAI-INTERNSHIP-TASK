import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.bg_color = "#1a1a2e"
        self.card_color = "#16213e"
        self.accent_color = "#0f4c75"
        self.success_color = "#27ae60"
        self.warning_color = "#f39c12"
        self.danger_color = "#e74c3c"
        self.text_color = "#ecf0f1"
        self.secondary_text = "#bdc3c7"
        
        self.root.configure(bg=self.bg_color)
        
        # Game variables
        self.max_attempts = 7
        self.secret_number = random.randint(1, 100)
        self.guess_count = 0
        self.game_active = True
        
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Game title with gradient effect
        title_frame = tk.Frame(main_frame, bg=self.card_color, relief='raised', bd=2)
        title_frame.pack(fill='x', pady=(0, 20))
        
        self.title_label = tk.Label(
            title_frame, 
            text="🎯 NUMBER GUESSING GAME", 
            font=("Arial", 18, "bold"),
            fg="#3498db",
            bg=self.card_color,
            pady=15
        )
        self.title_label.pack()
        
        # Instructions card
        instructions_frame = tk.Frame(main_frame, bg=self.card_color, relief='raised', bd=1)
        instructions_frame.pack(fill='x', pady=(0, 20))
        
        instructions_label = tk.Label(
            instructions_frame,
            text="I'm thinking of a number between 1 and 100\nCan you guess what it is?",
            font=("Arial", 11),
            fg=self.secondary_text,
            bg=self.card_color,
            pady=15
        )
        instructions_label.pack()
        
        # Input section
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill='x', pady=(0, 20))
        
        input_label = tk.Label(
            input_frame,
            text="Enter your guess:",
            font=("Arial", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        input_label.pack(anchor='w', pady=(0, 5))
        
        # Custom styled entry
        entry_frame = tk.Frame(input_frame, bg=self.accent_color, relief='raised', bd=2)
        entry_frame.pack(fill='x', pady=(0, 15))
        
        self.entry = tk.Entry(
            entry_frame,
            font=("Arial", 16, "bold"),
            justify="center",
            bg="#34495e",
            fg=self.text_color,
            bd=0,
            insertbackground=self.text_color,
            relief='flat'
        )
        self.entry.pack(padx=3, pady=3, fill='x')
        
        # Submit button with hover effect
        self.submit_button = tk.Button(
            input_frame,
            text="🎲 MAKE YOUR GUESS",
            command=self.check_guess,
            font=("Arial", 12, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            bd=0,
            relief='raised',
            pady=12,
            cursor='hand2',
            activebackground="#2980b9",
            activeforeground="white"
        )
        self.submit_button.pack(fill='x')
        
        # Feedback section
        feedback_frame = tk.Frame(main_frame, bg=self.card_color, relief='raised', bd=1)
        feedback_frame.pack(fill='x', pady=(0, 20))
        
        self.feedback_label = tk.Label(
            feedback_frame,
            text="🤔 Ready when you are!",
            font=("Arial", 13, "bold"),
            fg=self.secondary_text,
            bg=self.card_color,
            pady=20,
            wraplength=350
        )
        self.feedback_label.pack()
        
        # Stats section
        stats_frame = tk.Frame(main_frame, bg=self.bg_color)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Attempts counter with progress visualization
        attempts_container = tk.Frame(stats_frame, bg=self.card_color, relief='raised', bd=1)
        attempts_container.pack(fill='x', pady=(0, 10))
        
        self.attempts_label = tk.Label(
            attempts_container,
            text=f"💪 Attempts remaining: {self.max_attempts}",
            font=("Arial", 11, "bold"),
            fg=self.success_color,
            bg=self.card_color,
            pady=10
        )
        self.attempts_label.pack()
        
        # Progress bar frame
        progress_frame = tk.Frame(attempts_container, bg=self.card_color)
        progress_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        self.progress_bars = []
        for i in range(self.max_attempts):
            bar = tk.Label(
                progress_frame,
                text="●",
                font=("Arial", 8),
                fg=self.success_color,
                bg=self.card_color
            )
            bar.pack(side='left', padx=2)
            self.progress_bars.append(bar)
        
        # Guess history
        history_label = tk.Label(
            stats_frame,
            text="📋 Your guesses will appear here:",
            font=("Arial", 10, "bold"),
            fg=self.secondary_text,
            bg=self.bg_color
        )
        history_label.pack(anchor='w')
        
        self.history_frame = tk.Frame(stats_frame, bg=self.card_color, relief='raised', bd=1)
        self.history_frame.pack(fill='x', pady=(5, 20))
        
        self.history_label = tk.Label(
            self.history_frame,
            text="No guesses yet...",
            font=("Arial", 10),
            fg=self.secondary_text,
            bg=self.card_color,
            pady=10
        )
        self.history_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill='x')
        
        self.reset_button = tk.Button(
            button_frame,
            text="🔄 PLAY AGAIN",
            command=self.reset_game,
            font=("Arial", 11, "bold"),
            bg=self.warning_color,
            fg="white",
            bd=0,
            relief='raised',
            pady=10,
            cursor='hand2',
            activebackground="#e67e22",
            activeforeground="white",
            state="disabled"
        )
        self.reset_button.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.hint_button = tk.Button(
            button_frame,
            text="💡 HINT",
            command=self.give_hint,
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            bd=0,
            relief='raised',
            pady=10,
            cursor='hand2',
            activebackground="#8e44ad",
            activeforeground="white"
        )
        self.hint_button.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Guess history list
        self.guess_history = []
    
    def bind_events(self):
        # Allow Enter key to submit guess
        self.root.bind('<Return>', lambda event: self.check_guess())
        self.entry.focus_set()
        
        # Add hover effects to buttons
        self.add_hover_effect(self.submit_button, self.accent_color, "#2980b9")
        self.add_hover_effect(self.reset_button, self.warning_color, "#e67e22")
        self.add_hover_effect(self.hint_button, "#9b59b6", "#8e44ad")
    
    def add_hover_effect(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
    def check_guess(self):
        if not self.game_active:
            return
            
        guess_text = self.entry.get().strip()
        
        # Input validation with better feedback
        if not guess_text:
            self.show_feedback("⚠️ Please enter a number!", self.warning_color)
            self.entry.focus_set()
            return
        
        if not guess_text.isdigit():
            self.show_feedback("⚠️ Please enter a valid number between 1 and 100!", self.warning_color)
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
            return
        
        guess = int(guess_text)
        
        if guess < 1 or guess > 100:
            self.show_feedback("⚠️ Number must be between 1 and 100!", self.warning_color)
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
            return
        
        # Process the guess
        self.guess_count += 1
        self.guess_history.append(guess)
        self.entry.delete(0, tk.END)
        
        # Update progress bars
        if self.guess_count <= len(self.progress_bars):
            self.progress_bars[self.guess_count - 1].config(fg=self.danger_color)
        
        # Check the guess
        if guess < self.secret_number:
            difference = self.secret_number - guess
            if difference <= 5:
                self.show_feedback(f"📈 Too low, but you're very close! ({guess})", "#f39c12")
            elif difference <= 15:
                self.show_feedback(f"📈 Too low, getting warmer! ({guess})", "#e67e22")
            else:
                self.show_feedback(f"📈 Too low, try higher! ({guess})", self.danger_color)
        elif guess > self.secret_number:
            difference = guess - self.secret_number
            if difference <= 5:
                self.show_feedback(f"📉 Too high, but you're very close! ({guess})", "#f39c12")
            elif difference <= 15:
                self.show_feedback(f"📉 Too high, getting warmer! ({guess})", "#e67e22")
            else:
                self.show_feedback(f"📉 Too high, try lower! ({guess})", self.danger_color)
        else:
            # Winner!
            self.show_feedback(f"🎉 CONGRATULATIONS! You found it in {self.guess_count} attempts!", self.success_color)
            self.end_game(won=True)
            return
        
        # Update attempts
        attempts_left = self.max_attempts - self.guess_count
        self.update_attempts_display(attempts_left)
        self.update_history_display()
        
        # Check for game over
        if self.guess_count >= self.max_attempts:
            self.show_feedback(f"😞 Game Over! The number was {self.secret_number}.", self.danger_color)
            self.end_game(won=False)
        
        self.entry.focus_set()
    
    def show_feedback(self, message, color):
        self.feedback_label.config(text=message, fg=color)
        # Add a subtle animation effect
        self.root.after(100, lambda: self.feedback_label.config(relief='raised'))
        self.root.after(200, lambda: self.feedback_label.config(relief='flat'))
    
    def update_attempts_display(self, attempts_left):
        if attempts_left <= 2:
            color = self.danger_color
            emoji = "⚠️"
        elif attempts_left <= 4:
            color = self.warning_color
            emoji = "⏰"
        else:
            color = self.success_color
            emoji = "💪"
        
        self.attempts_label.config(
            text=f"{emoji} Attempts remaining: {attempts_left}",
            fg=color
        )
    
    def update_history_display(self):
        if self.guess_history:
            history_text = "Your guesses: " + " → ".join(map(str, self.guess_history))
            self.history_label.config(text=history_text, fg=self.text_color)
    
    def give_hint(self):
        if not self.game_active or self.guess_count == 0:
            return
        
        # Provide different hints based on the number of attempts
        if self.guess_count <= 2:
            if self.secret_number <= 25:
                hint = "💡 Hint: The number is in the lower quarter (1-25)"
            elif self.secret_number <= 50:
                hint = "💡 Hint: The number is in the second quarter (26-50)"
            elif self.secret_number <= 75:
                hint = "💡 Hint: The number is in the third quarter (51-75)"
            else:
                hint = "💡 Hint: The number is in the upper quarter (76-100)"
        else:
            # More specific hint
            if self.secret_number % 2 == 0:
                hint = "💡 Hint: The number is even"
            else:
                hint = "💡 Hint: The number is odd"
        
        self.show_feedback(hint, "#9b59b6")
        
        # Disable hint button after use
        self.hint_button.config(state="disabled", text="💡 USED", bg="#7f8c8d")
    
    def end_game(self, won=False):
        self.game_active = False
        self.entry.config(state="disabled", bg="#2c3e50")
        self.submit_button.config(state="disabled", bg="#7f8c8d", text="GAME OVER")
        self.reset_button.config(state="normal", bg=self.warning_color)
        
        if won:
            # Celebration effect
            self.title_label.config(text="🏆 CONGRATULATIONS! 🏆", fg=self.success_color)
        else:
            self.title_label.config(text="😞 Better luck next time!", fg=self.danger_color)
    
    def reset_game(self):
        # Reset game state
        self.secret_number = random.randint(1, 100)
        self.guess_count = 0
        self.game_active = True
        self.guess_history = []
        
        # Reset UI elements
        self.entry.config(state="normal", bg="#34495e")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        
        self.feedback_label.config(text="🤔 Ready when you are!", fg=self.secondary_text)
        self.attempts_label.config(text=f"💪 Attempts remaining: {self.max_attempts}", fg=self.success_color)
        self.history_label.config(text="No guesses yet...", fg=self.secondary_text)
        
        self.submit_button.config(state="normal", bg=self.accent_color, text="🎲 MAKE YOUR GUESS")
        self.reset_button.config(state="disabled", bg="#7f8c8d")
        self.hint_button.config(state="normal", bg="#9b59b6", text="💡 HINT")
        
        self.title_label.config(text="🎯 NUMBER GUESSING GAME", fg="#3498db")
        
        # Reset progress bars
        for bar in self.progress_bars:
            bar.config(fg=self.success_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()