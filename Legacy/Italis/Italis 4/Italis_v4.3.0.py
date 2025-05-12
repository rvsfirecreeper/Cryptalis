# Packages Installed: hashlib, math, time
import hashlib
import math
import time
# Dependencies
import argon2
import pyperclip
# Maxes for key 1, 2, and 3
keymax = 10**40
iterationmax = 25000
# Character set
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
           "S", "T", "U", "V", "W", "X", "Y", "Z", ",", ".", "?", "!", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
           " ", ":", "'", "\"", "-", "_", "(", ")", "[", "]", "{", "}", "/", "\\", "*", "&", "^", "%", "$", "#", "@", "=",
           "+", "`", "~", "<", ">", "↑", "↓","→","←", "”", "“", "•", "…", "‘", "’", "•", "°", "§", "©", "®"]
character_to_index = {char: idx for idx, char in enumerate(letters)}

# Hashing function for keys
def hash_key(key):
    salt = hashlib.sha256(str(key).encode()).digest()[:16]
    return int.from_bytes(argon2.low_level.hash_secret_raw(secret=key.encode(), salt=salt, type=argon2.Type.ID, time_cost=4, memory_cost=2 ** 16, parallelism=4, hash_len=32))

# En/Decryption function
def ecdc(encryptedtext, key, key2, position, iterations, ende):
    key = hash_key(key)
    key2 = hash_key(key2)
    position = hash_key(position)
    iterations = (hash_key(iterations) % 25000) + 175000
    output = []
    for i in range(iterations):
        for j in range(len(encryptedtext)):
            k=character_to_index[encryptedtext[j]]
            outletter = (k - (ende*key) + (ende*math.ceil(key2 // (j + 1))) - ende*position) % len(letters)
            output.append(letters[outletter])
            if ende == 1:
                position = (position + iterations + k) % abs(position - key + key2)
            else:
                position = (position + iterations + outletter) % abs(position - key + key2)

        encryptedtext=output
        if not i+1 == iterations:
            output=[]
    output = "".join(output)
    return output

# User Input Function
def choice():
    try:
        key = input("Enter key (1): ")
        key2 = input("Enter key (2): ")
        iterations = input("Enter key (3): ")
        initvector = input("Enter IV: ")
        # Catch errors
        if key == key2:
            raise ValueError("Key 1 must be different than Key 2")
    except ValueError as e:
        print(f"ValueError: {e}.")
        return choice()

    user_choice = input("Encrypt (ec) or Decrypt (dc)? ").lower()
    text = input("Enter text to en/decrypt: ")
    start = time.time()
    if user_choice == "ec":
        output = ecdc(text, key, key2, initvector, iterations, 1)
        return output
    elif user_choice == "dc":
        output = ecdc(text, key, key2, initvector, iterations, -1)
        return output
    else:
        print("Invalid choice")
        return choice()
# Run the program
result = choice()
if result:
    print(f"The text is: '{result}'")
    pyperclip.copy(result)
    print("Copied to clipboard")
input()
