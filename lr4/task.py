import random
import os

# ==========================================
# МАТЕМАТИЧЕСКИЙ АППАРАТ RSA
# ==========================================

def gcd(a, b):
    """Классический алгоритм Евклида для нахождения НОД (наибольшего общего делителя)"""
    while b != 0:
        a, b = b, a % b
    return a

def is_coprime(a, b):
    """Проверка, являются ли числа взаимно простыми (Требование из задания)"""
    return gcd(a, b) == 1

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для поиска секретной экспоненты d"""
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(e, phi):
    """Нахождение мультипликативного обратного (числа d)"""
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Обратного значения не существует')
    else:
        return x % phi

def generate_keypair(p, q):
    """Генерация ключей RSA на основе двух простых чисел"""
    n = p * q
    phi = (p - 1) * (q - 1)

    # Выбираем e: случайное число, взаимно простое с phi
    e = random.randrange(2, phi)
    
    # Требование методички: проверка взаимной простоты
    while not is_coprime(e, phi):
        e = random.randrange(2, phi)

    # Вычисляем d
    d = mod_inverse(e, phi)
    
    # Возвращаем (Открытый ключ, Секретный ключ)
    return ((e, n), (d, n))

# ==========================================
# ФУНКЦИИ ШИФРОВАНИЯ И ДЕШИФРОВАНИЯ
# ==========================================

def encrypt(pk, plaintext):
    """Шифрование текста (разбиваем на символы)"""
    key, n = pk
    # Для каждого символа переводим его в Unicode число (ord) и возводим в степень e по модулю n.
    # Используем встроенный pow(m, e, n) — это ответ на 4-й контрольный вопрос!
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    """Дешифрование массива чисел"""
    key, n = pk
    # Возводим каждое зашифрованное число в степень d по модулю n и переводим обратно в символ (chr)
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

# ==========================================
# ДРАЙВЕР ПРОГРАММЫ (Выполнение задания)
# ==========================================
def main():
    # 1. Выбираем два простых числа p и q (в реальности они генерируются спец. алгоритмами)
    # Выберем их так, чтобы n > 1104 (максимальный код кириллицы в Unicode), 
    # чтобы мы могли кодировать русские буквы по одной.
    p = 61
    q = 53
    
    print(f"1. Выбраны простые числа: p = {p}, q = {q}")
    
    # 2. Генерация ключей
    public, private = generate_keypair(p, q)
    print(f"2. Сгенерирован Открытый ключ (e, n): {public}")
    print(f"   Сгенерирован Секретный ключ (d, n): {private}")
    
    # 3. Исходное сообщение (достаточно длинное, как требует задание)
    message = input("введите чё-нибудь:\n- ")
    print(f"\n3. Исходное сообщение:\n'{message}'\n")
    
    # 4. Шифрование
    encrypted_msg = encrypt(public, message)
    # Зашифрованный текст - это массив больших чисел. Склеим их через пробел для вывода.
    encrypted_str = ' '.join(map(str, encrypted_msg))
    print(f"4. Зашифрованное сообщение (числа C):\n{encrypted_str}\n")
    
    # Требование методички: записать шифр в самостоятельный файл
    filename = "rsa_cipher.txt"
    with open(filename, 'w') as f:
        f.write(encrypted_str)
    print(f"   [ИНФО] Зашифрованный текст сохранен в файл '{filename}'")
    
    # 5. Чтение из файла и дешифрование
    with open(filename, 'r') as f:
        read_encrypted_str = f.read()
    
    # Преобразуем строку из файла обратно в список чисел
    cipher_array = list(map(int, read_encrypted_str.split()))
    
    decrypted_msg = decrypt(private, cipher_array)
    print(f"\n5. Расшифрованное сообщение (с использованием секретного ключа):\n'{decrypted_msg}'")
    
    # Удаление временного файла (опционально, можно закомментировать)
    os.remove(filename)

if __name__ == '__main__':
    main()