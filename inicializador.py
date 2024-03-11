import os
import logging

caminho_atual = os.getcwd().replace('\\', '/')
nome_do_projeto = input("Digite o nome do projeto: ")
logging.basicConfig(
    filename="project.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def criar_estrutura_diretorios():
    try:
        diretorios = [
            f"{nome_do_projeto}/nginx",
            f"{nome_do_projeto}/{nome_do_projeto}",
            f"{nome_do_projeto}/tests",
            f"{nome_do_projeto}/.github/workflows",
            f"{nome_do_projeto}/scripts",
            f"{nome_do_projeto}/util",
        ]
        for diretorio in diretorios:
            os.makedirs(diretorio, exist_ok=True)
            logging.info(f"Diretório {diretorio} criado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao criar diretórios: {e}")


def criar_arquivos(caminho, conteudo):
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
            logging.info(f"Arquivo {caminho} criado com sucesso.")
            f.close()
    except Exception as e:
        logging.error(f"Erro ao criar arquivo: {e}")


docker = """
FROM python:3.9

WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos para o contêiner
COPY . .

EXPOSE 80
        """
docker_compose = """

version: '3'

services:
  db:
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    env_file:
      - .env.dev


  web:
    build: .
    volumes:
      - .:/app
    command: sh -c "pip install -r requirements.txt && python manage.py runserver 0.0.0.0:8085"
    ports:
      - "8090:8085"
    depends_on:
      - db
    env_file:
      - .env.dev
    working_dir: /app 


  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: 123
    depends_on:
      - db
    ports:
      - "8081:80"

  # nginx:
  #   image: nginx
  #   volumes:
  #     - ./nginx/nginx.conf:/etc/nginx/nginx.conf
  #   depends_on:
  #     - web
volumes:
  postgres_data:
        
        """ # noqa
script = f"""
#!/bin/bash

# Verifica se o Python está instalado
if ! command -v python &> /dev/null; then
    echo "Python não está instalado. Por favor, instale o Python."
    exit 1
fi

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Por favor, instale o Docker."
    exit 1
fi

# Verifica se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose não está instalado.instale o Docker Compose."
    exit 1
fi

cd {caminho_atual}/{nome_do_projeto}

# Cria um ambiente virtual (venv) se não existir
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Ativa o ambiente virtual
source venv/Scripts/activate

# Instala o Django dentro do ambiente virtual
pip install django


# Cria um novo projeto Django na pasta 'django_app'
django-admin startproject {nome_do_projeto} .


# Aplica as migrações do banco de dados
python manage.py migrate

# Inicia o servidor Django
python manage.py runserver 0.0.0.0:8000

    """
gitignore = """
# Arquivos de ambiente
.env.dev
.env.test
.env.prod

# Arquivos de log
*.log
        """
readme = """
# My Django App

Este é um projeto Django que utiliza Docker Compose para gerenciar um ambiente
de desenvolvimento e integração contínua (CI/CD) para automatizar o teste e
a implantação do código.

## Instruções de Instalação

Para executar este projeto localmente, siga as instruções abaixo:

1. Clone o repositório:

   ```bash
   git clone https://github.com/dhrds/my-django-app.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd my-django-app
   ```

3. Execute o script de inicialização para instalar as dependências
e aplicar as migrações do banco de dados:

   ```bash
   sh scripts/setup.sh
   ```

4. Inicie o ambiente Docker Compose:

   ```bash
   docker-compose up
   ```

5. Acesse a aplicação em seu navegador em
[http://localhost:8000](http://localhost:8000).

## Instruções de Uso

Após iniciar o ambiente Docker Compose, você pode interagir com a aplicação
normalmente. Qualquer alteração feita nos arquivos será automaticamente
refletida no servidor de desenvolvimento.

## Testes

Este projeto utiliza pytest para testes automatizados.
Para executar os testes, utilize o seguinte comando:

```bash
pytest
```

## Contribuição

Se você gostaria de contribuir para este projeto,
por favor siga as etapas abaixo:

1. Fork este repositório.
2. Crie uma nova branch para suas alterações:

   ```bash
   git checkout -b minha-nova-feature
   ```

3. Faça suas alterações e commit:

   ```bash
   git commit -am 'Adiciona nova feature'
   ```

4. Push para a branch:

   ```bash
   git push origin minha-nova-feature
   ```

5. Crie um novo pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
        """
ci_cd = """
name: CI/CD

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry config virtualenvs.create false
          poetry install --no-dev

      - name: Run tests
        run: |
          pytest

      - name: Build Docker image
        run: |
          docker-compose build
        """
git = """
import git

git.config("--global", "user.name", "Seu Nome")
git.config("--global", "user.email", "seu_email@email.com")
git.config("--global", "init.defaultBranch", "main")

repo = git.Repo.init(".")
repo.index.add(".")
repo.index.commit("Criando estrutura básica do Django e configurando Git")

                """
nginx = """
# Configurações básicas
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

# Configuração HTTPS (opcional)
server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /etc/ssl/nginx.pem;
    ssl_certificate_key /etc/ssl/nginx.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

# Configuração para arquivos estáticos (opcional)
server {
    listen 80;
    server_name localhost;

    location /static/ {
        root /path/to/static/files;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

# Configuração Gunicorn com vários workers (opcional)
upstream gunicorn {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 8000;
    server_name localhost;

    location / {
        proxy_pass http://gunicorn;
    }
}

# Configuração com balanceamento de carga (opcional)
upstream gunicorn {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://gunicorn;
    }
}

"""


def criar_envs():

    ambientes = [
        ".dev",
        ".test",
        ".prod",
        "_exemplo.dev",
        "_exemplo.test",
        "_exemplo.prod",
    ]
    for ambiente in ambientes:
        with open(f"{nome_do_projeto}/.env{ambiente}",
                  "w", encoding="utf-8") as f:
            f.write(
                """
POSTGRES_DB=nome_do_banco_de_dados
POSTGRES_USER=nome_do_usuario
POSTGRES_PASSWORD=sua_senha_secreta
POSTGRES_HOST=db

DJANGO_SECRET_KEY=sua_chave_secreta
DJANGO_DEBUG=True
            """
            )


def main():

    criar_estrutura_diretorios()
    criar_envs()
    criar_arquivos(f"{nome_do_projeto}/Dockerfile", docker)
    criar_arquivos(f"{nome_do_projeto}/docker-compose.yml", docker_compose)
    criar_arquivos(f"{nome_do_projeto}/scripts/setup.sh", script)
    criar_arquivos(f"{nome_do_projeto}/.gitignore", gitignore)
    criar_arquivos(f"{nome_do_projeto}/README.md", readme)
    criar_arquivos(f"{nome_do_projeto}/requirements.txt", "Django==4.2.5")
    criar_arquivos(f"{nome_do_projeto}/.github/workflows/ci-cd.yml", ci_cd)
    criar_arquivos(f"{nome_do_projeto}/gitconfig.py", git)
    criar_arquivos(f"{nome_do_projeto}/nginx/nginx.conf", nginx)
    print("Arquivos criados com sucesso!")


if __name__ == "__main__":
    main()
