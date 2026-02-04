import bcrypt

# Hash memorizzato nel database
stored_hash = "$2b$12$mxVp9KR0tCeAoAnANyV7r.PWuyggl659SALTCZXQ6JfRicqusYZ/6"

# Password fornita per il test
provided_password = "password123"

# Verifica della corrispondenza
if bcrypt.checkpw(provided_password.encode("utf-8"), stored_hash.encode("utf-8")):
    print("La password fornita è corretta.")
else:
    print("La password fornita è errata.")