# Лабораторная работа №2. Метод гаммирования (Вариант 7)
# Линейный конгруэнтный датчик ПСЧ, b = 6

# алфавит из 64 символов (2^6), чтобы покрыть все значения от 0 до 63.
#  пробел (0), А-Я (1-32), а-я (33-62, кроме ё), точка (63).
ALPHABET = " АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыь."

# b = 6
b = 6
M = 2 ** b  # M = 64

# параметры датчика ПСЧ
# A mod 4 должно быть равно 1 (например 17), C - нечетное (например 11).
A = 17
C = 11
T_0 = 7  # seed

def char_to_int(char):
    """Переводит символ в его числовое значение (индекс в алфавите)"""
    if char in ALPHABET:
        return ALPHABET.index(char)
    return 0 # нет в алфавите, заменяем пробелом

def int_to_char(val):
    """Переводит числовое значение обратно в символ"""
    # 0-63
    return ALPHABET[val % M]

def to_bin(val):
    """Переводит число в 6-битную двоичную строку (для красивого вывода)"""
    return f"{val:06b}"

def generate_gamma(seed, a, c, m, length):
    """Генерация гаммы шифра с помощью линейного конгруэнтного датчика (ЛКГ)"""
    gamma = []
    t = seed
    for _ in range(length):
        t = (a * t + c) % m
        gamma.append(t)
    return gamma

def apply_gamma(data_ints, gamma_ints):
    """Наложение гаммы (XOR - сложение по модулю 2).
       Функция едина как для шифрования, так и для дешифрования."""
    result = []
    for i in range(len(data_ints)):
        # XOR
        result.append(data_ints[i] ^ gamma_ints[i])
    return result

def main():
    # 1. исходные 
    original_text = input("введите чё-нибудь:\n- ")
    print(f"Исходный текст: '{original_text}'\n")

    # в двоичный 
    text_ints = [char_to_int(c) for c in original_text]
    text_bins = [to_bin(val) for val in text_ints]

    # 2. гамма
    gamma_ints = generate_gamma(T_0, A, C, M, len(original_text))
    gamma_bins = [to_bin(val) for val in gamma_ints]

    # 3. шифрование (XOR исходных и гаммы)
    encrypted_ints = apply_gamma(text_ints, gamma_ints)
    encrypted_bins = [to_bin(val) for val in encrypted_ints]
    
    # другие символы
    encrypted_text = "".join([int_to_char(val) for val in encrypted_ints])

    print("--- ПРОЦЕСС ШИФРОВАНИЯ ---")
    print(f"Текст (двоичный): {' '.join(text_bins)}")
    print(f"Гамма (двоичная): {' '.join(gamma_bins)}")
    print("                  " + "-" * (len(original_text) * 7 - 1))
    print(f"Шифр  (двоичный): {' '.join(encrypted_bins)}")
    print(f"\nЗашифрованный текст: '{encrypted_text}'\n")

    # 4. декод (XOR шифротекста и ТОЙ ЖЕ самой гаммы)
    decrypted_ints = apply_gamma(encrypted_ints, gamma_ints)
    decrypted_bins = [to_bin(val) for val in decrypted_ints]
    decrypted_text = "".join([int_to_char(val) for val in decrypted_ints])

    print("--- ПРОЦЕСС ДЕШИФРОВАНИЯ ---")
    print(f"Шифр  (двоичный): {' '.join(encrypted_bins)}")
    print(f"Гамма (двоичная): {' '.join(gamma_bins)}")
    print("                  " + "-" * (len(original_text) * 7 - 1))
    print(f"Текст (двоичный): {' '.join(decrypted_bins)}")
    print(f"\nРасшифрованный текст: '{decrypted_text}'")

if __name__ == "__main__":
    main()