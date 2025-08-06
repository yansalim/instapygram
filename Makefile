.PHONY: install run test build compose-up clean

# Cria o ambiente virtual e instala dependências
install:
	python -m venv .venv && \
	. .venv/Scripts/activate && \
	pip install -r requirements.txt

# Executa a API localmente (Flask dev server)
run:
	python run.py

# Executa testes com pytest
test:
	pytest -x -s

# Compila a imagem Docker
build:
	docker build -t pipegram-flask .

# Sobe a API com Docker Compose (versão v2)
compose-up:
	docker compose up --build -d

# Remove o ambiente virtual
clean:
	rmdir /S /Q .venv
