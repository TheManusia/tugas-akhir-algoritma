import hashlib


def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def confirm(message):
    while True:
        confirm = input(f"{message} (y/n): ")
        if confirm.lower() == "y":
            return True
        elif confirm.lower() == "n":
            return False
        else:
            print("Input tidak valid")


def currencyFormat(number):
    return f"Rp{'{:,.2f}'.format(number)}"
