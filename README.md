# Stream2Gether
![stream2gether](stream2gether.jpeg)
Stream2Gether is a web application designed to let users watch videos together with friends remotely. While there are existing solutions like Rave, they often lack support for Linux or do not provide the features I wanted. Stream2Gether aims to bridge this gap by offering a simple and functional platform for video watching.

## Why Stream2Gether?
Pirating movies has often been my go-to for watching films, whether through Stremio, Telegram, or torrent sites. However, sharing these experiences with friends who are far away has always been a challenge. Existing software like Rave, which allows for synchronized watching, is not available on Linux, which I use extensively. Additionally, uploading videos to Google Drive for sharing is cumbersome and time-consuming.

Stream2Gether was created to address these issues, offering a more seamless way to enjoy videos together, right from your Linux environment.


## Features

- Watch videos together.
- Real-time chat functionality.
- Host videos directly from your local computer.
- User can also download the video from the room.

## Future Updates

- **Video Calling Feature:** Integrate video calling for a more interactive experience.
- **Improved UI:** Enhance the user interface for better aesthetics and usability.
- **Voice Calling:** Add voice communication capabilities.
- **Cloud Server Integration:** Implement cloud server support for smoother video sharing.
- **Synchronized Video Playback:** Syncing video in the room
- 
## Prerequisites

- **Git:** To clone the repository.
- **ngrok:** For tunneling and exposing local servers to the internet.
- **Node.js:** JavaScript runtime for running the Node.js server.
- **Python 3:** For the Flask backend.
- **envtool:** For managing Python virtual environments. (A tool made by me to handle python environments)
(Dont Worry every thing will be handled using a bash script)

## Setup

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/ky13-troj/stream2gether.git
cd stream2gether
```

### 2. Run the Setup Script

The `setup.sh` script will handle the installation of dependencies and setup of the environment.
```bash
chmod +x setup.sh
sudo bash setup.sh

```
### 3. Activate the Python Virtual Environment

After running the setup script, activate the virtual environment:
```bash
source venv/bin/activate

```
### 4. Run the Application

To start the Flask backend and Node.js server, use the `run.sh` script:
```bash
sudo bash run.sh

```

## Configuration

### ngrok

1. **Download ngrok:** The setup script will handle this step.
2. **API Key:** You will be prompted to enter your ngrok API key during the setup process. If you need to generate a new API key, sign up or log in at [ngrok Dashboard](https://dashboard.ngrok.com) and navigate to the Auth section.
3. **Multi-Tunneling:** The setup script configures ngrok for both Flask and Node.js tunnels.

### `credentials.json`

The `credentials.json` file will be created during the setup process. This file will contain your ngrok API key.

## Running the Application

Once everything is set up, you can start the Flask and Node.js servers using the `run.sh` script. Make sure your ngrok tunnels are correctly configured and running.

## Troubleshooting

If you encounter issues such as ports already being in use, check that no other services are using ports 5000 (Flask) or 3000 (Node.js). You can kill any processes using these ports or modify the configuration to use different ports.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or issues, please contact the project maintainer:
For any questions or issues, please contact the project maintainer:

- **Email:** williamskyle562@gmail.com
- **GitHub:** [ky13-troj](https://github.com/ky13-troj)
