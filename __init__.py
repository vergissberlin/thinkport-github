import logging
import requests
import paho.mqtt.client as mqtt
import os

def main(myTimer):
    logging.info("Azure Function gestartet...")

    # GitHub API URL
    url = "https://api.github.com/search/issues?q=org:thinkportrepo+is:issue+is:open"
    
    # GitHub API Request
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Anzahl offener Issues
    open_issues = data.get("total_count", 0)
    logging.info(f"Offene Issues: {open_issues}")

    # MQTT Verbindung
    mqtt_broker = os.getenv("MQTT_BROKER", "andrelademann.de")
    mqtt_port = int(os.getenv("MQTT_PORT", 1883))
    mqtt_topic = os.getenv("MQTT_TOPIC", "tp/cmnd/tasmota/display")
    
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    client.publish(mqtt_topic, f"Offene Issues: {open_issues}")
    client.disconnect()

    logging.info("Daten an MQTT gesendet!")