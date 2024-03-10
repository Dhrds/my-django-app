
# My Django App

Este é um projeto Django que utiliza Docker Compose para gerenciar um ambiente
de desenvolvimento e integração contínua (CI/CD) para automatizar o teste e
a implantação do código.

## Instruções de Instalação

Para executar este projeto localmente, siga as instruções abaixo:

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/my-django-app.git
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
        