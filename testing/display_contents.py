import requests, html
from bs4 import BeautifulSoup

# Function to fetch and parse AirNow RSS feed
def fetch_air_quality_data(feed_url):
    # Parse the RSS feed
    response = requests.get(feed_url)
    soup = BeautifulSoup(response.content, "xml")

    items = soup.find_all("item")

    #initialize all as None
    location = None
    agency = None
    two_microns = None
    ten_microns = None
    ozone = None

    #Find all variables in the parsed data
    for item in items:
        description = item.find("description").text  # Get the description text
        decoded_description = html.unescape(description)  # Decode HTML entities

        #Extract the specific line
        for line in decoded_description.split("<br />"):
            #clean the lines
            line = line.strip()
            clean_line = (line.replace("<div>", "").replace("</div>", "")
                              .replace("<b>", "").replace("</b>", "").strip())

            match True:
                case _ if "Location:" in clean_line:
                    location = clean_line.split("Location:")[1].strip()
                case _ if "Agency:" in clean_line:
                    agency = clean_line.split("Agency:")[1].strip()
                case _ if "Particle Pollution (2.5 microns)" in clean_line:
                    parts = clean_line.split(" - ")
                    two_microns = parts[0] + "- " + parts[1]
                case _ if  "Particle Pollution (10 microns)" in clean_line:
                    parts = clean_line.split(" - ")
                    ten_microns = parts[0] + "- " + parts[1]
                case _ if "Ozone" in clean_line:
                    parts = clean_line.split(" - ")
                    ozone = parts[0] + "- " + parts[1]
                 # Stop after finding the first match

    #check if any are None
    if not agency:
        agency = "Agency not found"
    if not location:
        location = "Location not found"
    if not two_microns:
        two_microns = "Current 2.5 microns not found"
    if not ten_microns:
        ten_microns = "Current 10 microns not found"
    if not ozone:
        ozone = "Current ozone not found"


    # Output the extracted data
    print(f"Location: {location}")
    print(f"Agency: {agency}")
    print(f"Current 2.5 Micron reading: {two_microns}")
    print(f"Current 10 Micron reading: {ten_microns}")
    print(f"Current Ozone reading: {ozone}")

    

# AirNow RSS feed URL
rss_feed_url = "https://feeds.airnowapi.org/rss/realtime/384.xml"

# Fetch and parse air quality data
fetch_air_quality_data(rss_feed_url)

rss_feed_url = "https://feeds.airnowapi.org/rss/realtime/382.xml"

# Fetch and parse air quality data
fetch_air_quality_data(rss_feed_url)