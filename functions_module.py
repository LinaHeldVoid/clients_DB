import psycopg2

conn = psycopg2.connect(database="...", user="...", password="...")


# Создание таблиц
def create_tables():
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
        DROP TABLE phone_number;
        DROP TABLE email;
        DROP TABLE clients;
        """)

        # создание таблиц
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            second_name VARCHAR(40) NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS email(
            email VARCHAR(100) NOT NULL,
            client_id INTEGER NOT NULL REFERENCES clients(id)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            number VARCHAR(30),
            client_id INTEGER NOT NULL REFERENCES clients(id)
        );
        """)
        conn.commit()


# проверка на "нулевой ввод"
def zero_input_check(input_data):
    if len(input_data) == 0:
        print("Данная графа обязательна для заполнения! Попробуйте ещё раз.")
        par = 1
    else:
        par = 0
    return par


# неизвестная команда
def bad_input():
    print("Ваш ответ не распознан. Попробуйте ещё раз.")


# расшифрофка данных из БД:
def translate(data):
    for array in data:
        for number in array:
            return number


# смена данных клиента
def change_name(client_id, new_name):
    print(client_id)
    print(type(client_id))
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients 
        SET name = %s
        WHERE id = %s; 
        """, (new_name, client_id))
        conn.commit()
        print("Имя успешно изменено!")
        return


def change_second_name(client_id, new_data):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients 
        SET second_name = %s
        WHERE id = %s; 
        """, (new_data, client_id))
        conn.commit()
        print("Фамилия успешно изменена!")
        return


def change_email(client_id, new_email):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE email 
        SET email = %s
        WHERE client_id = %s; 
        """, (new_email, client_id))
        conn.commit()
        print("Email успешно изменён!")
        return


def append_phone_number(client_id):
    client_id = int(client_id)
    print(client_id)
    print(type(client_id))
    phone_list = phone_insert()
    with conn.cursor() as cur:
        for numbers in phone_list:
            cur.execute("""
            INSERT INTO phone_number VALUES(%s, %s);
            """, (numbers, client_id))
        conn.commit()
    print("Номер телефона успешно изменён!")
    return


# реализация множества или ни одного номера телефона
def phone_insert():
    phone_list = []
    while True:
        phone_number = input("Номер телефона: ")
        if zero_input_check(phone_number):
            continue
        phone_list.append(phone_number)
        choice1 = input("Принято. Желаете ввести другой номер телефона? ").lower()
        if zero_input_check(choice1):
            continue
        elif choice1.lower() == "да":
            continue
        elif choice1.lower() == "нет":
            return phone_list
        else:
            bad_input()
            continue


# поиск клиента в базе
def search_data(string, check_string, search_point, table):
    while True:
        if zero_input_check(search_point):
            continue
        else:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT %s FROM %s
                WHERE %s = %s;
                """, (string, table, check_string, search_point))
                check_list = cur.fetchall()
                print(check_list)
                if zero_input_check(check_list):
                    continue
                else:
                    data = translate(check_list)
                    if data is None:
                        print("Такой информации в реестре нет! Попробуйте ещё раз.")
                        continue
                    else:
                        return search_point


# поиск id по фамилии клиента
def get_id(data, table, search_point):
    with conn.cursor() as curr:
        curr.execute("""
        SELECT id FROM %s
        WHERE %s = %s;
        """, (table.replace('"', ""), data.replace('"', ""), search_point.replace('"', "")))
        client_id = curr.fetchall()
        client_id = translate(client_id)
    return client_id


# Добавить нового клиента
def new_client():
    # чтение данных пользователя
    print("Добавление нового клиента. Введите следующие данные:")
    while True:
        name = input("Имя: ")
        if zero_input_check(name) == 1:
            continue
        else:
            break
    while True:
        second_name = input("Фамилия: ")
        if zero_input_check(second_name):
            continue
        else:
            break
    while True:
        email = input("Email: ")
        if zero_input_check(email):
            continue
        else:
            break
    with conn.cursor() as cur:
        cur.execute("""
        SELECT MAX(id) FROM clients;
        """)
        client_id = cur.fetchall()
        data = translate(client_id)
        if data is None:
            i = 1
        else:
            i = data + 1
        cur.execute("""
        INSERT INTO clients VALUES(%s, %s, %s);
        """, (i, name, second_name))
        cur.execute("""
        INSERT INTO email VALUES(%s, %s);
        """, (email, i))
    while True:
        choice = input("Желаете ввести номер телефона?").lower()
        if choice.lower() == "да":
            phone_list = phone_insert()
            with conn.cursor() as curr:
                for numbers in phone_list:
                    curr.execute("""
                    INSERT INTO phone_number VALUES(%s, %s);
                    """, (numbers, i))
        elif choice.lower() == "нет":
            break
        else:
            bad_input()
            continue
    conn.commit()
    return


# Добавить номер телефона для существующего клиента
def add_phone_number():
    search_point = input("Введите фамилию клиента: ")
    search_point = search_data("second_name", "second_name", search_point, "clients")
    phone_list = phone_insert()
    client_id = get_id("second_name", "clients", search_point)
    with conn.cursor() as curr:
        for numbers in phone_list:
            curr.execute("""
            INSERT INTO phone_number VALUES(%s, %s);
            """, (numbers, client_id))
        conn.commit()
        response = "Номер телефона добавлен!"
        print(response)
        return


