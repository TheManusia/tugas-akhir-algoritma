import hashlib


class Tools:

    def __init__(self):
        pass

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def confirm(self, message):
        while True:
            confirm = input(f"{message} (y/n): ")
            if confirm.lower() == "y":
                return True
            elif confirm.lower() == "n":
                return False
            else:
                print("Input tidak valid")
