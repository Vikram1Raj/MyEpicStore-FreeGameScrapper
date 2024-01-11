import time
from datetime import datetime
import pyautogui as pag

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import pywhatkit as kit
import logging

# Configure the logger
logging.basicConfig(filename='script.log', level=logging.INFO)

url = 'https://store.epicgames.com/en-US/'

options = Options()
options.headless = True

#Main Code
driver = webdriver.Firefox(options=options)
driver.get(url)

time.sleep(0.1)

game_title = driver.find_elements(By.CLASS_NAME, "css-1h2ruwl")
game_state = driver.find_elements(By.CLASS_NAME, "css-nf3v9d")

try:
  if len(game_title) >= 1:
    latest_game_state = game_state[4].text
    latest_game_title = game_title[0].text

    if len(game_title) >= 2:
      next_game_title = game_title[1].text
    else:
      next_game_title = "No Game"
    # Extract the date and time from the game_state
    availability_date, availability_time = latest_game_state.split(' - ')[-1].split(' at ')
    logging.info(f"Availability_Date = {availability_date}")
    logging.info(f"Availability_Time = {availability_time}")

    # Parse the availability date and time into a datetime object with the current year
    availability_datetime = datetime.strptime(f"{availability_date} {availability_time}", "%b %d %I:%M %p")
    availability_datetime = availability_datetime.replace(year=datetime.now().year)

    logging.info(f"Availability_datetime = {availability_datetime}")

    #Format YYYY-MM-DD Hr:Min:Sec
    today_date = datetime.now().replace(second=0, microsecond=0)
    logging.info(f"Today_date = {today_date}")

    TimeDifference = availability_datetime - today_date

    DaysDifference = TimeDifference.days

    if availability_datetime.date() >= today_date.date():
      logging.info(f"Game available today:{latest_game_title}")
      message = f"New game available today: \"*{latest_game_title}*\" until _{availability_datetime}_ and the next game \"*{next_game_title}*\" will be available in _{DaysDifference}days_"

      try:
        kit.sendwhatmsg_instantly("+Number", message)
        time.sleep(1.8)
        pag.click(1723,998)
        logging.info("Message sent successfully.")
      except Exception as e:
        logging.error(f"Failed to send message: {e}")
  else:
    logging.error(f"No Free games found")

except:
  logging.error(f"Error! Check the Script")

driver.quit()
