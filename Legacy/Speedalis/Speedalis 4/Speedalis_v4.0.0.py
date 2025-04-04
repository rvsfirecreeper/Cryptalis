# Packages Installed: hashlib, math, time
import hashlib
import math
import time
import argon2
# Maxes for key 1, 2, and 3
# Characters
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z",
           "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
           "!", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ",
           ",", ".", "?",":", "'", "\"", "-", "_", "(", ")", "[", "]", "{", "}", "/", "\\", "*", "&", "^", "%", "$", "#", "@", "=", "+", "`", "~", "<", ">", "↑", "↓","→","←"]
# Mapping Dictionary
character_to_index = {char: idx for idx, char in enumerate(letters)}
# Hashing function
def hash_key(key):
    salt = hashlib.sha256(str(key).encode()).digest()[:16]
    return int.from_bytes(argon2.low_level.hash_secret_raw(secret = key.encode(),salt = salt, type = argon2.Type.ID, time_cost = 4, memory_cost = 2**16, parallelism = 4, hash_len = 32))
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
        #Character Value
        charval=character_to_index[text[i]]
        listlen = len(letters)
        #Formula
        outletter=(charval + pc1 - ende * (math.ceil(key2 // (i + key3))) + (ende * position)) % listlen
        output.append(letters[outletter])
        #Change of variable
        if ende == 1:
            position = (position + charval + key3) % abs(position + pc2)
        else:
            position = (position + outletter + key3) % abs(position + pc2)
    output = "".join(output)
    return output

# User Input Function
def choice():
    try:
        #Input
        key = (input("Enter key (1): "))
        key2 = (input("Enter key (2): "))
        key3 = (input("Enter key (3): "))
        key4 = input("Enter key (4): ")
        #Catch errors
        if key == "" or key2 == "" or key3 == "" or key4 == "":
            raise ValueError("Key cannot be empty")
        if key == key2:
            raise ValueError("Key 1 and Key 2 cannot be the same, this will cause ZeroDivisionError")
    #Error Handling
    except ValueError as e:
        print(f"Error: {e}. Please enter a number or ensure Key 1 > Key 2. Make sure key 1 and 2 are under 10**40 and key 3 is under 5000")
        return choice()

    user_choice = input("Encrypt (ec) or Decrypt (dc)? ")
    text = input("Enter text to en/decrypt: ")
    start = time.time()
    if user_choice == "ec":
        return f"It took {time.time()-start} to encrypt. the text is:{ecdc(text, key, key2, key3, key4,1)}"
    elif user_choice == "dc":
        return f"It took {round(time.time()-start)} seconds to decrypt. the text is:{ecdc(text, key, key2, key3, key4, -1)}"
    else:
        print("Invalid choice")
        return choice()

# Run the program
result = choice()
if result:
    print(result)
input()