# изменение данных клиента
def change_data():
    search_point = input("Введите фамилию клиента: ")
    search_point = search_data("second_name", "second_name", search_point, "clients")
    client_id = get_id("second_name", "clients", search_point)
    while True:
        data = input("Какую информацию нужно изменить?" + "\n"
                     "1) Имя" + "\n"
                     "2) Фамилия" + "\n"
                     "3) Email" + "\n"
                     "4) Телефон" + "\n")
        if data.isnumeric() == 1:
            data = int(data)
        else:
            print("Пожалуйста, введите ответ цифрой")
            continue
        if data == 1:
            while True:
                new_name = input("Введите новое имя: ")
                if zero_input_check(new_name):
                    continue
                else:
                    change_name(client_id, new_name)
                    break
        elif data == 2:
            while True:
                new_second_name = input("Введите новую фамилию: ")
                if zero_input_check(new_second_name):
                    continue
                else:
                    change_second_name(client_id, new_second_name)
                    break
        elif data == 3:
            while True:
                new_email = input("Введите новый email: ")
                if zero_input_check(new_email):
                    continue
                else:
                    change_email(client_id, new_email)
                    return
        elif data == 4:
            append_phone_number(client_id)
            return
        else:
            bad_input()
            continue


# Удалить номер телефона для существующего клиента
def delete_number():
    search_point = input("Введите фамилию клиента: ")
    search_point = search_data("second_name", "second_name", search_point, "clients")
    client_id = get_id("second_name", "clients", search_point)
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s; 
        """, (client_id,))
        conn.commit()
    print("Номера телефонов для данного клиента удалены.")
    return


# Удалить клиента из базы
def delete_client():
    search_point = input("Введите фамилию клиента: ")
    search_point = search_data("second_name", "second_name", search_point, "clients")
    client_id = get_id("second_name", "clients", search_point)
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM clients
        WHERE client_id = %s; 
        """, (client_id,))
        cur.execute("""
        DELETE FROM email
        WHERE client_id = %s; 
        """, (client_id,))
        cur.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s; 
        """, (client_id,))
        conn.commit()
    print("Данные клиента удалены!")
    return


# Найти клиента по предоставленной информации
def show_data():
    while True:
        data = input("По каким данным нужно найти клиента?" + "\n"
                     "1) Имя" + "\n"
                     "2) Фамилия" + "\n"
                     "3) Email" + "\n"
                     "4) Телефон" + "\n")
        if data.isnumeric() == 1:
            data = int(data)
        else:
            print("Пожалуйста, введите ответ цифрой")
            continue
        if data == 1:
            while True:
                search_point = input("Введите имя: ")
                if zero_input_check(search_point):
                    continue
                else:
                    client_id = translate(get_id("name", "clients", search_point))
                    print(f"ID: {client_id}" + "\n")
                    name = translate(search_data("name", "name", search_point, "clients"))
                    print(f"Имя: {name}" + "\n")
                    second_name = translate(search_data("second_name", "name", search_point, "clients"))
                    print(f"Фамилия: {second_name}" + "\n")
                    email = translate(search_data("email", "client_id", client_id, "email"))
                    print(f"Email: {email}" + "\n")
                    phone_number = translate(search_data("number", "client_id", client_id, "phone_number"))
                    print(f"Номер телефона: {phone_number}" + "\n")
                    break
        elif data == 2:
            while True:
                search_point = input("Введите фамилию: ")
                if zero_input_check(search_point):
                    continue
                else:
                    client_id = translate(get_id("second_name", "clients", search_point))
                    name = translate(search_data("name", "second_name", search_point, "clients"))
                    second_name = translate(search_data("second_name", "second_name", search_point, "clients"))
                    email = translate(search_data("email", "client_id", client_id, "email"))
                    phone_number = translate(search_data("number", "client_id", client_id, "phone_number"))
                    print(f"ID: {client_id}" + "\n")
                    print(f"Имя: {name}" + "\n")
                    print(f"Фамилия: {second_name}" + "\n")
                    print(f"Email: {email}" + "\n")
                    print(f"Номер телефона: {phone_number}" + "\n")
                    break
        elif data == 3:
            while True:
                search_point = input("Введите email: ")
                if zero_input_check(search_point):
                    continue
                else:
                    client_id = translate(get_id("email", "email", search_point))
                    name = translate(search_data("name", "id", client_id, "clients"))
                    second_name = translate(search_data("second_name", "id", client_id, "clients"))
                    email = translate(search_data("email", "client_id", client_id, "email"))
                    phone_number = translate(search_data("number", "client_id", client_id, "phone_number"))
                    print(f"ID: {client_id}" + "\n")
                    print(f"Имя: {name}" + "\n")
                    print(f"Фамилия: {second_name}" + "\n")
                    print(f"Email: {email}" + "\n")
                    print(f"Номер телефона: {phone_number}" + "\n")
                    return
        elif data == 4:
            while True:
                search_point = input("Введите номер телефона: ")
                if zero_input_check(search_point):
                    continue
                else:
                    client_id = translate(get_id("phone_number", "number", search_point))
                    name = translate(search_data("name", "id", client_id, "clients"))
                    second_name = translate(search_data("second_name", "id", client_id, "clients"))
                    email = translate(search_data("email", "client_id", client_id, "email"))
                    phone_number = translate(search_data("number", "client_id", client_id, "phone_number"))
                    print(f"ID: {client_id}" + "\n")
                    print(f"Имя: {name}" + "\n")
                    print(f"Фамилия: {second_name}" + "\n")
                    print(f"Email: {email}" + "\n")
                    print(f"Номер телефона: {phone_number}" + "\n")
                    return
        else:
            bad_input()
            continue
