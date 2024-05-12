from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Słowo, które gracz będzie próbował odgadnąć
WORD = "PYTHON"

# Maksymalna liczba błędnych prób (cały wisielec)
MAX_WRONG_ATTEMPTS = 6

# Lista liter, które gracz już wybrał
guessed_letters = []

# Funkcja do generowania obrazka wisielca na podstawie liczby błędnych prób
def generate_hangman_image(num_wrong):
    stages = [
        """
           --------
           |      |
           |
           |
           |
           |
        """,
        """
           --------
           |      |
           |      O
           |
           |
           |
        """,
        """
           --------
           |      |
           |      O
           |      |
           |
           |
        """,
        """
           --------
           |      |
           |      O
           |     /|
           |
           |
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |
           |
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     /
           |
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / \\
           |
        """
    ]
    return stages[num_wrong]

# Funkcja do sprawdzenia stanu gry (czy gracz wygrał, przegrał lub nadal gra)
def check_game_state():
    if all(letter in guessed_letters for letter in WORD):
        return "win"
    incorrect_guesses = len([letter for letter in guessed_letters if letter not in WORD])
    if incorrect_guesses >= MAX_WRONG_ATTEMPTS:
        return "lose"
    return "play"

# Resetowanie gry
def reset_game():
    global guessed_letters
    guessed_letters = []

# Strona główna - wyświetla stan gry i formularz do wprowadzania liter
@app.route("/", methods=["GET", "POST"])
def home():
    global guessed_letters
    
    if request.method == "POST":
        if request.form.get("action") == "new_game":
            reset_game()
        else:
            letter = request.form["letter"].upper()
            if letter not in guessed_letters:
                guessed_letters.append(letter)

    game_state = check_game_state()
    hangman_image = generate_hangman_image(len([letter for letter in guessed_letters if letter not in WORD]))

    return render_template("index.html", word=WORD, guessed_letters=guessed_letters,
                           game_state=game_state, hangman_image=hangman_image)

if __name__ == "__main__":
    app.run(debug=True)
