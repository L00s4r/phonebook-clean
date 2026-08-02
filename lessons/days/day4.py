import json

FILE_NAME = "contacts.json"

def load_contacts():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_contacts(book):
    with open(FILE_NAME, "w") as f:
        json.dump(book, f, ensure_ascii=False, indent=2)

def add_contact(book, used_numbers):
    name = input("Введите имя: ").strip().title()
    if name in book:
        print("Такой контакт уже есть!")
        return
    
    phone = input("Введите номер телефона: ")
    if phone in used_numbers:
        print("Такой номер уже есть")
        return
    elif phone == "":
        print("Номер не может быть пустым!")
        return
    
    book[name] = phone
    used_numbers.append(phone)
    print(f"Контакт {name} добавлен!")

    save_contacts(book)

def find_contact(book):
    name = input("Введите имя для поиска: ").strip().title()
    if name in book:
        print(f"Номер {name}: {book[name]}")
    else:
        print("Контакт не найден!")

def show_all(book):
    if book:
        print("\nВсе контакты:")
        for name, phone in book.items():
            print(f"{name}: {phone}")
    else:
        print("Телефонная книга пуста!")

def delete_contact(book, used_numbers):
    name = input("Введите имя для удаления: ").strip().title()
    if name in book:
        used_numbers.remove(book[name])
        del book[name]
        print(f"Контакт {name} удален!")
        save_contacts(book)
    else:
        print("Контакт не найден!")

def edit_contact(book, used_numbers):
    name = input("Введите имя контакта: ").strip().title()
    if name not in book:
        print("Контакт не найден!")
        return
    
    old_phone = book[name]
    temp_phone = input("Введите новый номер: ")
    
    if temp_phone in used_numbers and temp_phone != old_phone:
        print("Этот номер уже занят!")
        return
    
    used_numbers.remove(old_phone)
    used_numbers.append(temp_phone)
    book[name] = temp_phone
    print(f"Номер контакта {name} изменен на: {temp_phone}")
    save_contacts(book)

def main():
    phone_book = load_contacts()  # Загружаем
    used_numbers = list(phone_book.values())
        
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
                add_contact(phone_book, used_numbers)
            elif choice == "2":
                find_contact(phone_book)
            elif choice == "3":
                show_all(phone_book)
            elif choice == "4":
                delete_contact(phone_book, used_numbers)
            elif choice == "5":
                edit_contact(phone_book, used_numbers)
            elif choice == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор!")

if __name__ == "__main__":
    main()