import requests
import json
import os

CREDENTIALS_FILE = "credentials.json"

def read_api_key(file_path):
    if not os.path.exists(file_path):
        api_key = input("Enter your ngrok API key: ")
        with open(file_path, "w") as f:
            json.dump({"api_key": api_key}, f, indent=4)
    else:
        with open(file_path, "r") as f:
            data = json.load(f)
            api_key = data.get("api_key")
            if not api_key:
                api_key = input("Enter your ngrok API key: ")
                data["api_key"] = api_key
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
    return api_key

def create_tunnel_auth_token(api_key):
    url = "https://api.ngrok.com/credentials"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Ngrok-Version": "2"
    }
    data = {
        "description": "development cred for user"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        auth_token = response.json()["token"]
        return auth_token
    else:
        print(f"Failed to create tunnel auth token: {response.status_code}")
        print(response.json())
        return None

def save_auth_token(auth_token, file_path):
    with open(file_path, "r+") as f:
        data = json.load(f)
        data["auth_token"] = auth_token
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def validate_json_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        # Check for an extra "}" at the end of the file
        if content.endswith("}}"):
            content = content[:-1]
            with open(file_path, "w") as f_write:
                f_write.write(content)

def main():
    api_key = read_api_key(CREDENTIALS_FILE)
    auth_token = create_tunnel_auth_token(api_key)
    if auth_token:
        save_auth_token(auth_token, CREDENTIALS_FILE)
        validate_json_file(CREDENTIALS_FILE)
        print("Auth token saved to credentials.json.")

if __name__ == "__main__":
    main()
