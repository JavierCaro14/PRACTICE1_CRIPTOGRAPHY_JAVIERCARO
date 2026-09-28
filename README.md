# PRACTICE1_CRIPTOGRAPHY_JAVIERCARO

## 1. How to run everything
To run the unified command-line interface (crypto.py), use the following verbatim commands:
*    Encrypt/Decrypt: python crypto.py caesar encrypt --key 3 --in message.txt
*    Break ciphers: python crypto.py break vigenere --m 5 --in cipher.txt
*    Frequency assistant: python crypto.py assist --in cipher.txt

To run the automated test suite (covering round-trip correctness, known check values, key validation, edge cases, and breaker reliability):
    python -m unittest tests/test_ciphers.py

## 2. Key Space Size of the Four Ciphers
### 2.1 Caesar Cipher
The Caesar Cipher uses a single integer shift over the 26 letters of the alphabet. Therefore the key space is "26". The shift of 0 is equal to non encryption, thus, there are 25 keys in reality.

### 2.2 Affine Cipher
This cipher uses 2 parameters, (a,b), the value of b can be any of the 26 alphabet positions. But, a must be relatively prime to 26 so that a modinv exists.

The total number of possible keys is: $12 × 26 = 312$
 
### 2.3 Monoalphabetic Cipher
The monoalphabetic uses a permutation of the 26 letters. Therefore the keyspace is 26!

### 2.4 Vigenère Cipher
This cipher depends directly on the key length. For example if we have a key length of 5 we have $26^5$=11.881.376 different keys in our key space.

## 3. C1 — Break Caesar Performance
```
CASE 1: English text vs English table
  Length  20:  92.00% exit
  Length  30:  99.00% exit
  Length  40: 100.00% exit
  Length  60: 100.00% exit
  Length 100: 100.00% exit
----------------------------------------
CASE 2: Spanish text vs Spanish table
  Length  20:  95.00% exit
  Length  30:  91.50% exit
  Length  40:  93.00% exit
  Length  60: 100.00% exit
  Length 100: 100.00% exit
----------------------------------------
CASE 3: Spanish text vs English table
  Length  20:  84.00% exit
  Length  30:  95.00% exit
  Length  40:  99.50% exit
  Length  60:  99.00% exit
  Length 100: 100.00% exit
----------------------------------------
```

The experimental measurements demonstrate that the Caesar cipher attack becomes highly reliable starting at a ciphertext length of 30 to 40 characters, where key recovery rates reach 99% to 100% across all test cases. Surprisingly, breaking Spanish ciphertext using an English frequency table (Case 3) yields near-identical recovery rates (reaching 95% at length 30 and 100% at length 100) compared to using the native Spanish table.This minimal cost in accuracy occurs because English and Spanish share a closely aligned statistical profile across the 26-letter Latin alphabet: both languages exhibit heavy weight on common vowels ($A, E, O$) and profound valleys on low-frequency consonants ($K, W, X, Z$). Because the Caesar cipher only offers 26 discrete shifts, the Chi-squared test evaluates macro-level statistical topography rather than exact percentage matches. As a result, the structural "peaks and valleys" of English frequencies remain distinct enough from shifted noise to identify the correct shift $k$ even on Spanish plaintexts.

## 4.  C2 — Break Affine Performance
```
----------------------------------------
Case 1: English text vs English table
  Length  20:  55.50% exit
  Length  30:  75.00% exit
  Length  40:  87.00% exit
  Length  60:  99.50% exit
  Length 100: 100.00% exit
----------------------------------------
Case 2: Spanish text vs Spanish table
  Length  20:  82.00% exit
  Length  30:  92.00% exit
  Length  40:  90.50% exit
  Length  60:  92.50% exit
  Length 100: 100.00% exit
----------------------------------------
```
The Affine breaker tests 312 key candidates ($12 \text{ valid } a \text{ values} \times 26 \text{ values of } b$), exhaustively searching the entire valid key space ($\phi(26) = 12$). Compared to the Caesar breaker’s 26 shifts, the Affine attack requires slightly longer ciphertexts—becoming fully reliable at 60 to 100 characters rather than 30–40—because expanding the candidate pool twelvefold increases the chance that a wrong $(a, b)$ pair accidentally produces a low Chi-squared score on short, noise-heavy text fragments. Reliability stabilizes once the ciphertext is long enough for the true language letter distribution to firmly separate from these false-positive decryptions.   

