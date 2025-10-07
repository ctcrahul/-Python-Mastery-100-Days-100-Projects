
"""                            Day19.py

                     Weather App using API: APIs (Basics)
              
"""


de == 200:
      data = response.json()
      weather = {
          "City": data["name"],
          "Temperature": f"{data['main']['temp']}C",
          "Weather": data["weather"][0]['description'].title(),
          "Humidity": f"{data['main']['humidity']}%",
          "Wind Speed": f"{data['wind']['speed']}m/s"
      }
      return weather
    elif response.status_code == 404:
      print("City not found.")
    else:
      print("An error occurred. Status Code: ", response.status_code)
  except Exception as e:
    print("An error occurred: ", e)
  return None

# Step 3: Display Weather Information
def display_weather(weather):
  print("\n--- Weather Information ---")
  for key,value in weather.items():
    print(f"{key}: {value}")

# Step 4: Main Program Loop
while True:
  print("\n--- Wea
