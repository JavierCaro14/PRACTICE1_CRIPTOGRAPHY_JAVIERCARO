from basics import to_letters, to_numbers

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def key_from_keyword(keyword: str) -> str:
    """
    Generates a 26-letter substitution key from a keyword.
    Places unique letters of the keyword first, followed by remaining alphabet letters in order.
    """
    keyword = keyword.upper()
    key = ""
    
    # 1. Add unique letters from the keyword
    for char in keyword:
        if char in ALPHABET and char not in key:
            key += char
            
    # 2. Append remaining alphabet letters
    for char in ALPHABET:
        if char not in key:
            key += char
            
    return key


def _validate_key(key: str):
    """Ensures the key is a valid permutation of the 26-letter alphabet."""
    if len(key) != 26 or set(key) != set(ALPHABET):
        raise ValueError("The key must be a valid permutation of 26 unique uppercase letters.")


def encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts plaintext by substituting each letter with the character at its index in the key.
    """
    _validate_key(key)
    
    # Normalize input text to standard letter indices (A=0, B=1, ...)
    numbers = to_numbers(plaintext)
    
    # Map each number to the corresponding character in the substitution key
    ciphertext_chars = []
    for num in numbers:
        ciphertext_chars.append(key[num])
        
    return "".join(ciphertext_chars)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts ciphertext by looking up the position of each character inside the key.
    """
    _validate_key(key)
    
    # Normalize input ciphertext into uppercase letters
    cleaned_text = to_letters(to_numbers(ciphertext))
    
    # Find the original alphabet index by locating where each letter appears in the key
    original_numbers = []
    for char in cleaned_text:
        position = key.index(char)
        original_numbers.append(position)
        
    # Convert original numeric indices back to plaintext letters
    return to_letters(original_numbers)

# print(key_from_keyword("CRYPTO"))
# print(encrypt("HELLO", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
# print(encrypt("BOB", "MNBVCXZASDFGHJKLPOIUYTREWQ"))