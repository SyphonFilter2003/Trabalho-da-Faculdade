# Para instalar as dependências
```pip install sqlalchemy flask_jwt_extended dotenv flask_sqlalchemy flask bcrypt``` 

1. app.py (Código Principal da API)
Este script configura uma aplicação Flask e integra Firebase e autenticação JWT.

2. taskAPI.py (Rotas para Gerenciamento de Tarefas)
Este script define rotas para criar, obter e excluir tarefas no Firestore.

3. userAPI.py (Rotas para Gerenciamento de Usuários)
Este script define rotas para registrar, autenticar e gerenciar usuários.

4. JavaScript (app.js)
Este script gerencia as interações do usuário com a aplicação web, incluindo registro, login, criação e gerenciamento de tarefas, e atualizações e exclusões de usuários.

5.Arquivos CSS são usados para estilizar o HTML da aplicação.

6. delete_user.html
Este é um template HTML para a página de exclusão de conta de usuário. Ele permite que o usuário exclua sua própria conta da aplicação

7. index.html
Este é o template HTML para a página inicial do "Task Manager". Ele serve como ponto de entrada para o usuário, oferecendo links para as páginas de registro e login.

8.login.html
Este arquivo HTML representa a página de login da aplicação. Ele inclui um formulário com campos para o nome de usuário e a senha, além de um botão de envio. O estilo é fornecido pelo arquivo bootstrap.min.css e o JavaScript é gerenciado pelo arquivo app.js.

9.register.html
Este arquivo HTML representa a página de registro de um novo usuário. O formulário contém campos para o nome de usuário e a senha, e um botão para enviar os dados. O arquivo bootstrap.min.css é utilizado para o estilo, e o script app.js é responsável pela lógica do lado do cliente.

10.tasks.html
Este arquivo HTML é para a página de tarefas. Contém um formulário para criar novas tarefas, com campos para título e descrição, e um botão para enviar. Além disso, exibe uma lista de tarefas e fornece links para atualizar ou excluir usuários. O arquivo bootstrap.min.css e styles.css são usados para estilização, e app.js lida com a funcionalidade do lado do cliente.

11.update_user.html
Este arquivo HTML é para a página de atualização de usuário. Inclui um formulário para modificar o nome de usuário e a senha. O formulário possui campos para o novo nome de usuário e nova senha, e um botão para atualizar as informações. O estilo é aplicado pelo bootstrap.min.css, e a lógica é gerida por app.js.

12.checkPassword.py
Este arquivo define uma função chamada check_password que verifica se uma senha fornecida corresponde a um hash armazenado. Ele utiliza a biblioteca bcrypt para realizar a comparação.

13.encrypt.py
Este arquivo contém a função hash_password, que recebe uma senha em texto simples e a transforma em um hash seguro usando a biblioteca bcrypt.

14.app.py
É uma aplicação Flask que gerencia usuários e tarefas com autenticação JWT e interação com o banco de dados usando SQLAlchemy.

15. Main.py
É responsável por iniciar a aplicação Flask, chamando uma função de criação de aplicativo a partir de um módulo chamado API.

