# Packages Installed: hashlib, math, time
import hashlib
import math
import time
# Maxes for key 1, 2, and 3
key_max = 10**40
# Characters
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z", 
           "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
           "!", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", 
           ",", ".", "?",":", "'", "\"", "-", "_", "(", ")", "[", "]", "{", "}", "/", "\\", "*", "&", "^", "%", "$", "#", "@", "=", "+", "`", "~", "<", ">", "↑", "↓","→","←"]
# Mapping Dictionary
character_to_index = {char: idx for idx, char in enumerate(letters)}
# Hashing function
def hash_key(key):
    return int(hashlib.sha256(str(key).encode()).hexdigest(), 16)
# Decryption function
def ecdc(text, key, key2, key3, position, ende):
    key = hash_key(key)
    key2 = hash_key(key2)
    key3=hash_key(key3)
    output = []
    for i in range(len(text)):
        #Chacter Value
        charval=character_to_index[text[i]]
        #Formula
        outletter=(charval + (ende * key) - ende * (math.ceil(key2 // (i + key3))) + (ende * position)) % len(letters)
        output.append(letters[outletter])
        #Change of variable
        if ende == 1:
            position = (position + charval + key3) % abs(position + key - key2)
        else:
            position = (position + outletter + key3) % abs(position + key - key2)
    output = "".join(output)
    return output

# User Input Function
def choice():
    try:
        #Input
        key = int(input("Enter key (1): "))
        key2 = int(input("Enter key (2): "))
        key3 = int(input("Enter key (3): "))
        key4 = int(input("Enter key (4): "))
        #Validity Checks
        if key <= key2:
            raise ValueError("Key 1 must be greater than Key 2")
        if key > key_max:
            raise ValueError("Key 1 must be less than 10^40")
        if key2 > key_max:
            raise ValueError("Key 2 must be less than 10^40")
        if key3 > key_max:
            raise ValueError(f"Key 3 must be less than 10^40")
        if key4 > key_max:
            raise ValueError(f"Key 4 must be less than 10^40")
        if key < 0 or key2 < 0 or key3 < 0:
            raise ValueError("Keys must be positive")
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
