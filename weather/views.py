from django.shortcuts import render
import json
import urllib.request
from datetime import datetime, timezone
import requests
# Create your views here.
def index(request):
    data = {}
    error_message = None
    if request.method == 'POST':
        city = request.POST['city']
        if city:
            try:
                res = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=4843294ed54d8db19afda2ecfd556d58').read()
                json_data = json.loads(res)
                api_key = 'GQjHMX4tvtHatHs08b3+EQ==XmNODG7RykC4hzJP'
                lat = json_data['coord']['lat']
                long = json_data['coord']['lon']
                time_url = "http://api.timezonedb.com/v2.1/get-time-zone?key=H3E525G4N9Q2&format=json&by=position&lat={}&lng={}".format(lat,long)
                resp = requests.get(time_url)
                resp_json = resp.json()
                icon_code = json_data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                sunrise = json_data['sys']['sunrise']
                sunset = json_data['sys']['sunset']
                current_time = datetime.now(timezone.utc).timestamp() 

                is_daytime = sunrise <= current_time <= sunset
                day_or_night = "Day" if is_daytime else "Night"

                data = {
                    'city' : str(json_data['name']),
                    'country_code' : str(json_data['sys']['country']),
                    'coordinate' : str(json_data['coord']['lon'])+' N '+str(json_data['coord']['lat'])+' E',
                    'temp' : str(int(json_data['main']['temp']) - int(273.15)) +' °C',
                    'pressure' : str(json_data['main']['pressure'])+' '+'hPa',
                    'humidity' : str(json_data['main']['humidity'])+' '+'%',
                    'icon_url': icon_url,
                    'desc' : str(json_data['weather'][0]['description']),
                    'day_or_night': day_or_night,
                }
                date_time = resp_json.get("formatted")
                date_time = str(date_time)
                date = date_time[:10]
                time = date_time[11:]

                
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    error_message = "City not found. Please enter a valid city name."
                else:
                    error_message = "An error occurred while fetching weather data."
        else:
            error_message = "City name cannot be empty"
            
    return render(request,'index.html', {'data':data, 'error_message':error_message,'date':date,'time':time})   