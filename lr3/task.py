import struct

# ==========================================
# ПАРАМЕТРЫ ВАРИАНТА № 7
# ==========================================
ROUNDS = 20          # Количество раундов
BLOCK_SIZE = 16      # Размер блока в байтах (128 бит)
MOD32 = 2**32        # Модуль для 32-битной арифметики

# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================
def ROL(val, shift):
    """Циклический сдвиг влево (ROtate Left) для 32-битного числа"""
    shift = shift % 32
    return ((val << shift) & (MOD32 - 1)) | (val >> (32 - shift))

def ROR(val, shift):
    """Циклический сдвиг вправо (ROtate Right) для 32-битного числа"""
    shift = shift % 32
    return (val >> shift) | ((val << (32 - shift)) & (MOD32 - 1))

def generate_round_keys(K1, K2, rounds):
    """Генерация ключей для каждого раунда Vi(K) = K1 ROL i + K2 ROR i"""
    keys = []
    # Раунды нумеруются с 1 до n (по методичке)
    for i in range(1, rounds + 1):
        Vi = (ROL(K1, i) + ROR(K2, i)) % MOD32
        keys.append(Vi)
    return keys

def F_function(X, V):
    """Образующая функция F. 
       Для варианта 7 - это 'Сложение' (арифметическое по модулю 2^32)"""
    return (X + V) % MOD32

# ==========================================
# ОСНОВНЫЕ АЛГОРИТМЫ ШИФРОВАНИЯ
# ==========================================
def encrypt_block(block, round_keys):
    """Шифрование одного 128-битного блока (16 байт)"""
    # Разбиваем 16 байт на 4 целых числа по 32 бита (Big Endian)
    X1, X2, X3, X4 = struct.unpack('>IIII', block)
    
    for i in range(ROUNDS):
        Vi = round_keys[i]
        
        # 1. Вычисляем функцию F
        F_val = F_function(X1, Vi)
        
        # 2. Наложение и сдвиг ветвей (строго по формулам методички)
        # Х1(i) = X2(i-1) XOR F(Vi)
        # Х2(i) = X3(i-1)
        # Х3(i) = X4(i-1)
        # Х4(i) = X1(i-1)
        new_X1 = X2 ^ F_val
        new_X2 = X3
        new_X3 = X4
        new_X4 = X1
        
        # Обновляем состояния для следующего раунда
        X1, X2, X3, X4 = new_X1, new_X2, new_X3, new_X4
        
    # Собираем 4 числа обратно в 16 байт
    return struct.pack('>IIII', X1, X2, X3, X4)

def decrypt_block(block, round_keys):
    """Дешифрование одного 128-битного блока"""
    X1_new, X2_new, X3_new, X4_new = struct.unpack('>IIII', block)
    
    # Для дешифрования ключи применяются в обратном порядке
    for i in reversed(range(ROUNDS)):
        Vi = round_keys[i]
        
        # Инвертируем сдвиг: восстанавливаем старые значения из новых
        X1 = X4_new
        X4 = X3_new
        X3 = X2_new
        
        # Функция F вычисляется от X1, который мы только что восстановили
        F_val = F_function(X1, Vi)
        
        # Восстанавливаем X2 с помощью свойства XOR: если A = B ^ C, то B = A ^ C
        X2 = X1_new ^ F_val
        
        # Обновляем для следующей итерации (двигаемся назад во времени)
        X1_new, X2_new, X3_new, X4_new = X1, X2, X3, X4
        
    return struct.pack('>IIII', X1_new, X2_new, X3_new, X4_new)

# ==========================================
# ДРАЙВЕР ПРОГРАММЫ
# ==========================================
def main():
    # Исходный текст (меньше или больше 16 байт - дополним пробелами)
    text = input("введите чё-нибудь:\n- ")
    print(f"Исходный текст: '{text}'")
    
    # Конвертируем в байты (используем cp1251 чтобы 1 символ = 1 байт)
    # и добиваем пробелами до кратности 16 байт
    data = text.encode('cp1251')
    pad_len = (BLOCK_SIZE - (len(data) % BLOCK_SIZE)) % BLOCK_SIZE
    data += b' ' * pad_len
    
    # Главный ключ 64 бита (разбит на K1 и K2 по 32 бита)
    K1 = 0x12345678
    K2 = 0x9ABCDEF0
    
    # Генерируем расписание ключей
    round_keys = generate_round_keys(K1, K2, ROUNDS)
    
    # ШИФРОВАНИЕ
    encrypted_data = b''
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        encrypted_data += encrypt_block(block, round_keys)
        
    print(f"Шифротекст (HEX): {encrypted_data.hex().upper()}")
    
    # ДЕШИФРОВАНИЕ
    decrypted_data = b''
    for i in range(0, len(encrypted_data), BLOCK_SIZE):
        block = encrypted_data[i:i+BLOCK_SIZE]
        decrypted_data += decrypt_block(block, round_keys)
        
    # Убираем пробелы, которыми добивали блок, и декодируем
    decrypted_text = decrypted_data.decode('cp1251').rstrip()
    print(f"Расшифр. текст: '{decrypted_text}'")

if __name__ == '__main__':
    main()