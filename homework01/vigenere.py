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
    ciphertext = ''
    if len(plaintext) > len(keyword):
        keyword *= len(plaintext) // len(keyword)
        keyword += keyword[:(len(plaintext) % len(keyword))]
    for i, ch in enumerate(plaintext):
        if keyword[i].isupper():
            shift = ord(keyword[i]) - 65
        else:
            shift = ord(keyword[i]) - 97
        if ch.isupper():
            ciphertext += chr((ord(ch) + shift - 65) % 26 + 65)
        else:
            ciphertext += chr((ord(ch) + shift - 97) % 26 + 97)

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
    plaintext = ''
    if len(ciphertext) > len(keyword):
        keyword *= len(ciphertext) // len(keyword)
        keyword += keyword[:(len(ciphertext) % len(keyword))]
    for i, ch in enumerate(ciphertext):
        if keyword[i].isupper():
            shift = ord(keyword[i]) - 65
        else:
            shift = ord(keyword[i]) - 97
        if ch.isupper():
            plaintext += chr((ord(ch) - shift - 65) % 26 + 65)
        else:
            plaintext += chr((ord(ch) - shift - 97) % 26 + 97)

    return plaintext