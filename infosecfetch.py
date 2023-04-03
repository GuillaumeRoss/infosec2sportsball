import csv
from requests_html import HTMLSession
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="security_conferences_scraper")

url = 'https://infosec-conferences.com/country/united-states/'
session = HTMLSession()
response = session.get(url)
response.html.render(timeout=20)

events = response.html.find('div.event-post-item-row')

def estimate_state(city):
    try:
        location = geolocator.geocode(city + ", United States", timeout=10)
        if location and 'address' in location.raw and 'state' in location.raw['address']:
            return location.raw['address']['state']
    except GeocoderTimedOut:
        return 'N/A'
    return 'N/A'

with open('security_conferences.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Start Date', 'City', 'State', 'Conference Name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for event in events:
        start_date = event.find('time[itemprop=startDate]', first=True).text.strip()
        
        location_info = event.find('span[itemprop=location]', first=True)
        location_text = location_info.find('span[itemprop=name]', first=True).text.strip()
        location_parts = location_text.split('|')[1].strip().split(',')
        city = location_parts[1].strip()
        state = location_parts[0].split()[-1].strip()

        conference_name_tag = event.find('span[itemprop=name] a', first=True)
        if conference_name_tag:
            conference_name = conference_name_tag.text.strip()
        else:
            conference_name = event.find('span[itemprop=name]', first=True).text.split('|')[0].strip()

        writer.writerow({'Start Date': start_date, 'City': city, 'State': state, 'Conference Name': conference_name})

print("CSV file has been created successfully.")
