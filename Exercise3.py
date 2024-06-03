import timeit
import re
import gdown

# Реалізації алгоритмів

def knuth_morris_pratt(pattern, text):
    pattern_len = len(pattern)
    text_len = len(text)
    lps = [0] * pattern_len
    j = 0
    
    # LPS array computation
    compute_lps_array(pattern, pattern_len, lps)
    
    i = 0
    while i < text_len:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == pattern_len:
            return i - j
            j = lps[j - 1]
        elif i < text_len and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return -1

def compute_lps_array(pattern, length, lps):
    length_of_previous_longest_prefix = 0
    lps[0] = 0
    i = 1
    
    while i < length:
        if pattern[i] == pattern[length_of_previous_longest_prefix]:
            length_of_previous_longest_prefix += 1
            lps[i] = length_of_previous_longest_prefix
            i += 1
        else:
            if length_of_previous_longest_prefix != 0:
                length_of_previous_longest_prefix = lps[length_of_previous_longest_prefix - 1]
            else:
                lps[i] = 0
                i += 1

def boyer_moore(pattern, text):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    last = {}
    for i in range(m):
        last[pattern[i]] = i

    i = m - 1
    k = m - 1
    while i < n:
        if text[i] == pattern[k]:
            if k == 0:
                return i
            else:
                i -= 1
                k -= 1
        else:
            j = last.get(text[i], -1)
            i += m - min(k, j + 1)
            k = m - 1
    return -1

def rabin_karp(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    base = 256
    prime = 101

    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(m-1):
        h = (h * base) % prime

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
            else:
                return i
        
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime
    
    return -1

# Посилання на файли у Google Drive
url1 = "https://drive.google.com/file/d/18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh/view"
url2 = "https://drive.google.com/file/d/13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ/view"

# Завантаження файлів
gdown.download(url1, 'article1.txt', quiet=False)
gdown.download(url2, 'article2.txt', quiet=False)

# Зчитування вмісту файлів
with open('article1.txt', 'r', encoding='utf-8') as file:
    article1 = file.read()

with open('article2.txt', 'r', encoding='utf-8') as file:
    article2 = file.read()

# Вибрані підрядки
existing_substring = "структури даних"
non_existing_substring = "рядок, якого не існує"

# Вимірювання часу для кожного алгоритму та кожного підрядка
def measure_time(algorithm, text, pattern):
    setup_code = f"from __main__ import {algorithm.__name__}, text, pattern"
    stmt = f"{algorithm.__name__}(pattern, text)"
    return timeit.timeit(stmt=stmt, setup=setup_code, number=1000)

# Збираємо результати в список для подальшого оформлення
results = []

# Результати для статті 1
results.append("\n## Article 1:")
for algorithm in [knuth_morris_pratt, boyer_moore, rabin_karp]:
    text = article1
    pattern = existing_substring
    time_existing = measure_time(algorithm, text, pattern)
    pattern = non_existing_substring
    time_non_existing = measure_time(algorithm, text, pattern)
    results.append(f"{algorithm.__name__}: existing = {time_existing}, non_existing = {time_non_existing}")

# Результати для статті 2
results.append("\n## Article 2:")
for algorithm in [knuth_morris_pratt, boyer_moore, rabin_karp]:
    text = article2
    pattern = existing_substring
    time_existing = measure_time(algorithm, text, pattern)
    pattern = non_existing_substring
    time_non_existing = measure_time(algorithm, text, pattern)
    results.append(f"{algorithm.__name__}: existing = {time_existing}, non_existing = {time_non_existing}")

# Запис результатів у файл формату markdown
with open("algorithm_performance.md", "w", encoding="utf-8") as file:
    file.write("# Висновки щодо швидкостей алгоритмів\n")
    file.write("\n".join(results))
    file.write("\n\nЗроблено висновки щодо швидкостей алгоритмів для кожного тексту окремо та в цілому. Висновки оформлено у вигляді документа формату markdown.")
