#-------------------------------------------------------------------------------
# Name: Patrick Cockrill
# Project 3
# Due Date: Sunday, March 3rd, 2019
#-------------------------------------------------------------------------------

def tally(letter, text):
    count = 0
    # Simply just counts the total number of occurences of the 'letter' in the 'text'
    for i in text.lower():
        if letter == i:
            # For every occurence add 1
            count += 1
    return count

def frequency(text):
    # Initially we assign an empty list to later append to when we get counts of characters
    count = []
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s',\
        't','u','v','w','x','y','z']
    # For every letter in the alphabet parse through it to add to the letters count
    for letter in alphabet:
        if tally(letter,text.lower()) == 0:
            count.append(0)
        else:
            count.append(tally(letter,text.lower()))
    return count

def common(frequencies):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s',\
        't','u','v','w','x','y','z']
    charCommons = ()
    charCount = 0

    for i in frequencies:
        if i > 0:
            charCount += i

    index = 0
    for char in alphabet:
        if frequencies[index] / (charCount) >= 0.10:
            charCommons += (char, )
        index += 1
    return charCommons

# Helper function, that serve as calls for cipher functions, to reduce nests.
def alph_index(index):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for char in range(len(alphabet)):
        # For every character in the alphabet if it doesnt equal the index return it
        if not alphabet[char] != index:
            return char
# ----------------------------------------------------------------------------

def atbash_cipher(plaintext):
    # Assign variables for the cipher Alphabet and the return value newString
    cipherText = "zyxwvutsrqponmlkjihgfedcba"
    newString = ""

    for char in plaintext:
        # For character in parameter plaintext concatenate to newStrings by changing
        # regular alphabet index to its cipher index
        newString += cipherText[alph_index(char)]
    return newString

def caesar_cipher(plaintext, shift):
    # Assigning the alphabet and the shifted string to initial values
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shiftString = ""

    for char in plaintext:
        # For the index of the character in the alphabet, refer to function above
        place = alph_index(char)
        place += shift

        # If the place of the character is greater than 0 then apply 26
        while place < 0:
            place += 26
        # While its index is higher than the alphabet char count then reset it back to 0 index
        while place > 25:
            place -= 26

        # Concatenate to the variable shiftString of the place
        shiftString += alphabet[place]
    return shiftString

def text_reversal(text):
    #reversing the input of text
    revString = ""
    #find the last index of the text by using length
    indexCount = len(text)
    # For the positions that are working backwards from the last index in the text
    for pos in range(indexCount):
        # the reversed values will be added to revString in reversed order
        # subtract 1 to get the last index in text
        posIncrement = text[(indexCount - 1) - pos]
        revString += posIncrement
    return revString

def backwards_cipher(plaintext, key):
    # Two empty string assignments that serve as segue's to the final value of ciphString
    ciphString = ""
    reverse = ""
    # indexLength determines the length of the plaintext received at input
    index = 0
    # A loop that runs while the index (initally 0) is less than the length
    while index < (len(plaintext)):
        if index % key == 0 and not index == 0:
            #if condition is true, we add reversed temporary string to result
            ciphString += text_reversal(reverse)
            #we reset the temp string
            reverse = ""
        # if we do not split collumns, we add character as given index in text to temporary string
        reverse += plaintext[index]
        index += 1
    # If there is not Nothing in the string than we'll concatendate the string to a reversal of
    # the string
    if reverse != None:
        ciphString += text_reversal(reverse)
    return ciphString

def fence_cipher(plaintext):
    # Assign the two different rails of the cipher
    railOne = ""
    railTwo = ""

    for index in range(len(plaintext)):
        # If the index of the plaintext is even then concatenate to railOne
        if index % 2 == 0:
            railOne += plaintext[index]
        # Elif the index of the plaintext is odd then concatenate to railTwo
        elif index % 2 == 1:
            railTwo += plaintext[index]
        else:
            break

    # Assign a variable to the addition of the two rails to form one string
    ciphString = railOne + railTwo
    return ciphString

def column_cipher(plaintext):
    # Assigning ciphString to an empty string
    ciphString = ""
    # Length of the plaintext string
    length = len(plaintext)

    # For the index of the plaintext for every 5 steps
    for index in range(0,5):
        # Assign a sequence variable to apply the start,stop,jump rules
        sequence = plaintext[index:length:5]
        # Concatenate to the empty ciphString starting at the index, end at length, and jump 5
        ciphString += sequence

    return ciphString
