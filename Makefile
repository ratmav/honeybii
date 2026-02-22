IMAGE := honeybii

.DEFAULT_GOAL := help

build:
	docker build -t $(IMAGE) .

test: build
	docker run --rm $(IMAGE) rake test

demo: build
	docker run --rm $(IMAGE) ruby bin/honeybii test/images/flower_bee.jpg

run: build
ifndef FILE
	$(error FILE is required. Usage: make run FILE=/path/to/image.jpg [OPTS="-p 6 -g 2"])
endif
	docker run --rm -v $(FILE):/input$(suffix $(FILE)) $(IMAGE) ruby bin/honeybii /input$(suffix $(FILE)) $(OPTS)

options: build
	docker run --rm $(IMAGE) ruby bin/honeybii

help:
	@echo "Usage:"
	@echo "  make build                              Build the Docker image"
	@echo "  make test                               Run tests"
	@echo "  make demo                               Run against the test image"
	@echo "  make run FILE=/path/to/image.jpg        Convert an image to ASCII"
	@echo "  make run FILE=/path/to/image.jpg OPTS=\"-p 6 -g 2\""
	@echo "                                          Convert with honeybii options"
	@echo "  make options                            Show honeybii options"
	@echo "  make help                               Show this help"

.PHONY: build test demo run options help
