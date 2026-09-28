from break_caesar import LETTER_FREQUENCIES, chi_squared, break_caesar
from vigenere import cosets, decrypt

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def break_vigenere(ciphertext: str, key_length: int | None = None, max_key_length: int = 20, language: str = "en") -> tuple[str, str]:
    """
    Breaks a Vigenère cipher using coset frequency analysis.
    
    If key_length is provided, breaks the cipher for that specific key length m.
    If key_length is None, searches key lengths from 1 to max_key_length and 
    returns the key and plaintext that minimize the overall Chi-Squared statistic.
    """
    # Step A: Validate language selection
    if language not in LETTER_FREQUENCIES:
        raise ValueError(f"Unsupported language code '{language}'. Use 'en' or 'es'.")

    table = LETTER_FREQUENCIES[language]

    # Step B: If exact key length m is known, break directly
    if key_length is not None:
        if key_length <= 0:
            raise ValueError("Key length must be a positive integer.")
        return _break_vigenere_fixed_length(ciphertext, key_length, language)

    # Step C: Otherwise, search candidate key lengths from 1 to max_key_length
    best_key = ""
    best_plaintext = ""
    lowest_score = float("inf")

    # Ensure max_key_length does not exceed ciphertext length
    upper_bound = min(max_key_length, len(ciphertext))

    for m in range(1, upper_bound + 1):
        key_candidate, plain_candidate = _break_vigenere_fixed_length(ciphertext, m, language)
        score = chi_squared(plain_candidate, table)

        # Step D: Keep track of the key length that produces the lowest (best) Chi-Squared score
        if score < lowest_score:
            lowest_score = score
            best_key = key_candidate
            best_plaintext = plain_candidate

    return best_key, best_plaintext


def _break_vigenere_fixed_length(ciphertext: str, m: int, language: str) -> tuple[str, str]:
    """
    Helper function that breaks a Vigenère cipher for a known key length m.
    Splits the text into m interleaved cosets and solves each as an independent Caesar cipher.
    """
    # 1. Divide ciphertext into m interleaved cosets using cosets() from vigenere.py
    cipher_cosets = cosets(ciphertext, m)

    key_chars = []

    # 2. Break each coset independently using break_caesar()
    for coset in cipher_cosets:
        shift, _ = break_caesar(coset, language=language)
        key_chars.append(ALPHABET[shift])

    # 3. Assemble the full key string
    recovered_key = "".join(key_chars)

    # 4. Decrypt full ciphertext with the reconstructed key
    decrypted_plaintext = decrypt(ciphertext, recovered_key)

    return recovered_key, decrypted_plaintext