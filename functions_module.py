import psycopg2

conn = psycopg2.connect(database='...', user='...', password='...')


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
        print('Данная графа обязательна для заполнения! Попробуйте ещё раз.')
        par = 1
    else:
        par = 0
    return par

# неизвестная команда
def bad_input():
    print('Ваш ответ не распознан. Попробуйте ещё раз.')


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
        print('Имя успешно изменено!')
        return


def change_second_name(client_id, new_data):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE clients 
        SET second_name = %s
        WHERE id = %s; 
        """, (new_data, client_id))
        conn.commit()
        print('Фамилия успешно изменена!')
        return


def change_email(client_id, new_email):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE email 
        SET email = %s
        WHERE client_id = %s; 
        """, (new_email, client_id))
        conn.commit()
        print('Email успешно изменён!')
        return


def change_phone_number(client_id):
    client_id = int(client_id)
    print(client_id)
    print(type(client_id))
    phone_list = phone_insert()
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE phone_number.client_id = %s; 
        """, (client_id, ))
        for numbers in phone_list:
            cur.execute("""
            INSERT INTO phone_number VALUES(%s, %s);
            """, (numbers, client_id))
        conn.commit()
        print('Телефон успешно изменён!')
        return


# реализация множества или ни одного номера телефона
def phone_insert():
    phone_list = []
    while True:
        phone_number = input('Номер телефона: ')
        if zero_input_check(phone_number):
            continue
        phone_list.append(phone_number)
        choice1 = input('Принято. Желаете ввести другой номер телефона? ').lower()
        if zero_input_check(choice1):
            continue
        elif choice1.lower() == 'да':
            continue
        elif choice1.lower() == 'нет':
            return phone_list
        else:
            bad_input()
            continue


# Добавить нового клиента
def new_client():
    # чтение данных пользователя
    print('Добавление нового клиента. Введите следующие данные:')
    while True:
        name = input('Имя: ')
        if zero_input_check(name) == 1:
            continue
        else:
            break
    while True:
        second_name = input('Фамилия: ')
        if zero_input_check(second_name):
            continue
        else:
            break
    while True:
        email = input('Email: ')
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
        choice = input('Желаете ввести номер телефона?').lower()
        if choice.lower() == 'да':
            phone_list = phone_insert()
            with conn.cursor() as curr:
                for numbers in phone_list:
                    curr.execute("""
                    INSERT INTO phone_number VALUES(%s, %s);
                    """, (numbers, i))
        elif choice.lower() == 'нет':
            break
        else:
            bad_input()
            continue
    conn.commit()
    return


# Добавить номер телефона для существующего клиента
def add_phone_number():
    while True:
        search_point = input('Введите фамилию клиента: ')
        if zero_input_check(search_point):
            continue
        else:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT second_name FROM clients;
                """)
                check_list = cur.fetchall()
                print(check_list)
                if zero_input_check(check_list):
                    continue
                else:
                    data = translate(check_list)
                    if data is None:
                        print('Такой фамилии в реестре нет! Попробуйте ещё раз.')
                        continue
                    else:
                        phone_list = phone_insert()
                        with conn.cursor() as cursor:
                            cursor.execute("""
                            SELECT id FROM clients WHERE second_name=%s;
                            """, search_point)
                            check_id = cursor.fetchall()
                            client_id = translate(check_id)
                        with conn.cursor() as curr:
                            for numbers in phone_list:
                                curr.execute("""
                                INSERT INTO phone_number VALUES(%s, %s);
                                """, (numbers, client_id))
                            conn.commit()
                            response = 'Номер телефона добавлен!'
                            print(response)
                            return


def change_data():
    while True:
        search_point = input('Введите фамилию клиента: ')
        with conn.cursor() as cur:
            cur.execute("""
            SELECT second_name FROM clients WHERE second_name=%s;
            """, search_point)
            search_point = cur.fetchall()
            true_input = translate(search_point)
            if true_input is None:
                print('Такой фамилии в реестре нет! Попробуйте ещё раз.')
                continue
            else:
                while True:
                    with conn.cursor() as curr:
                        curr.execute("""
                        SELECT id FROM clients
                        WHERE second_name = %s;
                        """, search_point)
                        client_id = curr.fetchall()
                        client_id = translate(client_id)
                    data = input('Какую информацию нужно изменить?' + '\n'
                                 '1) Имя' + '\n'
                                 '2) Фамилия' + '\n'
                                 '3) Email' + '\n'
                                 '4) Телефон' + '\n')
                    if data.isnumeric() == 1:
                        data = int(data)
                    else:
                        print('Пожалуйста, введите ответ цифрой')
                        continue
                    if data == 1:
                        new_name = input('Введите новое имя: ')
                        if zero_input_check(new_name):
                            continue
                        else:
                            change_name(client_id, new_name)
                            return
                    elif data == 2:
                        new_second_name = input('Введите новую фамилию: ')
                        if zero_input_check(new_second_name):
                            continue
                        else:
                            change_second_name(client_id, new_second_name)
                            return
                    elif data == 3:
                        new_email = input('Введите новый email: ')
                        if zero_input_check(new_email):
                            continue
                        else:
                            change_email(client_id, new_email)
                            return
                    elif data == 4:
                        change_phone_number(client_id)
                        return
                    else:
                        bad_input()
                        continue