# Stream2Gether

Stream2Gether is a collaborative streaming platform that allows users to create and join rooms to watch videos together. This project includes features like multi-tunneling with ngrok, a Node.js server, and a Python Flask backend.

## Features

- Multi-room video streaming with ngrok tunneling
- Real-time chat functionality
- Node.js server integration
- Python Flask backend

## Prerequisites

- **Git:** To clone the repository.
- **ngrok:** For tunneling and exposing local servers to the internet.
- **Node.js:** JavaScript runtime for running the Node.js server.
- **Python 3:** For the Flask backend.
- **envtool:** For managing Python virtual environments.
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
