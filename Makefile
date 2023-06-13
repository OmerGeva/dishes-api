# Set environment variables
export FLASK_APP=app.py

run:	
	flask --app dishes-api/app run
dev:
	flask --app dishes-api/app run -h localhost -p 8000 --debug

test:
	cd dishes-api && python -m unittest discover -s tests

clean:
	rm -rf dishes-api/__pycache__

remove_images:
	docker rmi $(docker images -a -q)

.PHONY: run