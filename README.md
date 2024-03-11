## README.md

**Projeto Django - Script de Criação Automática**

Este documento descreve o script Python que automatiza a criação de um projeto Django básico. 

### Funcionalidades

* Cria a estrutura de diretórios do projeto, incluindo:
    * `nginx`
    * `django_app`
    * `tests`
    * `.github/workflows`
    * `scripts`
* Gera arquivos de configuração essenciais:  
    * `Dockerfile`
    * `docker-compose.yml`
    * `.gitignore`
    * `README.md`
    * `requirements.txt`
    * `setup.sh` (script de inicialização)
    * `gitconfig.py` (configuração básica do Git)
    * Arquivos de ambiente (`.env`)
* Integra com Docker e Docker Compose para facilitar o gerenciamento de ambiente e deploy.
* Inclui um script de inicialização (`setup.sh`) para instalar dependências e aplicar migrações do banco de dados.

### Uso

1. Salve o script como `create_django_project.py` no diretório desejado.
2. Execute o comando `python create_django_project.py`.
3. Execute o comando `sh script/setup.sh` no git bash se estiver no windows
4. Execute o comando docker-compose up -d para iniciar e docker-compose down para finalizar

docker exec -it appmed-db-1 bash

pg_dump -h db -p 5432 -U nome_do_usuario -d nome_do_banco_de_dados > arquivo_de_backup.sql 

### Observações

* Este script é um exemplo e pode ser adaptado às suas necessidades específicas.
* É recomendável ler e compreender o código antes de executá-lo.
* O script cria um projeto Django básico. Você pode precisar instalar outras dependências e configurar o projeto de acordo com suas necessidades.

### Recursos Adicionais

* Documentação oficial do Django: [https://docs.djangoproject.com/en/stable/](https://docs.djangoproject.com/en/stable/)
* Tutoriais do Django: [https://www.djangoproject.com/start/](https://www.djangoproject.com/start/)
* Documentação do Docker: [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)
* Documentação do Docker Compose: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)

### Contribuições

Este script é open-source e você pode contribuir para o seu desenvolvimento. Agradecemos qualquer colaboração!

### Tenha um excelente desenvolvimento com Django!
