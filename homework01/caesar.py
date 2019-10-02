def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    symbols = '1234567890.,/!@#$%^&*()_-+={}[] '
    for ch in plaintext:
        if ch in symbols:
            ciphertext += ch
        elif ch.isupper():
            ciphertext += chr((ord(ch) + 3 - 65) % 26 + 65)
        else:
            ciphertext += chr((ord(ch) + 3 - 97) % 26 + 97)

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    symbols = '1234567890.,/!@#$%^&*()_-+={}[] '
    for ch in ciphertext:
        if ch in symbols:
            plaintext += ch
        elif ch.isupper():
            plaintext += chr((ord(ch) - 3 - 65) % 26 + 65)
        else:
            plaintext += chr((ord(ch) - 3 - 97) % 26 + 97)

    return plaintext