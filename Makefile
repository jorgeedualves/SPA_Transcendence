DB_SERVICE_NAME = postgres-transcendence
APP_SERVICE_NAME = django-transcendence

DOCKER_SCRIPTS = $(addprefix _compose_scripts/,conditional-delete-container.sh conditional-delete-image.sh conditional-stop-container.sh)

all: .env volumes docker-compose.yml
	docker-compose up --build --detach --force-recreate

stop:
	docker-compose down

restart: stop start

clean: clean-db clean-app

fclean: fclean-db fclean-app  rm-volumes

clean-db: chmod-scripts
	@./_compose_scripts/conditional-stop-container.sh $(DB_SERVICE_NAME)
	@./_compose_scripts/conditional-delete-container.sh $(DB_SERVICE_NAME)

clean-app: chmod-scripts
	@./_compose_scripts/conditional-stop-container.sh $(APP_SERVICE_NAME)
	@./_compose_scripts/conditional-delete-container.sh $(APP_SERVICE_NAME)

fclean-db: clean-db
	@./_compose_scripts/conditional-delete-image.sh postgres

fclean-app: clean-app
	@./_compose_scripts/conditional-delete-image.sh django

chmod-scripts: $(DOCKER_SCRIPTS)
	chmod +x $(DOCKER_SCRIPTS)

volumes:
	mkdir -p ~/goinfre/ft_transcendence/django \
			 ~/goinfre/ft_transcendence/postgres

rm-volumes:
	docker volume rm -f spa_transcendence_django-vol
	docker volume rm -f spa_transcendence_postgres-vol

re: fclean all

.PHONY: all stop restart clean fclean clean-db fclean-db clean-app fclean-app volumes re