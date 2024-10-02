import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import sv_ttk  # Import the Sun Valley theme

class QuizGeneratorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Generator")
        self.geometry("600x400")

        # Apply Sun Valley theme
        sv_ttk.set_theme("dark")

        self.create_widgets()

    def create_widgets(self):
        # Title Frame
        title_frame = ttk.Frame(self, padding="10")
        title_frame.pack(fill=tk.X)

        ttk.Label(title_frame, text="Quiz Title:").pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(title_frame)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Questions Frame (scrollable)
        questions_frame = ttk.Frame(self)
        questions_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(questions_frame)
        scrollbar = ttk.Scrollbar(questions_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initial question
        self.add_question()

        # Buttons Frame
        buttons_frame = ttk.Frame(self, padding="10")
        buttons_frame.pack(fill=tk.X)

        ttk.Button(buttons_frame, text="Add Question", command=self.add_question).pack(side=tk.LEFT)
        ttk.Button(buttons_frame, text="Save Quiz", command=self.save_quiz).pack(side=tk.RIGHT)

    def add_question(self):
        question_frame = ttk.LabelFrame(self.scrollable_frame, text=f"Question {len(self.scrollable_frame.winfo_children()) + 1}", padding="10")
        question_frame.pack(fill=tk.X, pady=5)

        ttk.Label(question_frame, text="Question:").grid(row=0, column=0, sticky=tk.W)
        question_entry = ttk.Entry(question_frame)
        question_entry.grid(row=0, column=1, sticky=tk.W + tk.E)

        ttk.Label(question_frame, text="Answer:").grid(row=1, column=0, sticky=tk.W)
        answer_entry = ttk.Entry(question_frame)
        answer_entry.grid(row=1, column=1, sticky=tk.W + tk.E)

        ttk.Label(question_frame, text="Example (Optional):").grid(row=2, column=0, sticky=tk.W)
        example_entry = ttk.Entry(question_frame)
        example_entry.grid(row=2, column=1, sticky=tk.W + tk.E)

        question_frame.columnconfigure(1, weight=1)  # Make entry widgets expand

    def save_quiz(self):
        title = self.title_entry.get()
        if not title:
            messagebox.showerror("Error", "Please enter a quiz title.")
            return

        questions = []
        for question_frame in self.scrollable_frame.winfo_children():
            question_entry = question_frame.winfo_children()[1]  # Get question entry
            answer_entry = question_frame.winfo_children()[3]  # Get answer entry
            example_entry = question_frame.winfo_children()[5]  # Get example entry

            question = question_entry.get()
            answer = answer_entry.get()

            if not question or not answer:
                messagebox.showerror("Error", "Please fill in all question and answer fields.")
                return

            question_data = {
                "question": question,
                "answer": answer
            }
            example = example_entry.get()
            if example:
                question_data["example"] = example

            questions.append(question_data)

        quiz_data = {
            "title": title,
            "questions": questions
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(quiz_data, f, indent=4)
                messagebox.showinfo("Success", f"Quiz saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving quiz: {e}")

if __name__ == "__main__":
    app = QuizGeneratorGUI()
    app.mainloop()