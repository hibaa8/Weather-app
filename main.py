import tkinter as tk
from tkinter import font
from geopy.geocoders import Nominatim
from datetime import datetime
import requests
import urllib.request
import PIL

from PIL import ImageTk, Image, ImageDraw

root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=700)
canvas.pack()


def change_frame(frame):
    frame.place(relx=.05, rely=.05, relwidth=0.9, relheight=0.9)
    frame.tkraise()


def label(frame, text, size):
    label1 = tk.Label(frame, text=text, fg='white', bg='blue')
    label1.config(font=("sansserif", size))
    return label1


def app_settings():
    global frame1
    frame1 = tk.Frame(root, bg='blue')
    change_frame(frame1)
    title = label(frame1, 'Weather App Settings', 44)
    title.pack()

    city = label(frame1, 'City: ', 20)
    city.place(relx=0.27, rely=0.2, relheight=0.05)
    in_city = tk.Entry(frame1, font=('serif', 20))
    in_city.place(relx=0.32, rely=0.2, relwidth=0.4, relheight=0.05)

    country = label(frame1, 'Country: ', 20)
    country.place(relx=0.24, rely=0.4, relheight=0.05)
    in_country = tk.Entry(frame1, font=('serif', 20))
    in_country.place(relx=0.32, rely=0.4, relwidth=0.4, relheight=0.05)

    save_button = tk.Button(frame1, font=('serif', 15), fg='black', bg='white', text='Save',
                            command=lambda: get_data(in_city, in_country))
    save_button.place(relx=0.45, rely=0.6, relwidth=0.1)


def get_data(in_city, in_country):
    city = in_city.get()
    country = in_country.get()
    location = [city, country]
    print(location)
    get_weather(location)
    return location

weather_key = '' #hidden 


def get_weather(in_location):
    city = in_location[0] + ', ' + in_location[1]
    locate = Nominatim(user_agent='weather_key = '505339f29b05943380b4a2805cc0e1e4'hibaaltaf')
    find_coordinates = locate.geocode(city)
    latitude = find_coordinates.latitude
    longitude = find_coordinates.longitude

    url = 'https://api.openweathermap.org/data/2.5/onecall'
    get_request = requests.get(url,
                               params={'APPID': weather_key, 'lat': latitude, 'lon': longitude, 'units': 'imperial'})
    global weather
    weather = get_request.json()

    print(weather)

    city_name = 'City Name: ' + in_location[0].capitalize()
    conditions = 'Conditions: ' + str(weather['current']['weather'][0]['description'])
    temperature = 'Temperature: ' + str(round(weather['current']['temp'])) + 'F'
    feels_like = 'Feels Like: ' + str(round(weather['current']['feels_like'])) + 'F'
    wind_speed = 'Wind Speed: ' + str(round(weather['current']['wind_speed'])) + ' mph'
    visibility = 'Visibility: ' + str(round((weather['current']['visibility']) / 100)) + '%'
    humidity = 'Humidity: ' + str(round(weather['current']['humidity'])) + '%'
    weather_icon = weather['current']['weather'][0]['icon']
    current_weather = [city_name, conditions, temperature, feels_like, wind_speed, visibility, humidity, weather_icon]
    show_current_weather(current_weather)

    hourly_weather()
    get_daily_weather()
    return

