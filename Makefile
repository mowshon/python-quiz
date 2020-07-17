.PHONY: run build

run: build
	docker run -e APP_CONFIG_FILE="/opt/configs/prod.yaml" -v $(shell pwd)/configs:/opt/configs quizbot

build:
	eval DOCKER_BUILDKIT=1 docker build -t quizbot .
