from random import randint
with open('for_lesson7.txt', 'w', encoding='utf-8') as file:
    for i in range(100):
        a = randint(0, 100)
        file.write(f'{a}\n')
with open('for_lesson7.txt', 'r', encoding='utf-8') as file:
    numbers = {}
    for line in file:
        number = line.strip()
        if number in numbers:
            numbers[number] += 1
        else:
            numbers[number] = 1
print("Повторяющиеся числа:")
for number, count in numbers.items():
    if count > 1:
        print(f"Число {number} встречается {count} раза")