from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime

## Global variableS ##

BOTTOKEN: Final = "PLACEHOLDER"
BOT_USERNAME: Final = "PLACEHOLDER"
API_KEY = "PLACEHOLDER"

## weatherapp start ##

def get_weatherdata(location):

    city = location.title()

    geo_data = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")

    lat = geo_data.json()[0]["lat"]

    lon = geo_data.json()[0]["lon"]

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    weathercondition = weather_data.json()["weather"][0]["main"]
    weatherdescription = weather_data.json()["weather"][0]["description"]
    temperature = weather_data.json()["main"]["temp"]
    humidity = weather_data.json()["main"]["humidity"]
    air_pressure = weather_data.json()["main"]["pressure"]
    visibility = weather_data.json()["visibility"]
    if visibility >= 10000:
        visibility = "perfect."

    else: 
        visibility = str(visibility) + " meters."

    weathercondition = weathercondition.lower()


    weather_response = ("It is " + str(temperature) + "° Celsius.\n\nThe current forecast for "+ (city) +" is " + (weathercondition) + "." + "\n\nThe air pressure is " + str(air_pressure) + " HPa. With a humidity of " + str(humidity) + "%. \n\nThe visibility is " + str(visibility))

    return weather_response

## wetterapp end ##

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, what do you need?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Haha there is no support lmao")

async def wetter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weatherdata = get_weatherdata()
    await update.message.reply_text(weatherdata)


# Antworten 

def handle_response(text: str):
    processed: str = text.lower()  

    if "hi" in processed:
        return "Hi" 

    if processed.startswith("weather for "):
        location = processed[12:]
        response = get_weatherdata(location)
         
        return response
    
    return "I didnt catch that, sorry..."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip
            response: str = handle_response(new_text)

            return response
        else:
            return 
        
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    app = Application.builder().BOTTOKEN(BOTTOKEN).build()
    print("starting bot...")

    # commands

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('wetter', wetter_command))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    

    # Errors
    app.add_error_handler(error)

    print("polling...")
    app.run_polling(poll_interval= 3)