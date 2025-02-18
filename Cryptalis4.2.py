# This is a legacyversion. Not Reccomended
# Character set
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
           "S", "T", "U", "V", "W", "X", "Y", "Z", ",", ".", "?", "!", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
           " ", "'", "\"", "-", "_", "(", ")", "[", "]", "{", "}", "/", "\\", "*", "&", "^", "%", "$", "#", "@", "=",
           "+", "`", "~", "<", ">"]

# Hashing function
def hash_key(key):
    return int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % (10 ** 40)

# Encryption function
def ec(text, key, key2, wordcounter):
    key = hash_key(key)
    key2 = hash_key(key2)
    output = ""

    for i in range(len(text)):
        for k in range(len(letters)):
            if text[i] == letters[k]:
                output += letters[(k + key - math.ceil(key2 // (i + 1)) + wordcounter) % len(letters)]
                break
        wordcounter += i  # Non determination
        wordcounter = wordcounter % abs(wordcounter - key + key2)
    return output

# Decryption function
def dc(encryptedtext, key, key2, wordcounter):
    key = hash_key(key)
    key2 = hash_key(key2)
    output = ""

    for i in range(len(encryptedtext)):
        for k in range(len(letters)):
            if encryptedtext[i] == letters[k]:
                output += letters[(k - key + math.ceil(key2 // (i + 1)) - wordcounter) % len(letters)]
                break
        wordcounter += i
        wordcounter = wordcounter % abs(wordcounter - key + key2)
    return output

# input
def choice():
    try:
        key = int(input("Enter key (1): "))
        if key > 10 ** 40:
            key = 10 ** 40
        key2 = int(input("Enter key (2): "))
        if key2 > 10 ** 40:
            key2 = 10 ** 40
        if key <= key2:
            key = int('c you')
    except:
        print("Please enter a number or ensure Key 1 > Key 2")
        return choice()

    user_choice = input("Encrypt (ec) or Decrypt (dc)? ").lower()

    if user_choice == "ec":
        text_to_encrypt = input("Enter text to encrypt: ")
        return ec(text_to_encrypt, key, key2, 1)
    elif user_choice == "dc":
        text_to_decrypt = input("Enter text to decrypt: ")
        return dc(text_to_decrypt, key, key2, 1)
    else:
        print("Invalid choice")
        return choice()

# Run 
result = choice()
if result:
    print(result)
input()
