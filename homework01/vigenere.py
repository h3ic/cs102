def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    if len(plaintext) > len(keyword):
        keyword += keyword*((len(plaintext) // len(keyword))-1)
        keyword += keyword[:(len(plaintext) % len(keyword))]
    i = 0
    for ch in plaintext:
        if keyword[i].isupper():
            shift = ord(keyword[i])-65
        else:
            shift = ord(keyword[i])-97
        if ch.isupper():
            ciphertext += chr((ord(ch) + shift - 65) % 26 + 65)
        else:
            ciphertext += chr((ord(ch) + shift - 97) % 26 + 97)
        i += 1

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    return plaintext


#if __name__ == '__main__':
#   print(encrypt_vigenere('ATTACKATDAWN', 'LEMON'))