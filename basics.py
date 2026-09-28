letter_to_num = {
    'A': 0,  'B': 1,  'C': 2,  'D': 3,  'E': 4,  'F': 5,  'G': 6,
    'H': 7,  'I': 8,  'J': 9,  'K': 10, 'L': 11, 'M': 12, 'N': 13,
    'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
    'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
}

def to_numbers(text: str) -> list[int]:
    """
    Normaliza el texto a mayúsculas, filtra cualquier carácter
    que no esté entre A y Z, y lo convierte a números.
    """
    resultado = []
    for c in text.upper():
        if c in letter_to_num:
            resultado.append(letter_to_num[c])
    return resultado

def to_letters(numbers: list[int]) -> str: # 0..25 -> text
    
    num_to_letter = {
    0: 'A',  1: 'B',  2: 'C',  3: 'D',  4: 'E',  5: 'F',  6: 'G',
    7: 'H',  8: 'I',  9: 'J',  10: 'K', 11: 'L', 12: 'M', 13: 'N',
    14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U',
    21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}
    resultado = []
    for number in numbers:
        letra = num_to_letter[number % 26]
        resultado.append(letra)
    return "".join(resultado)

print(to_letters([7, 4, 11, 11, 14, 22, 14, 17, 11, 3]))

def egcd(a: int, b: int) -> tuple[int, int, int]:
    # Adjust signs to garanty the compatibility with negative numbers
    sign_a = -1 if a < 0 else 1
    sign_b = -1 if b < 0 else 1
    
    a_abs, b_abs = abs(a), abs(b)
    
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    while b_abs != 0:
        q = a_abs // b_abs
        a_abs, b_abs = b_abs, a_abs % b_abs
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    return a_abs, x0 * sign_a, y0 * sign_b

def modinv(a: int, m: int) -> int:

    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"No existe inverso modular para a={a} mod {m} porque gcd({a}, {m}) = {g}")
    return x % m

def xor_bytes(data: bytes, key: bytes) -> bytes:   # key repeats cyclically
    if not key:
        raise ValueError("La clave no puede estar vacía.")
    
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data)) # This line iterates through each byte in data, pairs it with a cyclically repeated byte from key using modulo indexing (i % len(key)), performs a bitwise XOR operation (^) on each pair, and packages the resulting sequence back into a bytes object.(used help in this part but understood how it works)

# xor_bytes(b"HELLO", b"KEYKE").hex()
# print(modinv(5,26))
# print(modinv(7,26))
# print(modinv(17,26))
# print(modinv(13,26)) # first value error
# print(modinv(2,26)) # second value error