def show_current_weather(in_list):
    global frame2
    frame2 = tk.Frame(root, bg='blue')
    change_frame(frame2)

    x = 0.05
    y = 0.05
    i = 0
    cw_background = tk.PhotoImage('white_background.jpg')
    cw_background_label = tk.Label(frame2, image=cw_background)
    cw_background_label.place(x=0, y=0, relwidth=.98, relheight=0.25, relx=0.01, rely=0.02)
    for i in range(0,7):
        label_i = tk.Label(frame2, text=in_list[i], fg='black', anchor='nw', justify='left', padx=0)
        label_i.config(font=('serif', 18, 'bold'))
        label_i.place(relx=x, rely=y)
        y += 0.05
        if y > 0.18:
            x += 0.28
            y = 0.05
        i += 1
    weather_icon = in_list[7]
    image_name = 'media/' + weather_icon + '.png'
    image = Image.open(image_name)
    image = image.resize((170, 170), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    img_label = tk.Label(frame2, image=image)
    img_label.image = image
    img_label.place(relx=0.8, rely=0.02)

    back_button = tk.Button(frame2, font=('serif', 15, 'bold'), fg='black', bg='white', text='Settings',
                            command=lambda: change_frame(frame1))
    back_button.place(relx=0.92, rely=0.02, relheight=0.05)


def hourly_weather():
    global two_day_weather
    two_day_weather = {}
    day_1 = []
    day_2 = []
    day_3 = []
    for i in range(48):
        timestamp = weather['hourly'][i]['dt']
        date = str(datetime.fromtimestamp(timestamp))
        formated_date = datetime.fromisoformat(str(date))
        hour = formated_date.hour
        date = date[:-9]
        if int(hour) > 12:
            hour = str(int(hour) - 12) + 'PM'
        elif int(hour) == 12:
            hour = str(int(hour)) + 'PM'
        else:
            hour = str(hour) + 'AM'
        temp = 'Temperature: {}F'.format(round(weather['hourly'][i]['temp']))
        feels_like = 'Feels Like: {}F'.format(round(weather['hourly'][i]['feels_like']))
        wind_speed = 'Wind Speed: {} mph'.format(round(weather['hourly'][i]['wind_speed']))
        conditions = str(weather['hourly'][i]['weather'][0]['description'])
        humidity = 'Humidity: {}%'.format(weather['hourly'][i]['humidity'])
        icon = weather['hourly'][i]['weather'][0]['icon']
        hourly_weather = [date, hour, temp, feels_like, conditions, wind_speed, humidity, icon]
        if date not in two_day_weather:
            two_day_weather[date] = ''
        dates_list = list(two_day_weather.keys())
        if hourly_weather[0] == dates_list[0]:
            day_1.append(hourly_weather)
        elif hourly_weather[0] == dates_list[1]:
            day_2.append(hourly_weather)
        else:
            day_3.append(hourly_weather)
    two_day_weather[dates_list[0]] = day_1
    two_day_weather[dates_list[1]] = day_2
    try:
        two_day_weather[dates_list[2]] = day_3
    except:
        pass

def get_daily_weather():

    for i in range(0, 6):
        timestamp = weather['daily'][i]['dt']
        date = 'Date: ' + str(datetime.fromtimestamp(timestamp))
        date = date[:-9]
        temperature = 'Temperature: ' + str(round(weather['daily'][i]['temp']['day'])) + 'F'
        min_temperature = 'Minimum: ' + str(round(weather['daily'][i]['temp']['min'])) + 'F'
        max_temperature = 'Maximum: ' + str(round(weather['daily'][i]['temp']['max'])) + 'F'
        humidity = 'Humidity: ' + str(round(weather['daily'][i]['humidity'])) + '%'
        wind_speed = 'Wind Speed: ' + str(round(weather['daily'][i]['wind_speed'])) + 'mph'
        conditions = str(weather['daily'][i]['weather'][0]['description'])
        cloud_cover = 'Cloud Cover: ' + str(round(weather['daily'][i]['clouds'])) + '%'
        icon = weather['daily'][i]['weather'][0]['icon']
        day_i = [date, temperature, min_temperature, max_temperature, humidity, wind_speed, conditions, cloud_cover,
                 icon]
        show_daily_weather(day_i)
    return

day_x = 0.01
def show_daily_weather(in_list):
    global day_x
    keys = list(two_day_weather.keys())
    for key in keys:
        if key in str(in_list[0]):
            pass_in = key
            command = lambda d=pass_in: hourly_weather_description(d)
            break
        else:
            command = None
    day_i_button = tk.Button(frame2, font=('serif', 15, 'bold'), fg='black', bg='white', anchor='n',
                         pady=10,
                         text="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(in_list[0], in_list[1], in_list[2], in_list[3],
                                                                      in_list[4], in_list[5], in_list[6], in_list[7]),
                         command=command)
    day_i_button.place(relwidth=.156, relheight=0.675, relx=day_x, rely=0.3)
    weather_icon = in_list[8]
    print(weather_icon)
    image_name = 'media/' + weather_icon + '.png'
    image = Image.open(image_name)
    image = image.resize((140, 140), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    img_label = tk.Label(frame2, image=image)
    img_label.image = image
    img_label.place(relx=day_x + 0.025, rely=0.7)
    day_x += 0.165


def hourly_weather_description(date):
    frame3 = tk.Frame(root, bg='blue')
    print(two_day_weather)
    hour_conditions = two_day_weather[date]
    print(hour_conditions)
    change_frame(frame3)
    x = 0.01
    y = 0.01

    length = len([i for i in hour_conditions if hour_conditions.index(i) < 12])

    height = (1 / 12) - 0.015
    for i in range(length):
        hour_bg = tk.PhotoImage('white_background.jpg')
        hour_bg_label = tk.Label(frame3, image=hour_bg)
        hour_bg_label.image = hour_bg
        hour_bg_label.place(relwidth=0.98, relheight=height, relx=x, rely=y)
        y += height + 0.01
    x = 0.01
    y = 0.01

    for hour in hour_conditions:
        if hour_conditions.index(hour) < 12:
            for j in range(1, 7):
                label_j = tk.Label(frame3, font=('serif', 15, 'bold'), fg='black', justify='left',
                                   text=hour[j])
                label_j.place(relx=x, rely=y)
                x += 0.16
            x = 0.925

            weather_icon = hour[7]
            print(weather_icon)
            image_name = 'media/' + weather_icon + '.png'
            image = Image.open(image_name)
            image = image.resize((50, 45), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            img_label = tk.Label(frame3, image=image)
            img_label.image = image
            img_label.place(relx=x, rely=y)

        x = 0.01
        y += height + 0.01

    back_button = tk.Button(frame3, font=('serif', 15, 'bold'), fg='black', bg='white', text='Back',
                            command=lambda: change_frame(frame2))
    back_button.place(relx=0.01, rely=0.95, relheight=0.05)

    next_button = tk.Button(frame3, font=('serif', 15, 'bold'), fg='black', bg='white', text='Next',
                            command=lambda: next_hours(date, two_day_weather))
    next_button.place(relx=0.95, rely=0.95, relheight=0.05)

    return


def next_hours(in_date, in_dict):
    n_x = 0.01
    n_y = 0.01
    in_list = two_day_weather[in_date]
    frame4 = tk.Frame(root, bg='blue')
    change_frame(frame4)

    length = len([i for i in in_list if in_list.index(i) >= 12])
    print(length)
    height = (1 / 12) - 0.015
    for i in range(length):
        hour_bg = tk.PhotoImage('white_background.jpg')
        hour_bg_label = tk.Label(frame4, image=hour_bg)
        hour_bg_label.image = hour_bg
        hour_bg_label.place(relwidth=0.98, relheight=height, relx=n_x, rely=n_y)
        n_y += height + 0.01
    keys = list(in_dict.keys())
    if in_date in keys[1]:
        n_y -= 0.991 + ((length + 1) * height)
    else:
        n_y -= 0.96 + (length * height)
    print(n_y)
    n_x = 0.01

    for hour in in_list:
        if in_list.index(hour) >= 12:
            for n in range(1, 7):
                label_n = tk.Label(frame4, font=('serif', 15, 'bold'), fg='black', justify='left',
                                   text=hour[n])
                label_n.place(relx=n_x, rely=n_y)
                n_x += 0.16
            n_x = 0.925

            weather_icon = hour[7]
            image_name = 'media/' + weather_icon + '.png'
            image = Image.open(image_name)
            image = image.resize((50, 45), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            img_label = tk.Label(frame4, image=image)
            img_label.image = image
            img_label.place(relx=n_x, rely=n_y)
        n_y += height + 0.01

        n_x = 0.01

    back_button = tk.Button(frame4, font=('serif', 15, 'bold'), fg='black', bg='white', text='Back',
                            command=lambda: change_frame(frame2))
    back_button.place(relx=0.01, rely=0.95, relheight=0.05)

    return


app_settings()
root.mainloop()
