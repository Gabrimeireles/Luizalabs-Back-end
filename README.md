# Sistema Bancario em POO (Python)

Projeto desenvolvido no **bootcamp DIO | Luizalabs - Back-end com Python - 2ª Edicao**.

Repositorio de estudo e evolucao de um sistema bancario no terminal, modelado com Programacao Orientada a Objetos (POO).

## Sobre o projeto

Este projeto implementa operacoes bancarias basicas com foco em boas praticas de modelagem:

- cadastro de clientes (`PessoaFisica`)
- criacao de contas (`ContaCorrente`)
- deposito
- saque com regras de limite
- extrato com historico de transacoes

A aplicacao roda via CLI (terminal) e foi estruturada para facilitar manutencao e expansao de funcionalidades.

## Contexto academico

Desafio pratico do bootcamp **DIO | Luizalabs - Back-end com Python - 2ª Edicao**, com foco em:

- fundamentos de Python
- modelagem orientada a objetos
- regras de negocio bancarias
- evolucao de codigo procedural para POO

## Status

Em desenvolvimento ativo.

## Tecnologias

- Python 3.x
- Programacao Orientada a Objetos

## Estrutura do repositorio

- [`banco_poo.py`](./banco_poo.py): implementacao principal do sistema
- [`.gitignore`](./.gitignore): regras de ignorar arquivos locais e de ambiente

## Modelo de dominio (UML)

Classes principais aplicadas:

- `Cliente`
- `PessoaFisica`
- `Conta`
- `ContaCorrente`
- `Historico`
- `Transacao` (abstrata)
- `Deposito`
- `Saque`

## Como executar

### 1) Clonar o repositorio

```bash
git clone <URL_DO_REPOSITORIO>
cd Luizalabs-Back-end
```

### 2) Executar a aplicacao

```bash
python banco_poo.py
```

## Funcionalidades atuais

- [x] Criar usuario
- [x] Criar conta corrente
- [x] Depositar
- [x] Sacar com limite por operacao
- [x] Limite diario de saques
- [x] Exibir extrato
- [x] Listar contas

## Proximos passos

- [ ] Persistencia em banco de dados (SQLite/PostgreSQL)
- [ ] Testes automatizados (pytest)
- [ ] Separacao em modulos (`models`, `services`, `main`)
- [ ] Camada de autenticacao basica

## Autor

- Nome: `Gabriel Resende Meireles`
- LinkedIn: `https://www.linkedin.com/in/Gabrimeireles`
- Email: `seu-email@dominio.com`
