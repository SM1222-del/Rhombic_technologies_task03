# Rhombic_technologies_task03
Location Tracker Virtual Assistant

This Python script is a simple virtual assistant that helps you track your current location using your public IP address. It fetches your approximate location using the ip-api.com service and displays it on an interactive map using the folium library. The assistant can also speak to you and listen to your commands using text-to-speech (pyttsx3) and speech recognition (speech_recognition) libraries.

Features:
Fetch Public IP: Retrieves your public IP address.

Geolocation: Determines your approximate location (city, region, country) using ip-api.com.

Interactive Map: Displays your location on a map using folium.

Voice Commands: Responds to voice commands like "Where am I?" or "Show my location."

Text-to-Speech: Speaks out your location and other responses.

###How It Works:
The assistant listens for your voice command.

If you ask for your location, it fetches your public IP and uses it to determine your approximate location.

The location is displayed on an interactive map, and the assistant speaks out your address.

###Requirements:

Python 3.x
Libraries: requests, folium, speech_recognition, pyttsx3

###Usage:
Run the script, and the virtual assistant will greet you. Simply ask, "Where am I?" or "Show my location," and it will fetch and display your location. Say "exit" to end the session.
