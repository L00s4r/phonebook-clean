phone_book = {}

while True:
    print("\n--- Телефонная книга ---")
    print("1. Добавить контакт")
    print("2. Найти контакт")
    print("3. Показать все контакты")
    print("4. Удалить контакт")    
    print("5. Изменить номер контакта")
    print("6. Выход")

    
    choice = input("Выберите действие (1-6): ")
    
    if choice == "1":
        name = input("Введите имя: ")
        if name in phone_book:
            print("Такой контакт уже есть!")
            continue
        phone = input("Введите номер телефона: ")
        if phone in phone_book.values():
            print("Такой номер уже есть")
            continue
        elif phone == "":
            print("Номер не может быть пустым!")
            continue
        phone_book[name] = phone
        print(f"Контакт {name} добавлен!")
        
    elif choice == "2":
        name = input("Введите имя для поиска: ")
        if name in phone_book:
            print(f"Номер {name}: {phone_book[name]}")
        else:
            print("Контакт не найден!")
            
    elif choice == "3":
        if phone_book:
            print("\nВсе контакты:")
            for name, phone in phone_book.items():
                print(f"{name}: {phone}")
        else:
            print("Телефонная книга пуста!")
            
    elif choice == "4":
        name = input("Введите имя для удаления: ")
        if name in phone_book:
            del phone_book[name]
            print(f"Контакт {name} удален!")
        else:
            print("Контакт не найден!")
    elif choice == "5":
        name = input("Введите имя контакта: ")
        if name in phone_book:
            temp_phone = input("Введите новый номер: ")
            phone_book[name] = temp_phone
            print("Контакт успешно изменен!")
        else:
            print("Контакт не найден!")
    elif choice == "6":
        print("До свидания!")
        break
    else:
        print("Неверный выбор!")