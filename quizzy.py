import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sv_ttk
import random
import json
import os

class Quizzy(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quizzy - Quiz Selector") 
        self.geometry("400x250") 

        # Apply Sun Valley theme
        sv_ttk.set_theme("dark")

        self.quiz_files = self.get_quiz_files()
        self.create_widgets()

    def get_quiz_files(self):
        quiz_dir = "quizes"
        if not os.path.exists(quiz_dir):
            os.makedirs(quiz_dir)
        return [f for f in os.listdir(quiz_dir) if f.endswith(".json")]

    def create_widgets(self):
        self.label = ttk.Label(self, text="Select a quiz file from the list or open a new JSON file:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self, width=250)
        for quiz_file in self.quiz_files:
            self.listbox.insert(tk.END, quiz_file)
        self.listbox.pack()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        self.open_button = ttk.Button(button_frame, text="Open Selected", command=self.open_quiz) 
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.open_file_button = ttk.Button(button_frame, text="Open JSON File", command=self.open_json_file)
        self.open_file_button.pack(side=tk.LEFT, padx=5)

    def open_json_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_quiz_data(file_path, from_file=True)

    def open_quiz(self):
        selection = self.listbox.curselection()
        if selection:
            quiz_file = self.quiz_files[selection[0]]
            self.load_quiz_data(quiz_file)
        else:
            messagebox.showwarning("Warning", "Please select a quiz file.")

    def load_quiz_data(self, quiz_file, from_file=False):
        try:
            if from_file:
                with open(quiz_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            else:
                with open(os.path.join("quizes", quiz_file), "r", encoding="utf-8") as f:
                    self.data = json.load(f)

            self.title(self.data["title"])
            self.geometry("600x500")

            self.questions = self.data["questions"]  # Changed from 'verbs' to 'questions'

            self.current_question = None
            self.score = 0
            self.total_questions = 0

            # Clear existing widgets
            for widget in self.winfo_children():
                widget.destroy()

            # Create new quiz widgets
            self.create_quiz_widgets()
            self.next_question()

        except Exception as e:
            messagebox.showerror("Error", f"Error loading quiz file: {e}")

    def create_quiz_widgets(self):
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.question_label_frame = ttk.LabelFrame(self.main_frame, text="Question", padding="10")
        self.question_label_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.question_label = ttk.Label(self.question_label_frame, text="", wraplength=550, font=("", 12))
        self.question_label.pack(pady=10)

        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.main_frame, textvariable=self.answer_var, font=("", 12), width=30)
        self.answer_entry.pack(pady=10)

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        self.submit_button = ttk.Button(button_frame, text="Submit", command=self.check_answer)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.idk_button = ttk.Button(button_frame, text="I Don't Know", command=self.reveal_answer)
        self.idk_button.pack(side=tk.LEFT, padx=5)

        self.score_label = ttk.Label(self.main_frame, text="Score: 0/0", font=("", 12))
        self.score_label.pack(pady=10)

        self.mode_var = tk.StringVar(value="flashcard")
        mode_frame = ttk.Frame(self.main_frame)
        mode_frame.pack(pady=10)
        self.flashcard_rb = ttk.Radiobutton(mode_frame, text="Flashcard", variable=self.mode_var, value="flashcard", command=self.next_question)
        self.multiple_choice_rb = ttk.Radiobutton(mode_frame, text="Multiple Choice", variable=self.mode_var, value="multiple_choice", command=self.next_question)
        self.flashcard_rb.pack(side=tk.LEFT, padx=5)
        self.multiple_choice_rb.pack(side=tk.LEFT, padx=5)

        self.choice_frame = ttk.Frame(self.main_frame)
        self.choice_frame.pack(pady=10)

        self.notification_label = ttk.Label(self.main_frame, text="", font=("", 12))
        self.notification_label.pack(pady=10)

    def next_question(self):
        self.notification_label.config(text="")
        if self.questions:
            self.current_question = random.choice(self.questions)
            # Clear the answer entry
            self.answer_var.set("")
            self.answer_entry.config(state="normal")
            self.submit_button.config(state="normal")
            self.idk_button.config(state="normal")

            if self.mode_var.get() == "flashcard":
                self.show_flashcard()
            else:
                self.show_multiple_choice()
        else:
            messagebox.showinfo("Quiz Completed", "You have completed all questions in this quiz!")

    def show_flashcard(self):
        self.question_label.config(text=self.current_question["question"]) 
        self.answer_entry.delete(0, tk.END)
        self.clear_choices()
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())  # Enable Enter key

    def show_multiple_choice(self):
        self.question_label.config(text=self.current_question["question"]) 
        choices = [self.current_question["answer"]]
        while len(choices) < 4:
            random_question = random.choice(self.questions)
            if random_question["answer"] not in choices:
                choices.append(random_question["answer"])
        random.shuffle(choices)

        self.clear_choices()

        self.answer_var.set("")
        for choice in choices:
            rb = ttk.Radiobutton(self.choice_frame, text=choice, variable=self.answer_var, value=choice)
            rb.pack(anchor=tk.W, padx=20, pady=5)

        self.answer_entry.config(state="disabled")

    def clear_choices(self):
        for widget in self.choice_frame.winfo_children():
            widget.destroy()

    def check_answer(self):
        user_answer = self.answer_var.get().strip().lower()
        correct_answer = self.current_question["answer"].lower()

        self.total_questions += 1
        if user_answer == correct_answer:
            self.score += 1
            self.notification_label.config(text="Correct!", foreground="green") 
            self.answer_entry.config(background="lightgreen")
        else:
            self.notification_label.config(text=f"Incorrect. The correct answer is '{self.current_question['answer']}'.", foreground="red")
            self.answer_entry.config(background="lightcoral") 
            # Show the correct answer in the textbox if it's a flashcard question
            if self.mode_var.get() == "flashcard":
                self.answer_var.set(self.current_question['answer'])


        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        self.answer_entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.idk_button.config(state="disabled")

        self.after(2000, self.reset_for_next_question)

    def reset_for_next_question(self):
        self.answer_entry.config(background="white")  # Reset background color
        self.next_question()

    def reveal_answer(self):
        self.submit_button.config(state="disabled")
        self.idk_button.config(state="disabled")

        if self.mode_var.get() == "flashcard":
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, self.current_question['answer']) 
            self.answer_entry.config(state="disabled")
        else:
            for widget in self.choice_frame.winfo_children():
                if widget.cget("text") == self.current_question['answer']: 
                    widget.config(foreground="green")

        self.after(2000, self.reset_for_next_question)

if __name__ == "__main__":
    # Hide the console window (Windows only)
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    app = Quizzy()
    app.mainloop()