# ==========================================
# ЛАБОРАТОРНАЯ РАБОТА 6: ШИФРОВАНИЕ ПАРОЛЕЙ
# ==========================================

# База данных пользователей (в реальности это файл или SQL-база)
# Формат: { "имя_пользователя": "зашифрованный_пароль_числом" }
database = {}

# --- ПАРАМЕТРЫ ДЛЯ МАТЕМАТИЧЕСКОЙ ФОРМУЛЫ ИЗ МЕТОДИЧКИ ---
# Формула: f(x) = (x^3 + a1*x^2 + a2*x + a3) mod P
P = 9973           # P - большое простое число
a1, a2, a3 = 5, 17, 31 # a - целые числа (секретные коэффициенты полинома)


def string_to_number(password_str):
    """
    Вспомогательная функция: превращает текстовый пароль в число X.
    Без этого мы не сможем подставить пароль в математическую формулу.
    """
    x = 0
    for char in password_str:
        # Сдвигаем число и прибавляем код символа. 
        # Это защищает от того, что "ab" и "ba" дадут одинаковую сумму.
        x = x * 256 + ord(char) 
    return x


def encrypt_password(password_str):
    """
    Главная функция: реализует метод "полиномиального необратимого представления" 
    строго по формуле из методички (п. 6.2.5).
    """
    # 1. Получаем число X из пароля
    x = string_to_number(password_str)
    
    # 2. Считаем полином: x^3 + a1*x^2 + a2*x + a3
    term0 = x ** 3
    term1 = a1 * (x ** 2)
    term2 = a2 * x
    term3 = a3
    
    sum_poly = term0 + term1 + term2 + term3
    
    # 3. Делаем необратимое преобразование (берем остаток от деления на P)
    encrypted_x = sum_poly % P
    
    return encrypted_x


# ==========================================
# ИНТЕРФЕЙС ПРОГРАММЫ (Режим диалога)
# ==========================================
def register_user():
    print("\n--- РЕГИСТРАЦИЯ ---")
    login = input("Придумайте логин: ")
    if login in database:
        print("[-] Ошибка: Такой пользователь уже существует!")
        return
        
    password = input("Придумайте пароль: ")
    
    # СИСТЕМА НЕ ХРАНИТ ПАРОЛЬ! Она его шифрует и сохраняет результат.
    encrypted_pass = encrypt_password(password)
    database[login] = encrypted_pass
    
    print(f"[+] Регистрация успешна!")
    print(f"[ДЛЯ ПРЕПОДАВАТЕЛЯ] В базу записано: {{'{login}': {encrypted_pass}}}")


def login_user():
    print("\n--- ВХОД В СИСТЕМУ ---")
    login = input("Введите логин: ")
    if login not in database:
        print("[-] Ошибка: Пользователь не найден!")
        return
        
    password = input("Введите пароль: ")
    
    # Шифруем введенный пароль тем же алгоритмом
    current_encrypted_pass = encrypt_password(password)
    
    # Сравниваем зашифрованные значения
    saved_encrypted_pass = database[login]
    
    if current_encrypted_pass == saved_encrypted_pass:
        print("[+] ДОСТУП РАЗРЕШЕН! Добро пожаловать, " + login)
    else:
        print("[-] ДОСТУП ЗАПРЕЩЕН! Неверный пароль.")


def main():
    while True:
        print("\n=== ПАРОЛЬНАЯ ЗАЩИТА ===")
        print("1. Регистрация нового пользователя")
        print("2. Вход в систему")
        print("3. Показать содержимое базы данных (для проверки)")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("\n[БАЗА ДАННЫХ]:")
            for user, pwd in database.items():
                print(f"Пользователь: {user} | Сохраненный Хэш: {pwd}")
        elif choice == '0':
            break
        else:
            print("Неверный ввод.")

if __name__ == '__main__':
    main()