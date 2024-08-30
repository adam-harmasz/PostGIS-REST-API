db-name=postgres


recreate-db:
	docker-compose stop web
	docker-compose exec db bash -c "su postgres -c 'dropdb $(db-name); createdb $(db-name);'"
	docker-compose up -d web
	make migrations

migrations:
	docker-compose exec web bash -c "python manage.py makemigrations && \
	python manage.py migrate"

build:
	docker-compose build

dev:
	docker-compose run --rm web python manage.py migrate
	docker-compose up

web-bash:
	docker-compose exec web bash

shell:
	docker-compose exec web bash -c "python manage.py shell"

format:
	docker-compose exec web bash -c "black . --line-length 120"

test:
	docker-compose exec web bash -c "python manage.py test"
