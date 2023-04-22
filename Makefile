# Set environment variables
export FLASK_APP=app.py

# Run the app
run:
	flask --app app run

# Run tests
dev:
	flask --app app run -h localhost -p 8000 --debug

# Run tests
test:
	python -m unittest discover -s tests

# Clean up temporary files
clean:
	rm -rf __pycache__

# Default target
.PHONY: run