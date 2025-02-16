import requests
import folium
import speech_recognition as sr
import pyttsx3
import webbrowser
import os

GOOGLE_API_KEY = ""  # Replace with your Google API key

# Function to fetch the public IP address
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json().get("ip")
        return None
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        return None

# Function to fetch data using Google Geocoding API
def get_geolocation(ip_address):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        if response.status_code == 200:
            data = response.json()
            latitude = data.get("lat")
            longitude = data.get("lon")
            print(f"Approximate Location (from ip-api.com): {data}")

            if latitude and longitude:
                google_geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_API_KEY}"
                google_response = requests.get(google_geocode_url)
                google_data = google_response.json()
                print(f"Google Geocoding API Response: {google_data}")

                if google_data.get("status") == "OK":
                    formatted_address = google_data["results"][0]["formatted_address"]
                    print(f"Precise Location (from Google Geocoding API): {formatted_address}")
                    return {
                        "latitude": latitude,
                        "longitude": longitude,
                        "address": formatted_address
                    }
                else:
                    print(f"Google Geocoding API Error: {google_data.get('error_message')}")  # Debug statement
                    return {"error": google_data.get("error_message", "Google Geocoding API failed")}
        return {"error": "Unable to fetch precise location data"}
    except Exception as e:
        print(f"Error fetching geolocation data: {e}")
        return {"error": "An error occurred"}

# Function to generate and display a map using folium
def show_map(latitude, longitude):
    mp = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker(
        location=[latitude, longitude],
        popup="Your Location",
        icon=folium.Icon(color="blue")
    ).add_to(mp)

    # Save the map to an HTML file
    map_file = "user_location_map.html"
    mp.save(map_file)

    webbrowser.open(f"file://{os.path.abspath(map_file)}")

# Function to speak text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to listen
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-US")
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you please repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please try again later.")
        return None

# Virtual Assistant
def virtual_assistant():
    speak("Hello! I am your virtual assistant. How can I help you today?")

    while True:
        query = listen()

        if query and "location" in query:
            speak("Fetching your location. Please wait a moment.")

            # Fetch user's public IP address
            ip_address = get_public_ip()
            if not ip_address:
                speak("Sorry, I couldn't fetch your IP address. Please check your internet connection.")
                continue

            geolocation = get_geolocation(ip_address)
            if "error" in geolocation:
                speak(f"Sorry, I couldn't fetch your location. Error: {geolocation['error']}")
                continue

            # Extract location details
            address = geolocation.get("address", "unknown location")
            latitude = geolocation.get("latitude")
            longitude = geolocation.get("longitude")

            location_message = f"You are currently at {address}."
            print(location_message)
            speak(location_message)

            if latitude and longitude:
                speak("Displaying your location on the map.")
                show_map(latitude, longitude)
            else:
                speak("Sorry, I couldn't fetch your exact location coordinates.")

        elif query and "exit" in query:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")

# Call the function
if __name__ == "__main__":
    virtual_assistant()