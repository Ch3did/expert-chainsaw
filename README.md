# Orçamento Oficina (ERP básico de Budgets)

Projeto **Django** focado em um **ERP básico de orçamentos (budgets)**, onde é possível montar um **budget** adicionando **serviços** e **produtos** relacionados para **validar e calcular o valor total** de cada orçamento.

> A interface do projeto é **exclusivamente pelo Django Admin** (`/admin`).  
> Não há telas públicas nem endpoints como foco principal.

## O que dá para fazer no Admin

- Criar e gerenciar **Budgets**
- Adicionar **Serviços** ao Budget (com quantidade e preço unitário no contexto do orçamento)
- Adicionar **Produtos** ao Budget (com quantidade e preço unitário no contexto do orçamento)
- Calcular o **valor total** do Budget somando serviços + produtos
- Validar regras do orçamento (ex.: estoque, valores, etc., conforme implementado nos models)

## Stack

- Python + Django
- PostgreSQL
- Docker + Docker Compose

## Como rodar com Docker Compose

### 1) Pré-requisitos

- Docker
- Docker Compose

### 2) Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto (ou ajuste conforme seu compose). Exemplo mínimo:

```env
# Postgres
POSTGRES_DB=oficina
POSTGRES_USER=oficina
POSTGRES_PASSWORD=oficina
POSTGRES_HOST=db
POSTGRES_PORT=5432

```

### 3) Subir os containers

Na raiz do projeto:

```bash
docker compose up --build
```

O container `web` executa:

- `python manage.py migrate`
- `python manage.py runserver 0.0.0.0:8000`

### 4) Criar usuário admin

Em outro terminal:

```bash
docker compose exec web python manage.py createsuperuser
```

### 5) Acessar o Admin

- Admin: `http://localhost:8000/admin`


## Observações

- O valor do budget deve ser recalculado quando serviços/produtos do orçamento mudarem (conforme sua implementação de `update_total_value` / signals / override de `save`).
- Para manter histórico de preços, o recomendado é salvar `unit_price` no item do orçamento (BudgetService/BudgetProduct), em vez de depender do preço atual do cadastro do serviço/produto.
