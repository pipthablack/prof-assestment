from app import create_app

app = create_app()

if __name__ == "__main__":
      app.run(host='0.0.0.0', port=8080) # Run the Flask app in debug mode on port 5000
