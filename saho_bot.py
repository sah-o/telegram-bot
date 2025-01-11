import telebot
import os
import barcode
from barcode.writer import ImageWriter
from PIL import Image

API_TOKEN = '7639575774:AAFWIpo255rrkpcVZSRYD9c_3jqKZv6vKhQ'  # API Token provided by BotFather
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Send me a barcode number (1-9), and I will generate a barcode image for you!")

@bot.message_handler(func=lambda message: True)
def generate_barcode(message):
    # Get the last digit of the barcode number
    barcode_number = message.text[-1]  # The last digit (1-9)
    
    if barcode_number.isdigit() and 1 <= int(barcode_number) <= 9:
        barcode_data = barcode_number * 10  # Just an example of how to generate the barcode
        
        # Generate barcode image
        barcode_image = barcode.get_barcode_class('code128')(barcode_data, writer=ImageWriter())
        barcode_image_path = f"barcode_{barcode_number}.png"
        barcode_image.save(barcode_image_path)
        
        # Send the barcode image
        with open(barcode_image_path, 'rb') as barcode_file:
            bot.send_photo(message.chat.id, barcode_file)
        
        # Clean up the image after sending
        os.remove(barcode_image_path)
    else:
        bot.send_message(message.chat.id, "Please send a number between 1 and 9.")

bot.polling()
