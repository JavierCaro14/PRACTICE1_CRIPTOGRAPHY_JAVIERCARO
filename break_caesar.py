from caesar import decrypt
# 1. Frequency Tables & Citations

# English relative letter frequencies (A-Z)
# Citation: Lewand, Robert (2000). "Cryptological Mathematics". 
# Mathematical Association of America.
ENGLISH_FREQS: dict[str, float] = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

# Spanish relative letter frequencies (A-Z, normalized without Ñ or accents)
# Citation: Corpus de Referencia del Español Actual (CREA), 
# Real Academia Española (RAE).
SPANISH_FREQS: dict[str, float] = {
    'A': 0.1253, 'B': 0.0142, 'C': 0.0468, 'D': 0.0586, 'E': 0.1368,
    'F': 0.0069, 'G': 0.0101, 'H': 0.0070, 'I': 0.0625, 'J': 0.0044,
    'K': 0.0002, 'L': 0.0497, 'M': 0.0315, 'N': 0.0671, 'O': 0.0868,
    'P': 0.0251, 'Q': 0.0088, 'R': 0.0687, 'S': 0.0798, 'T': 0.0463,
    'U': 0.0393, 'V': 0.0090, 'W': 0.0001, 'X': 0.0022, 'Y': 0.0090,
    'Z': 0.0052
}

# Dictionary lookup mapping language identifiers to their respective frequency tables
LETTER_FREQUENCIES: dict[str, dict[str, float]] = {
    "en": ENGLISH_FREQS,
    "es": SPANISH_FREQS
}

# 2. Statistical Analysis Function

def chi_squared(text: str, table: dict[str, float]) -> float:
    """
    Calculates the normalized Chi-Squared statistic for a candidate string
    against an expected language frequency distribution.
    """
    # Step A: Count occurrences of each valid character present in the table
    counts: dict[str, int] = {}
    for char in text.upper():
        if char in table:
            counts[char] = counts.get(char, 0) + 1

    # Step B: Determine the total number of analyzed letters (N)
    n = sum(counts.values())
    if n == 0:
        return 0.0

    # Step C: Compute raw Chi-Squared sum: ∑ ((observed - expected)^2 / expected)
    raw_chi2 = 0.0
    for char, expected_prob in table.items():
        observed = counts.get(char, 0)
        expected = n * expected_prob
        if expected > 0:
            raw_chi2 += ((observed - expected) ** 2) / expected

    # Step D: Normalize by total text length (N) for cross-length comparability
    return raw_chi2 / n

# 3. Caesar Cipher Automated Breaker

def break_caesar(ciphertext: str, language: str = "en") -> tuple[int, str]:
    """
    Breaks a Caesar cipher by testing all 26 possible shift values and 
    returning the key and plaintext that minimize the Chi-Squared statistic.
    """
    # Step A: Validate language selection and retrieve frequency table
    if language not in LETTER_FREQUENCIES:
        raise ValueError(f"Unsupported language code '{language}'. Use 'en' or 'es'.")

    table = LETTER_FREQUENCIES[language]

    # Step B: Initialize tracking variables for the minimum score search
    best_shift = 0
    lowest_score = float("inf")
    best_plaintext = ""

    # Step C: Evaluate all 26 possible shift keys (0 through 25)
    for k in range(26):
        candidate_text = decrypt(ciphertext, k)
        score = chi_squared(candidate_text, table)

        # Step D: Keep track of the shift that produces the lowest (best) score
        if score < lowest_score:
            lowest_score = score
            best_shift = k
            best_plaintext = candidate_text

    # Step E: Return best key-plaintext pair
    return best_shift, best_plaintext