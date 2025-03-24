import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import time
import matplotlib.pyplot as plt
import numpy as np

def scrape_weather_data(city):
    if not os.path.exists('weather_data'):
        os.makedirs('weather_data')

    city_formatted = city.lower().replace(' ', '-')
    url = f"https://www.wunderground.com/history/daily/{city_formatted}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            current_temp = soup.find('span', class_='wu-value-to')
            current_condition = soup.find('div', class_='condition-icon')

            if current_temp and current_condition:
                print(f"Current temperature in {city}: {current_temp.text}°F")
                print(f"Current condition: {current_condition.get('title', 'Unknown')}")
            table = soup.find('table', class_='days')
            if table:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_file = f"weather_data/{city}_{timestamp}.csv"

                with open(csv_file, 'w', newline='') as file:
                    writer = csv.writer(file)

                    headers = []
                    header_row = table.find('thead').find('tr')
                    for th in header_row.find_all('th'):
                        headers.append(th.text.strip())
                    writer.writerow(headers)

                    tbody = table.find('tbody')
                    for tr in tbody.find_all('tr'):
                        row = []
                        for td in tr.find_all('td'):
                            row.append(td.text.strip())
                        writer.writerow(row)
                print(f"Historical weather data saved to {csv_file}")
                visualize_weather_data(csv_file)
            else:
                print("Could not find historical data table")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def visualize_weather_data(csv_file):
    # Read data from CSV
    dates = []
    temps = []
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        
        temp_index = headers.index('Temp') if 'Temp' in headers else 1
        
        for row in reader:
            if len(row) > temp_index:
                try:
                    dates.append(row[0])
                    temps.append(float(row[temp_index].replace('°F', '')))
                except ValueError:
                    continue
    
    if dates and temps:
        plt.figure(figsize=(10, 6))
        plt.plot(dates, temps, marker='o')
        plt.title('Temperature Variation')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°F)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot
        plot_file = csv_file.replace('.csv', '_plot.png')
        plt.savefig(plot_file)
        print(f"Plot saved as {plot_file}")
        plt.close()

if __name__ == "__main__":
    city = input("Enter a city name for weather data: ")
    scrape_weather_data(city)