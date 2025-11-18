from app import create_app

app = create_app()

if __name__ == "__main__":
    # Run on port 3001 for alignment with preview system
    app.run(host="0.0.0.0", port=3001, debug=True)
