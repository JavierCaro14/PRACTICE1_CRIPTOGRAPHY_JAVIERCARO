from basics import egcd, to_letters, to_numbers, modinv

def valid_keys() -> list[tuple[int, int]]:
    keys = []
    for a in range(26):
        g, _, _ = egcd(a, 26)
        if g == 1:
            for b in range(26):
                keys.append((a, b))
    return keys

def encrypt(plaintext: str, a: int, b: int) -> str:
    a_mod = a % 26
    b_mod = b % 26
    
    # Validate that 'a' has the modular inverse in the module 26
    g, _, _ = egcd(a_mod, 26)
    if g != 1:
        raise ValueError(f"Invalid 'a' value ({a}): gcd({a_mod}, 26) = {g}, must be 1.")
    
    nums = to_numbers(plaintext)
    encrypted_nums = [(a_mod * x + b_mod) % 26 for x in nums]
    return to_letters(encrypted_nums)

def decrypt(ciphertext: str, a: int, b: int) -> str:
   # modinv validates if gcd(a,26) != 1 and gives a ValueError if it happens.
    a_inv = modinv(a, 26)
    
    nums = to_numbers(ciphertext)
    decrypted_nums = [(a_inv * (y - b)) % 26 for y in nums]
    return to_letters(decrypted_nums)
# encrypt("attack", 5, 8)