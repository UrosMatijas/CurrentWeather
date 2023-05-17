import requests
import tkinter
from datetime import datetime
from PIL import Image, ImageTk
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY1 = os.getenv('API_KEY_CITY')
API_KEY2 = os.getenv('API_KEY_WEATHER')

root = tkinter.Tk()
root.title("Current weather checker")
root.geometry("1000x600")

def lat_lon(key, cit):
    api_url = f"https://api.api-ninjas.com/v1/city?name={cit}"
    r_city = requests.get(api_url, headers={'X-Api-Key': key})
    r_city_json = r_city.json()
    return r_city_json

def check_temp():

    city = name_entry.get()
    lat = lat_lon(API_KEY1, city)[0]["latitude"]
    lon = lat_lon(API_KEY1, city)[0]["longitude"]

    if type_entry.get().lower() == "c":
        type = "metric"
    elif type_entry.get().lower() == "f":
        type = "imperial"
    elif type_entry.get().lower() == "k":
        type = "standard"

    r_weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}'
                             f'&appid={API_KEY2}&units={type}')
    data = r_weather.json()

    temp_label = tkinter.Label(text=f"Current temperature: {data['main']['temp']}", font=("Helvetica", 15))
    temp_label.grid(row=3, column=0, sticky="w")
    temp_max_label = tkinter.Label(text=f"Max temperature: {data['main']['temp_max']}", font=("Helvetica", 13))
    temp_max_label.grid(row=4, column=0, sticky="w")
    temp_min_label = tkinter.Label(text=f"Min temperature: {data['main']['temp_min']}", font=("Helvetica", 11))
    temp_min_label.grid(row=5, column=0, sticky="w")
    feels_like_label = tkinter.Label(text=f"Max temperature: {data['main']['feels_like']}", font=("Helvetica", 12))
    feels_like_label.grid(row=6, column=0, sticky="w")
    weather_label = tkinter.Label(text=f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
                                  font=("Arial", 20))
    weather_label.grid(row=7, column=0, sticky="w")

    clouds = data["clouds"]["all"]
    id = data["weather"][0]["id"]
    if datetime.now().hour > 20 or datetime.now().hour < 7:
        op_img = Image.open("venv/static/night.jpeg")
    elif id>=200 and id<300:
        op_img = Image.open("venv/static/thunderstorm.jpg")
    elif id>=300 and id<600:
        op_img = Image.open("venv/static/rain.jpg")
    elif id>=600 and id<700:
        op_img = Image.open("venv/static/snow.jpg")
    elif id>=700 and id<800:
        op_img = Image.open("venv/static/fog.jpg")
    elif id>=800:
        if clouds<35:
            op_img = Image.open("venv/static/sun.jpg")
        elif clouds<70:
            op_img = Image.open("venv/static/clouds1.jpg")
        else:
            op_img = Image.open("venv/static/clouds2.jpg")
    img = ImageTk.PhotoImage(op_img)
    canv.imgref = img
    canv.itemconfig(img_cont, image=img)

l1 = tkinter.Label(root, text="City:", font=("Helvetica", 20), padx=10, pady=10)
l1.grid(row=0, column=0, sticky="e")

name_entry = tkinter.Entry(root, width=30, font=("Helvetica", 16))
name_entry.grid(row=0, column=1, sticky="w")

l2 = tkinter.Label(root, text="Celsius(C), Fahrenheit(F) or Kelvin(K)?",font=("Helvetica", 20),
                   padx=10, pady=10)
l2.grid(row=1, column=0, sticky="e")

type_entry = tkinter.Entry(root, width=20, font=("Helvetica", 16))
type_entry.grid(row=1, column=1, sticky="w")

canv = tkinter.Canvas(root, width=500, height=500)
canv.grid(row=3, column=1, sticky="e", rowspan=8)
sat_img = Image.open("venv/static/earth.jpg")
img = ImageTk.PhotoImage(sat_img)
img_cont = canv.create_image(100, 100, image=img)

button = tkinter.Button(root, text="Check", font=("Helvetica", 15), command=check_temp)
button.grid(row=2, column=1, sticky="w")

root.mainloop()

