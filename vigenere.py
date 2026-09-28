from basics import to_letters, to_numbers
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _validate_key(key: str) -> list[int]:
    """Ensures the key is non-empty, contains only alphabetic characters, and returns its numeric values."""
    if not key or not key.isalpha():
        raise ValueError("The key must be a non-empty string containing only alphabetic characters.")
    return to_numbers(key)


def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts plaintext using the Vigenère cipher.
    Each character is shifted by the corresponding key letter (repeated cyclically).
    """
    key_nums = _validate_key(key)
    plain_nums = to_numbers(plaintext)
    
    # Add the shift from the cyclic key to each plaintext letter modulo 26
    cipher_nums = [
        (p + key_nums[i % len(key_nums)]) % 26 
        for i, p in enumerate(plain_nums)
    ]
    
    return to_letters(cipher_nums)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts ciphertext using the Vigenère cipher by subtracting key shifts.
    """
    key_nums = _validate_key(key)
    cipher_nums = to_numbers(ciphertext)
    
    # Subtract the shift of the cyclic key from each ciphertext letter modulo 26
    plain_nums = [
        (c - key_nums[i % len(key_nums)]) % 26 
        for i, c in enumerate(cipher_nums)
    ]
    
    return to_letters(plain_nums)


def cosets(ciphertext: str, m: int) -> list[str]:
    """
    Splits the ciphertext into m interleaved sub-sequences (cosets).
    The i-th coset contains letters enciphered with the i-th key position (0, m, 2m...).
    """
    if m <= 0:
        raise ValueError("Key length m must be a positive integer.")
        
    cleaned_text = to_letters(to_numbers(ciphertext))
    
    # Python slicing [start::step] grabs every m-th character starting from position i
    return [cleaned_text[i::m] for i in range(m)]

# print(encrypt("MYSECRETMESSAGE", "KEY"))
# print(encrypt("attackatdawn", "LEMON"))
# print(cosets("ABCDEF", 3))