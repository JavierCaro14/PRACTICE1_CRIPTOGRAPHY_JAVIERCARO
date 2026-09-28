from basics import to_letters, to_numbers

def encrypt(plaintext: str, k: int) -> str:
    nums = to_numbers(plaintext) 
    encrypted_nums = [(n + k) % 26 for n in nums] 
    return to_letters(encrypted_nums) 

def decrypt(ciphertext: str, k: int) -> str:
    nums = to_numbers(ciphertext) 
    decrypted_nums = [(n - k) % 26 for n in nums]
    return to_letters(decrypted_nums)

# encrypt("MYSECRETMESSAGE", 3)