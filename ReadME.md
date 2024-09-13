# Para instalar as dependências
```pip install sqlalchemy flask_jwt_extended dotenv flask_sqlalchemy flask bcrypt``` 

No arquivo `app.py`, encontra-se as funções necessárias para executar a aplicação:
  - inicialização do banco de dados, criando as tabelas de acordo com as classes `User` e `Task`;
  - inicialização do Flask;
  - inicialização das variáveis de ambiente — isto é: são variáveis que são executadas assim que o projeto for executado. As variáveis de ambiente são necessárias para armarzenar dados sensíveis como: chaves de acesso para banco de dados, chaves de acesso para executar requisições HTTP (como utilizado em APIs como o GitHub, para ter acesso a repositórios privados e na API da Riot Games é necessário ter uma conta Riot Games para que possa ser vinculada com a chave de acesso);
  - instanciamento da JWT;
  - criação das rotas das páginas;
  - criação das rotas de requisições HTTP das tabelas.

## JWT Token
Por questões de segurança, foi aplicado a tecnologia [Hash Salt](https://www.dcode.fr/hash-function) para manter as senhas mais seguras. E para autenticação, assim que o usuário se conectar à conta, é gerado um [JWT Token](https://jwt.io/introduction) em que fica guardado o ID do usuário, a data de expiração do Token, qual é o tipo de algoritmo que foi implementado, etc. Ele funciona como um ingresso. Sendo assim, foi criado certas rotas protegidas com JWT Token para que sejam acessadas com segurança capturando a informação do ID do usuário, por exemplo: sem o JWT Token o usuário consegue apagar a conta dos outros através do ID, assim como pode também apagar as tarefas dos outros.

## Banco de dados relacional - SQLite
Por se tratar de um banco de dados relacional, no caso do SQLite, é necessário definir regras para cada dado inserido no banco de dados. Como, por exemplo, o tipo do campo (texto/varchar, número inteiro, decimal/numerico, pk (chave primária), booleano, etc.). Em um banco de dados relacional, é possível fazer uma vinculação de chave estrangeira usando SQL puro. Por exemplo: O usuário fez uma tarefa para alguém. A tarefa receberá as propriedades: `id, title, description, author, responsable`. Quem criou a tarefa, terá seu CPF (chave estrangeira, id do autor) registrada no campo author. Quem será responsável pela tarefa também terá o CPF registrado no responsable. Sendo assim, de acordo com UML, o gráfico fica desta forma:

![image](https://github.com/user-attachments/assets/9c06941a-3ea1-4f78-9204-f59bfede6f97)


