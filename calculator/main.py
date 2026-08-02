import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        # Переменная для хранения выражения
        self.expression = ""
        self.input_var = tk.StringVar()
        self.create_widgets()
    def create_widgets(self):
        # Поле ввода
        input_frame = tk.Frame(self.window)
        input_frame.pack(expand=True, fill="both")
        
        input_field = tk.Entry(
            input_frame, 
            font=('Arial', 18), 
            textvariable=self.input_var, 
            justify='right',
            bd=10,
            relief=tk.RIDGE
        )
        input_field.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Кнопки
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(expand=True, fill="both")
        
        # Расположение кнопок
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['00', '0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                button = tk.Button(
                    buttons_frame,
                    text=button_text,
                    font=('Arial', 16),
                    command=lambda text=button_text: self.button_click(text),
                    relief=tk.RAISED,
                    bd=3
                )
                button.grid(
                    row=i, 
                    column=j, 
                    sticky="nsew", 
                    padx=2, 
                    pady=2,
                    ipadx=10,
                    ipady=10
                )
                
                # Делаем кнопку "=" выше других
                if button_text == '=':
                    button.config(bg='orange', fg='white')
                elif button_text in ['C', '⌫', '%', '/', '*', '-', '+']:
                    button.config(bg='lightgray')
        
        # Настройка весов для равномерного распределения
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def button_click(self, text):
        if text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '%':
            self.percentage()
        else:
            self.expression += str(text)
            self.input_var.set(self.expression)
    
    def calculate(self):
        try:
            # Заменяем символы для eval
            expression = self.expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            self.input_var.set(result)
            self.expression = str(result)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
            self.clear()
        except:
            messagebox.showerror("Ошибка", "Неверное выражение!")
            self.clear()
    
    def clear(self):
        self.expression = ""
        self.input_var.set("")
    
    def backspace(self):
        self.expression = self.expression[:-1]
        self.input_var.set(self.expression)
    
    def percentage(self):
        try:
            expression = self.expression.replace('×', '*').replace('÷', '/')
            result = eval(expression) / 100
            self.input_var.set(result)
            self.expression = str(result)
        except:
            messagebox.showerror("Ошибка", "Неверное выражение для процента!")
            self.clear()
    
    def run(self):
        self.window.mainloop()

# Запуск калькулятора
if __name__ == "__main__":
    calc = Calculator()
    calc.run()