import subprocess
import requests
import time
import json
import os
import signal

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
NGROK_URLS_FILE = os.path.join(SCRIPT_DIR, "ngrok_urls.txt")

def read_api_key(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("api_key")
    return None

def read_auth_token(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("auth_token")
    return None

def kill_existing_ngrok():
    url = "http://127.0.0.1:4040/api/tunnels"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for tunnel in data['tunnels']:
                subprocess.run(["ngrok", "http", "stop", tunnel["name"]], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except requests.ConnectionError:
        pass

def start_ngrok(auth_token):
    kill_existing_ngrok()
    subprocess.run(["ngrok", "authtoken", auth_token], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.Popen(["ngrok", "start", "--all"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def get_ngrok_urls():
    time.sleep(5)  # Wait for ngrok to initialize
    url = "http://127.0.0.1:4040/api/tunnels"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ngrok_urls = [tunnel['public_url'] for tunnel in data['tunnels'] if tunnel['proto'] == 'https']
        return ngrok_urls
    except requests.exceptions.RequestException:
        return []

def save_ngrok_urls():
    auth_token = read_auth_token(CREDENTIALS_FILE)
    if auth_token:
        start_ngrok(auth_token)
        ngrok_urls = get_ngrok_urls()
        if ngrok_urls:
            print(f"Your ngrok URLs are: {ngrok_urls}")
            with open(NGROK_URLS_FILE, "w") as f:
                for url in ngrok_urls:
                    f.write(f"{url}\n")
        else:
            print("Failed to get ngrok URLs")
    else:
        print("Auth token not found in credentials.json")

def delete_auth_tokens(api_key):
    url = "https://api.ngrok.com/credentials"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Ngrok-Version": "2",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        credentials = response.json().get('credentials', [])
        for credential in credentials:
            credential_id = credential.get('id')
            delete_url = f"https://api.ngrok.com/credentials/{credential_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f"Deleted auth token {credential_id}")
            else:
                print(f"Failed to delete auth token {credential_id}")
    except requests.exceptions.RequestException as e:
        pass

def signal_handler(signal, frame):
    print("Application terminated. Deleting ngrok auth tokens...")
    api_key = read_api_key(CREDENTIALS_FILE)
    if api_key:
        delete_auth_tokens(api_key)
    else:
        print("API key not found in credentials.json")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        save_ngrok_urls()
    except Exception as e:
        print(f"Error starting ngrok: {e}")
