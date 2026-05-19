import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os

location = input("Enter location: ")

geo_url = f'https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json'
response_geo = requests.get(geo_url)
data_geo = response_geo.json()

latitude = data_geo['results'][0]['latitude']
longitude = data_geo['results'][0]['longitude']

today = datetime.now()
week_ago = today - timedelta(days=7)

start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

response = requests.get(url)
data = response.json()

print(data)

daily_data = data['daily']

# Create a DataFrame
df = pd.DataFrame({
    'date': daily_data['time'],
    'max_temp': daily_data['temperature_2m_max'],
    'min_temp': daily_data['temperature_2m_min'],
})

#Convert date strings to datetime
df['date'] = pd.to_datetime(df['date'])
df['max_temp'] = pd.to_numeric(df['max_temp'])
df['min_temp'] = pd.to_numeric(df['min_temp'])

print(df)

# -------------------------------------------------

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['max_temp'], marker='o', label='Max Temp')
plt.plot(df['date'], df['min_temp'], marker='o', label='Min Temp')

safe_location = location.strip().lower().replace(" ", "_")
# Add labels and title
plt.xlabel('Date')
plt.ylabel('Temp (oC)')
plt.title(f'{safe_location} Weather - Past 7 Days')
plt.legend()

# Rotate x-axis labels for readability
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('weather_chart.png')
plt.show()

if not os.path.exists('data'):
    os.makedirs('data')

df.to_csv(f'data/{safe_location}_weather.csv', index=False)
print(f'Data saved to data/{safe_location}_weather.csv')