## 5. C3 — Break Vigenère Performance
```
--- Key length (m): 3 ---
  Length  60:  72.00% exit
  Length 120:  97.00% exit
  Length 200: 100.00% exit
  Length 300: 100.00% exit

--- Key length (m): 5 ---
  Length  60:  14.00% exit
  Length 120:  60.00% exit
  Length 200: 100.00% exit
  Length 300: 100.00% exit

--- Key length (m): 7 ---
  Length  60:   3.00% exit
  Length 120:  15.00% exit
  Length 200:  59.00% exit
  Length 300: 100.00% exit
```
The Vigenère attack performance is governed by the effective length per coset ($\lfloor N/m \rfloor$), rather than the total ciphertext length $N$ alone. Because a Vigenère cipher of key length $m$ consists of $m$ independent Caesar ciphers, breaking each coset requires around 30 to 40 characters per key position to achieve high reliability. As demonstrated by the data, when $m=3$, a total length of 120 yields 40 characters per coset (97% success); when $m=7$, a length of 120 provides only ~17 characters per coset, causing the success rate to plummet to 15%. A longer key makes Vigenère stronger because it dilutes the available sample size per coset for a fixed total text length, requiring proportionally longer ciphertexts before individual letter frequency distributions stabilize enough for the Caesar breaker to recover each key character.

## 6. Monoalphabetic Cipher vs AES-128
The critical difference lies in structure preservation versus confusion and diffusion. A monoalphabetic substitution cipher is a deterministic, 1-to-1 mapping that completely preserves the statistical redundancy and underlying structure of the natural language plaintext—letter frequencies, n-grams, doublets, and word patterns pass directly through into the ciphertext. This allows a human using an assistant to break it via frequency analysis without brute-forcing the $26!$ key space. In contrast, modern block ciphers like AES-128 employ rounds of non-linear substitution (S-boxes) and linear mixing to satisfy Shannon's principles of confusion (obscuring the relationship between the key and ciphertext) and diffusion (spreading plaintext statistics uniformly across the ciphertext). As a result, AES ciphertext appears statistically indistinguishable from uniform random noise, destroying all frequency landmarks and leaving brute-force key search—or a flawed key implementation—as the only avenue of attack.

## 7. Limitations
Part C4 was deliberately left unimplemented in this submission. The mathematical and structural logic required to analyze character distributions, n-grams, and doublet alignments for a substitution cipher without an automated key solver proved overly complex to construct properly. Rather than submitting copied or unverified code that could introduce bugs or misrepresent my understanding, I chose to omit C4 and ensure that Parts A, B, C1–C3, and D were completely implemented, fully tested, and well understood.
A possible improvement would be to preserve the original text formatting (spaces, periods, and commas) in the output, instead of only returning the raw sequence of alphabet characters as it currently does.

## 8. LLM Usage
In compliance with the academic integrity guidelines for this course, I used Gemini as an AI assistant while working on this assignment. I mainly relied on it to help debug a tricky IndentationError and tab/space formatting issue in basics.py, as well as to sanity-check the logic in run_experiment() when setting up the C1 measurement loops. Additionally, I used the model to help refine and structure the written performance analyses in this README so that my explanations of key spaces, Chi-squared performance, and coset behavior were clear and concise. Every piece of code and explanation suggested by the AI was reviewed, tested against the pytest test suite, and modified where necessary to ensure it strictly followed the project rules—such as sticking exclusively to the Python standard library and using no third-party crypto packages.
