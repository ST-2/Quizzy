## Quizzy - README.md

**Quizzy** is a simple quiz application built with Tkinter that allows you to load and take quizzes from JSON files. It features a user-friendly interface with two modes: flashcard and multiple-choice. This was made mainly because of my hatred towards Quizlet

### Features

* **Load quizzes from JSON files:**  Quizzy can load quiz data from JSON files, allowing you to easily create and share quizzes.
* **Two quiz modes:** Choose between flashcard mode for focused learning or multiple-choice mode for a more challenging experience.
* **Scoring:**  Tracks your score as you progress through the quiz.
* **Sun Valley Theme:**  Modern and visually appealing interface with the Sun Valley theme.
* **"I Don't Know" option:**  Reveal the correct answer if you get stuck.


### Requirements

* Python 3.x
* Tkinter (usually included with Python)
* `sv_ttk` (for the Sun Valley theme)
* `json` (included with Python)


### Installation

1. **Install `sv_ttk`:**
   ```bash
   pip install sv_ttk
   ```

2. **Create a "quizes" directory:**
   Create a folder named "quizes" in the same directory as the `Quizzy.py` file. This is where you will store your quiz JSON files.

### Usage

1. **Create Quiz JSON files:**
   Create JSON files in the "quizes" directory following this format:

   ```json
   {
     "title": "Quiz Title",
     "questions": [
       {
         "question": "What is the capital of France?",
         "answer": "Paris",
         "example": "Example sentence with Paris..." 
       },
       {
         "question": "Another question?",
         "answer": "Answer"
       }
     ]
   }
   ```

2. **Run `Quizzy.py`:**
   ```bash
   python Quizzy.py 
   ```

3. **Select a quiz:**
   Choose a quiz from the list or open a JSON file using the "Open JSON File" button.

4. **Answer the questions:**
   Answer the questions in either flashcard or multiple-choice mode.

### To-Do

* Add more customization options (e.g., font size, colors).
* Implement a timer for timed quizzes.
* Add support for different question types (e.g., true/false, fill-in-the-blank).


## Quiz Generator - README.md

**Quiz Generator** is a Tkinter application that helps you easily create quizzes in JSON format. It provides a graphical interface for adding questions, answers, and optional examples.

### Features

* **User-friendly interface:**  Easily add questions and answers with a simple form.
* **Scrollable questions area:**  Add as many questions as you need.
* **Optional examples:**  Include example sentences or explanations for each question.
* **Save to JSON:**  Save your quiz in JSON format for use with Quizzy.
* **Sun Valley Theme:**  Modern and visually appealing interface with the Sun Valley theme.

### Requirements

* Python 3.x
* Tkinter (usually included with Python)
* `sv_ttk` (for the Sun Valley theme)
* `json` (included with Python)

### Installation

1. **Install `sv_ttk`:**
   ```bash
   pip install sv_ttk
   ```

### Usage

1. **Run `QuizGeneratorGUI.py`:**
   ```bash
   python QuizGeneratorGUI.py
   ```

2. **Enter a quiz title:**
   Provide a title for your quiz.

3. **Add questions:**
   Fill in the question, answer, and optional example fields for each question. Click "Add Question" to add more questions.

4. **Save the quiz:**
   Click "Save Quiz" to save your quiz as a JSON file. You can then use this file with the Quizzy application.
