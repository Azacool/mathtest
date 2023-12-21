import telebot
from telebot import types
from django.core.management import call_command
import os
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automobiles.settings')
import django
django.setup()

from avto.models import Avto
import random

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

math_test_keyboard = types.ReplyKeyboardMarkup(row_width=2)
math_test_keyboard.add(types.KeyboardButton('Addition'))
math_test_keyboard.add(types.KeyboardButton('Subtraction'))
math_test_keyboard.add(types.KeyboardButton('Multiplication'))
math_test_keyboard.add(types.KeyboardButton('Division'))

@bot.message_handler(commands=['cars'])
def show_all_cars(message):
    cars = Avto.objects.all()
    car_info = "\n".join([f"{car.model} - {car.year}" for car in cars])
    bot.send_message(message.chat.id, f"All Car Information:\n{car_info}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hey there! You initialized a math test bot. Choose a math operation from the keyboard below:", reply_markup=math_test_keyboard)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text.startswith('/'):
        if message.text == '/cars':
            show_all_cars(message)
        bot.send_message(message.chat.id, f"Received command: {message.text}")
    else:
        bot.send_message(message.chat.id, "I apologize, I only understand commands.") 

def generate_math_problem(operation):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    if operation == 'Addition':
        return f"What is {a} + {b}?", a + b
    elif operation == 'Subtraction':
        return f"What is {a} - {b}?", a - b
    elif operation == 'Multiplication':
        return f"What is {a} * {b}?", a * b
    elif operation == 'Division':
        return f"What is {a * b} / {b}?", a

@bot.message_handler(func=lambda message: True)
def handle_math_test(message):
    if message.text in ['Addition', 'Subtraction', 'Multiplication', 'Division']:
        operation = message.text
        problem, answer = generate_math_problem(operation)
        bot.send_message(message.chat.id, problem)
        bot.register_next_step_handler(message, check_answer, answer)

def check_answer(message, correct_answer):
    try:
        user_answer = float(message.text)
        if user_answer == correct_answer:
            bot.reply_to(message, "Correct! Well done.")
        else:
            bot.reply_to(message, f"Sorry, the correct answer is {correct_answer}. Try another one!")
    except ValueError:
        bot.reply_to(message, "Please enter a valid number.")

bot.infinity_polling()

