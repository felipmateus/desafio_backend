# Documentação da API de Usuários

Esta é a documentação da API de usuários.

## Recurso `/usuarios/{user_id}`

### `GET`

Retorna informações do usuário.

**Parâmetros:**

- `user_id` (int): ID do usuário a ser buscado.

**Respostas:**

- `200 OK`: Retorna um objeto JSON com as informações do usuário.
- `404 Not Found`: Usuário não encontrado.

### `DELETE`

Deleta o usuário e sua carteira.

**Parâmetros:**

- `user_id` (int): ID do usuário a ser deletado.

**Respostas:**

- `201 Created`: Usuário deletado com sucesso.
- `404 Not Found`: Usuário não encontrado.

## Recurso `/usuarios/cadastro`

### `POST`

Cadastra um novo usuário e sua carteira.

**Parâmetros:**

- `email` (string): E-mail do usuário.
- `password` (string): Senha do usuário.
- `name` (string): Nome do usuário.
- `cpf` (int): CPF do usuário.
- `type` (string): Tipo de usuário (opcional).

**Respostas:**

- `201 Created`: Usuário criado com sucesso.
- `422 Unprocessable Entity`: Algum campo obrigatório não foi preenchido.

## Recurso `/usuarios/login`

### `POST`

Realiza o login do usuário.

**Parâmetros:**

- `email` (string): E-mail do usuário.
- `password` (string): Senha do usuário.

**Respostas:**

- `200 OK`: Retorna um token de acesso válido por um determinado período de tempo.
- `401 Unauthorized`: Credenciais inválidas.

## Recurso `/usuarios/transferencia`

### `POST`

Realiza uma transferência entre carteiras de usuários.

**Parâmetros:**

- `cpf` (int): CPF do usuário que está realizando a transferência.
- `value_payer` (float): Valor da transferência.
- `cpf_payee` (int): CPF do usuário que receberá a transferência.

**Respostas:**

- `200 OK`: Transferência realizada com sucesso.
- `404 Not Found`: Usuário não encontrado.
- `422 Unprocessable Entity`: Valor da transferência inválido ou não há saldo suficiente na carteira do usuário que está realizando a transferência.
