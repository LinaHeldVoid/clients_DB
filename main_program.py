import functions_module
from functions_module import conn


def main():
    while True:
        choice = input('Каким будет вам следующий шаг? ' + '\n'
                       '1) Добавить нового клиента' + '\n'
                       '2) Изменить номер телефона у существующего клиента' + '\n'
                       '3) Изменить данные о существующем клиенте' + '\n'
                       '4) Удалить номер телефона для существующего клиента' + '\n'
                       '5) Удалить клиента из базы' + '\n'
                       '6) Найти клиента по внесённым данным' + '\n'
                       '7) Завершить работу' + '\n')
        if choice.isnumeric() == 1:
            choice = int(choice)
        else:
            print('Пожалуйста, введите ответ цифрой')
            continue
        if choice == 1:
            functions_module.new_client()
            conn.commit()
        elif choice == 2:
            functions_module.add_phone_number()
            conn.commit()
        elif choice == 3:
            functions_module.change_data()
            conn.commit()
        elif choice == 4:
            functions_module.delete_number()
            conn.commit()
        elif choice == 5:
            functions_module.delete_client()
            conn.commit()
        elif choice == 6:
            functions_module.show_data()
        elif choice == 7:
            conn.commit()
            conn.close()
            print('Программа завершает свою работу.')
            exit()
        else:
            print('Ваш ответ не распознан.')
            continue


if __name__ == "__main__":
    functions_module.create_tables()
    print('Приветствуем! Эта программа умеет создавать базу данных и записывать туда данные о клиентах.')
    functions_module.new_client()
    conn.commit()
    print('Первый клиент успешно добавлен!')
    main()
