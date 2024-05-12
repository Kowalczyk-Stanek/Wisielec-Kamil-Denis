import random
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'tajny_Sekretny_klucz_potrzebny_do_session'
# Lista słów z tematyki przedmiotów szkolnych
WORD_LIST = [
    "MATEMATYKA",
    "FIZYKA",
    "CHEMIA",
    "BIOLOGIA",
    "INFORMATYKA",
    "HISTORIA",
    "GEOGRAFIA"
    "WOS",
    "PLASTYKA",
    "MUZYKA"
]

# Maksymalna liczba błędnych prób (cały wisielec)
MAX_WRONG_ATTEMPTS = 6

# Wybieramy losowe słowo z listy WORD_LIST
def choose_word():
    return random.choice(WORD_LIST)

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
    word = session.get("word")
    if all(letter in guessed_letters for letter in word):
        return "win"
    incorrect_guesses = len([letter for letter in guessed_letters if letter not in word])
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
    if request.method == "GET":
        word = choose_word().upper()
        session["word"] = word
        reset_game()
    elif request.method == "POST":
        letter = request.form["letter"].upper()
        if letter not in guessed_letters:
            guessed_letters.append(letter)

    game_state = check_game_state()
    hangman_image = generate_hangman_image(len([letter for letter in guessed_letters if letter not in session["word"]]))

    return render_template("index.html", word=session["word"], guessed_letters=guessed_letters,
                           game_state=game_state, hangman_image=hangman_image)

if __name__ == "__main__":
    app.run(debug=True)
