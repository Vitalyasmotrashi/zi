import random


q = 251                  # простое 
p = 503                  # простое (p = 2*q + 1 -> q делит p-1)
a = 4                    # a > 1, a < p-1. a^q mod p должно быть = 1
# : 4^251 mod 503 = 1.

def get_hash(text):
    """
    количество '1' в битовом представлении символов текста.
    """
    count_ones = 0
    for char in text:
        # ord(char) дает код символа, bin() переводит в двоичную строку '0b110001...'
        count_ones += bin(ord(char)).count('1')
    return count_ones

# ==========================================
# 2. ГЕНЕРАЦИЯ КЛЮЧЕЙ
# ==========================================
def generate_keys():
    # x - Секретный ключ (от 1 до q-1)
    x = random.randint(1, q - 1)
    # y - Открытый ключ
    y = pow(a, x, p)
    return x, y

# ==========================================
# 3. ПРОЦЕДУРА СОЗДАНИЯ ПОДПИСИ (п. 5.2.2)
# ==========================================
def sign(message, x):
    # Шаг 1: Вычисляем хэш
    h = get_hash(message)
    if h % p == 0:
        h = 1
        
    while True:
        # Шаг 2: Выбираем случайное k
        k = random.randint(1, q - 1)
        
        # Шаг 3: Вычисляем r и r1
        r_temp = pow(a, k, p)
        r1 = r_temp % q
        
        if r1 == 0:
            continue # Возвращаемся к шагу 2 (по методичке)
            
        # Шаг 4: Вычисляем s
        s = (x * r1 + k * h) % q
        
        if s == 0:
            continue # Возвращаемся к шагу 2
            
        # Если всё ок, возвращаем подпись (пару чисел r1 и s)
        return r1, s

# ==========================================
# 4. ПРОЦЕДУРА ПРОВЕРКИ ПОДПИСИ (п. 5.2.3)
# ==========================================
def verify(message, signature, y):
    r1, s = signature
    
    # Шаг 1: Проверка границ
    if not (0 < r1 < q) or not (0 < s < q):
        print("[-] Ошибка: Подпись вне допустимого диапазона!")
        return False
        
    # Шаг 2: Вычисляем хэш полученного сообщения
    h = get_hash(message)
    if h % p == 0:
        h = 1
        
    # Шаг 3: Вычисляем v (возведение в степень по модулю)
    v = pow(h, q - 2, q)
    
    # Шаг 4: Вычисляем z1 и z2
    z1 = (s * v) % q
    z2 = ((q - r1) * v) % q
    
    # Шаг 5: Вычисляем u
    # Формула: u = ((a^z1 * y^z2) mod p) mod q
    # pow(a, z1, p) - это быстрое возведение a в z1 по модулю p
    part1 = pow(a, z1, p)
    part2 = pow(y, z2, p)
    u = ((part1 * part2) % p) % q
    
    # Шаг 6: Проверка равенства
    if u == r1:
        return True
    else:
        return False

# ==========================================
# ТЕСТИРОВАНИЕ И ВЫПОЛНЕНИЕ ЛАБЫ
# ==========================================
if __name__ == "__main__":
    print("=== ЛАБОРАТОРНАЯ РАБОТА: ЭЦП ГОСТ Р34.10-94 ===")
    
    # 1. Исходные данные
    text = "вот тут крч изначальный текст вооооот"
    print(f"\n[!] Исходное сообщение: '{text}'")
    
    hash_value = get_hash(text)
    print(f"[!] Хэш сообщения (кол-во единиц в битах): {hash_value}")
    
    # 2. Генерация ключей
    secret_key, public_key = generate_keys()
    print(f"\n[КЛЮЧИ]")
    print(f"Секретный ключ (x): {secret_key}")
    print(f"Открытый ключ (y): {public_key}")
    
    # 3. Подписываем сообщение
    signature = sign(text, secret_key)
    print(f"\n[ПОДПИСАНИЕ]")
    print(f"Подпись сгенерирована. Числа (r, s): {signature}")
    
    # 4. Проверяем правильность подписи
    print(f"\n[ПРОВЕРКА ВАЛИДНОЙ ПОДПИСИ]")
    is_valid = verify(text, signature, public_key)
    if is_valid:
        print("[+] УСПЕХ: Подпись верна! Авторство подтверждено.")
    else:
        print("[-] ОШИБКА: Подпись недействительна!")
        
    # 5. Имитируем атаку: хакер изменил текст!
    print(f"\n[АТАКА НА ТЕКСТ]")
    hacked_text = "это 100 проц не тот текст который уже подписан"
    print(f"Измененный текст: '{hacked_text}'")
    is_valid_hacked = verify(hacked_text, signature, public_key)
    if is_valid_hacked:
        print("[+] УСПЕХ: Подпись верна!")
    else:
        print("[-] УСПЕХ ЗАЩИТЫ: Подпись отвергнута (текст был изменен)!")

    # 6. Имитируем атаку: хакер изменил саму подпись
    print(f"\n[АТАКА НА ПОДПИСЬ]")
    fake_r, fake_s = signature
    fake_signature = (fake_r, fake_s + 1) # Испортили второе число на единичку
    print(f"Оригинальный текст, но поддельная подпись: {fake_signature}")
    is_valid_fake_sig = verify(text, fake_signature, public_key)
    if is_valid_fake_sig:
        print("[+] УСПЕХ: Подпись верна!")
    else:
        print("[-] УСПЕХ ЗАЩИТЫ: Подпись отвергнута (сама подпись повреждена)!")