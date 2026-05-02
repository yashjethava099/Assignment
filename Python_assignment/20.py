import random
import string

class User:
    def __init__(self, user_id, name, password):
        self.data = (user_id, name, password)   # storing as tuple

    def display(self):
        print("User Details:", self.data)


def generate_password(text):
    try:
        words = text.split()

        if len(words) == 0:
            raise ValueError("Input cannot be empty")

        # pick random words
        selected_words = random.sample(words, min(2, len(words)))

        # add random elements
        number = str(random.randint(10, 99))
        special = random.choice("!@#$%^&*")
        upper = random.choice(string.ascii_uppercase)

        password = "".join(selected_words) + number + special + upper

        # ensure length > 8
        if len(password) <= 8:
            password += "Xy9@"   # force strong length

        return password

    except Exception as e:
        print("Error:", e)
        return None


# ---- Main Program ----
try:
    user_id = int(input("Enter user ID: "))
    name = input("Enter name: ")
    text = input("Enter some words: ")

    password = generate_password(text)

    if password:
        user = User(user_id, name, password)
        user.display()
    else:
        print("Password generation failed.")

except ValueError:
    print("Invalid input! Please enter correct data type.")