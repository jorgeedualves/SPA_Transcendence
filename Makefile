DB_SERVICE_NAME = postgres-transcendence
APP_SERVICE_NAME = django-transcendence
PROXY_SERVICE_NAME = nginx-transcendence

DOCKER_SCRIPTS = $(addprefix _compose_scripts/,conditional-delete-container.sh conditional-delete-image.sh conditional-stop-container.sh)

all: .env volumes docker-compose.yml
	docker-compose up --build --detach --force-recreate

stop:
	docker-compose down

restart: stop start

clean: clean-db clean-app clean-proxy

fclean: fclean-db fclean-app fclean-proxy clean-postgres-data

clean-db: chmod-scripts
	@./_compose_scripts/conditional-stop-container.sh $(DB_SERVICE_NAME)
	@./_compose_scripts/conditional-delete-container.sh $(DB_SERVICE_NAME)

clean-app: chmod-scripts
	@./_compose_scripts/conditional-stop-container.sh $(APP_SERVICE_NAME)
	@./_compose_scripts/conditional-delete-container.sh $(APP_SERVICE_NAME)

clean-proxy: chmod-scripts
	@./_compose_scripts/conditional-stop-container.sh $(PROXY_SERVICE_NAME)
	@./_compose_scripts/conditional-delete-container.sh $(PROXY_SERVICE_NAME)

fclean-db: clean-db
	@./_compose_scripts/conditional-delete-image.sh postgres:16-alpine

fclean-app: clean-app
	@./_compose_scripts/conditional-delete-image.sh django

fclean-proxy: clean-proxy
	@./_compose_scripts/conditional-delete-image.sh nginx:alpine

chmod-scripts: $(DOCKER_SCRIPTS)
	chmod +x $(DOCKER_SCRIPTS)

volumes:
	mkdir -p ~/goinfre/ft_transcendence/postgres \
			 ~/goinfre/ft_transcendence/static

rm-volumes:
	docker volume rm -f spa_transcendence_postgres-vol
	docker volume rm -f spa_transcendence_static-vol

clean-postgres-data: rm-volumes
	sudo rm -rf ~/goinfre/ft_transcendence/postgres \
				~/goinfre/ft_transcendence/static

re: fclean all

.PHONY: all stop restart clean fclean clean-db fclean-db clean-app fclean-app rm-volumes volumes clean-postgres-data re