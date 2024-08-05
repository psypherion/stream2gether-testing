# Ensure the presence of server.js
if [ ! -f server.js ]; then
    echo "server.js not found. Make sure it is in the current directory." 1>&2
    exit 1
fi

# Start the Flask application
echo "Starting Flask application..."
export FLASK_APP=app.py  # Change 'app.py' to your Flask app filename
export FLASK_ENV=development
python3 app.py &

# Start the Node.js server
echo "Starting Node.js server..."
node server.js 

