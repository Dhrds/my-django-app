import os


nome_do_projeto = input("Digite o nome do projeto: ")


def criar_estrutura_diretorios():
    diretorios = [
        f"{nome_do_projeto}/nginx",
        f"{nome_do_projeto}/django_app",
        f"{nome_do_projeto}/tests",
        f"{nome_do_projeto}/.github/workflows",
        f"{nome_do_projeto}/scripts",
    ]
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)


def criar_dockerfile():

    with open(f"{nome_do_projeto}/Dockerfile", "w", encoding="utf-8") as f:
        f.write("""
FROM python:3.9

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry && \\
    poetry config virtualenvs.create false && \\
    poetry install --no-dev

COPY . .
CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']
        """)


def criar_docker_compose():

    with open(f"{nome_do_projeto}/docker-compose.yml",
              "w", encoding="utf-8") as f:
        f.write("""
version: '3'

services:
  db:
    image: postgres
    volumes:
      - db_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DJANGO_DEBUG: ${DJANGO_DEBUG}

  nginx:
    image: nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
    depends_on:
      - web

  monitoring_tool:
    image: monitoring_tool_image
        """)


def criar_envs():

    ambientes = ['.dev', '.test', '.prod',
                 '_exemplo.dev', '_exemplo.test', '_exemplo.prod']
    for ambiente in ambientes:
        with open(f"{nome_do_projeto}/.env{ambiente}",
                  "w", encoding="utf-8") as f:
            f.write("""
POSTGRES_DB=nome_do_banco_de_dados
POSTGRES_USER=nome_do_usuario
POSTGRES_PASSWORD=sua_senha_secreta
POSTGRES_HOST=db

DJANGO_SECRET_KEY=sua_chave_secreta
DJANGO_DEBUG=True
            """)


def criar_gitignore():
    with open(f"{nome_do_projeto}/.gitignore", "w", encoding="utf-8") as f:
        f.write("""
# Arquivos de ambiente
.env.dev
.env.test
.env.prod

# Arquivos de log
*.log
        """)


def criar_readme():
    with open(f"{nome_do_projeto}/README.md", "w", encoding="utf-8") as f:
        f.write("""
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
        """)


def criar_ci_cd():
    with open(f"{nome_do_projeto}/.github/workflows/ci-cd.yml",
              "w", encoding="utf-8") as f:
        f.write("""
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
        """)


def criar_script_inicializacao():
    with open(f"{nome_do_projeto}/scripts/setup.sh",
              "w", encoding="utf-8") as f:
        f.write("""
#!/bin/bash


# Função para exibir a mensagem de uso
usage() {
  echo "Uso: $0 [-v VENV]"
  echo "  -v VENV  Especifica o ambiente virtual Python a ser usado."
  exit 1
}

# Variável para armazenar o ambiente virtual
venv=

# Leitura e tratamento das opções e argumentos
while getopts ":v:" opt; do
  case $opt in
    v) venv=$OPTARG ;;
    *) usage ;;
  esac
done

# Remoção das opções da lista de argumentos
shift $((OPTIND-1))

# Validação do comando pip
if ! command -v pip >/dev/null 2>&1; then
  echo "Erro: O comando 'pip' não está instalado."
  exit 1
fi

# Validação do ambiente virtual Python
if [ -n "$venv" ]; then
  if ! python -c "import sys; print(sys.prefix)" | grep -q "$venv"; then
    echo "Erro: O ambiente virtual Python '$venv' não existe."
    exit 1
  fi
else
  if ! python -c "import sys; print(sys.prefix)" | grep -q venv; then
    echo "Erro: O ambiente virtual Python não está ativado."
    exit 1
  fi
fi

# Instalação de dependências
pip install -r requirements.txt >> install.log 2>&1

# Verificação de erros na instalação das dependências
if [ $? -ne 0 ]; then
  echo "Erro ao instalar as dependências. Consulte o log de erros."
  exit 1
fi

# Aplicação de migrações de banco de dados
python manage.py migrate >> migrate.log 2>&1

# Verificação de erros na migração do banco de dados
if [ $? -ne 0 ]; then
  echo "Erro nas migrações do banco de dados. Consulte o log de erros."
  exit 1
fi

echo "Script executado com sucesso!"

    """)


def criar_git():
    with open(f"{nome_do_projeto}/gitconfig.py", "w", encoding="utf-8") as f:
        f.write("""
import git

git.config("--global", "user.name", "Seu Nome")
git.config("--global", "user.email", "seu_email@email.com")
git.config("--global", "init.defaultBranch", "main")

repo = git.Repo.init(".")
repo.index.add(".")
repo.index.commit("Criando estrutura básica do Django e configurando Git")

                """)


def main():

    criar_estrutura_diretorios()
    criar_dockerfile()
    criar_docker_compose()
    criar_envs()
    criar_readme()
    criar_gitignore()
    criar_ci_cd()
    criar_script_inicializacao()
    criar_git()
    print("Arquivos criados com sucesso!")


if __name__ == "__main__":
    main()
