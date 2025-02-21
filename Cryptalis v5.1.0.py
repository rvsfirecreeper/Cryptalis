import hashlib
import math
import time
keymax = 10**40
iterationmax = 5000
# Character set
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
           "S", "T", "U", "V", "W", "X", "Y", "Z", ",", ".", "?", "!", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
           " ", "'", "\"", "-", "_", "(", ")", "[", "]", "{", "}", "/", "\\", "*", "&", "^", "%", "$", "#", "@", "=",
           "+", "`", "~", "<", ">", "↑", "↓","→","←"]


# Hashing function for keys
def hash_key(key):
    return (int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % (keymax))+1


# Encryption function
def ec(text, key, key2, wordcounter, iterations):
    key = hash_key(key)
    key2 = hash_key(key2)
    output = ""
    for i in range(iterations):
        for j in range(len(text)):
            for k in range(len(letters)):
                if text[j] == letters[k]:
                    output += letters[(k + key - math.ceil(key2 // (j + 1)) + wordcounter) % len(letters)]
                    break
            wordcounter += j  # Non determination
            wordcounter = wordcounter % abs(wordcounter - key + key2)
        text = output
        if not i + 1 == iterations:
            output = ""
    return output


# Decryption function
def dc(encryptedtext, key, key2, wordcounter, iterations):
    key = hash_key(key)
    key2 = hash_key(key2)
    output = ""
    for i in range(iterations):
        for j in range(len(encryptedtext)):
            for k in range(len(letters)):
                if encryptedtext[j] == letters[k]:
                    output += letters[(k - key + math.ceil(key2 // (j + 1)) - wordcounter) % len(letters)]
                    break
            wordcounter += j
            wordcounter = wordcounter % abs(wordcounter - key + key2)
        encryptedtext=output
        if not i+1 == iterations:
            output=""
    return output


# User Input Function
def choice():
    try:
        key = int(input("Enter key (1): "))
        if key > keymax:
            key = keymax
        key2 = int(input("Enter key (2): "))
        if key2 > keymax:
            key2 = keymax
        if key <= key2:
            key = int('c you')
        iterations=int(input("Enter key (3): "))
        if iterations > iterationmax:
            iterations = iterationmax
    except:
        print("Please enter a number or ensure Key 1 > Key 2. Make sure key 1 and 2 are under 10**40 and key 3 is under 5000")
        return choice()

    user_choice = input("Encrypt (ec) or Decrypt (dc)? ").lower()
    if user_choice == "ec":
        text_to_encrypt = input("Enter text to encrypt: ")
        start = time.time()
        return "It took " + str(time.time()-start) + " to encrypt. the text is:" + ec(text_to_encrypt, key, key2, 1, iterations)
    elif user_choice == "dc":
        text_to_decrypt = input("Enter text to decrypt: ")
        start = time.time()
        return "It took " + str(time.time()-start) + " to decrypt. the text is:" + dc(text_to_decrypt, key, key2, 1, iterations)
    else:
        print("Invalid choice")
        return choice()


# Run the program
result = choice()
if result:
    print(result)
input()
