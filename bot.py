from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

import busio
import board

import adafruit_ads1x15.ads1115 as ads1115
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_htu21d import HTU21D

from dotenv import load_dotenv
import os

load_dotenv()

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)
ads = ads1115.ADS1115(i2c)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Temperature: %0.1f C" % sensor.temperature)
    await update.message.reply_text("Humidity: %0.1f %%" % sensor.relative_humidity)
    await update.message.reply_text("Analog in 1: %d" % AnalogIn(ads, ads1115.P0).value)
    await update.message.reply_text("Analog in 2: %d" % AnalogIn(ads, ads1115.P1).value)
    await update.message.reply_text("Analog in 3 (dry control): %d" % AnalogIn(ads, ads1115.P2).value)


app = Application.builder().token(os.getenv("TELEGRAM_API_KEY")).build()

app.add_handler(MessageHandler(filters.ALL, hello))

app.run_polling()
