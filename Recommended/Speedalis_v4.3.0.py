# Packages Installed: hashlib, math, time
import hashlib
import math
import time
# Dependencies
import argon2
import pyperclip
# Maxes for key 1, 2, and 3
# Characters
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
           "S", "T", "U", "V", "W", "X", "Y", "Z", ",", ".", "?", "!", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
           " ", ":", "'", "\"", "-", "_", "(", ")", "[", "]", "{", "}", "/", "\\", "*", "&", "^", "%", "$", "#", "@",
           "=",
           "+", "`", "~", "<", ">", "↑", "↓", "→", "←", "”", "“", "•", "…", "‘", "’", "•", "°", "§", "©", "®"]
# Mapping Dictionary
character_to_index = {char: idx for idx, char in enumerate(letters)}


# Hashing function
def hash_key(key):
    salt = hashlib.sha256(str(key).encode()).digest()[:16]
    return int.from_bytes(
        argon2.low_level.hash_secret_raw(secret=key.encode(), salt=salt, type=argon2.Type.ID, time_cost=16,
                                         memory_cost=2 ** 16, parallelism=4, hash_len=32))


# En/Decryption function
def ecdc(text, key, key2, key3, position, ende):
    key = hash_key(key)
    key2 = hash_key(key2)
    key3 = hash_key(key3)
    position = hash_key(position)
    # Precomputed Values
    pc1 = (ende * key)
    pc2 = key - key2
    output = []
    for i in range(len(text)):
        # Character Value
        charval = character_to_index[text[i]]
        listlen = len(letters)
        # Formula
        outletter = (charval - pc1 + ende * (math.ceil(key2 // (i + key3))) - (ende * position)) % listlen
        output.append(letters[outletter])
        # Change of variable
        if ende == 1:
            position = (position + charval + key3) % abs(position + pc2)
        else:
            position = (position + outletter + key3) % abs(position + pc2)
    output = "".join(output)
    return output


# User Input Function
def choice():
    try:
        # Input
        key = (input("Enter key (1): "))
        key2 = (input("Enter key (2): "))
        key3 = (input("Enter key (3): "))
        initvector = input("Enter IV: ")
        # Catch errors
        if key == key2:
            raise ValueError("Key 1 and Key 2 cannot be the same, this will cause ZeroDivisionError")
    # Error Handling
    except ValueError as e:
        print(f"ValueError: {e}.")
        return choice()

    user_choice = input("Encrypt (ec) or Decrypt (dc)? ")
    text = input("Enter text to en/decrypt: ")
    start = time.time()
    if user_choice == "ec":
        output = ecdc(text, key, key2, key3, initvector, 1)
        return output
    elif user_choice == "dc":
        output = ecdc(text, key, key2, key3, initvector, -1)
        return output
    else:
        print("Invalid choice")
        return choice()


# Run the program
result = choice()
if result:
    print (f"The text is: '{result}'")
    pyperclip.copy(result)
    print("Copied to clipboard")
input()
