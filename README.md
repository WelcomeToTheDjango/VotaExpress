# VotaExpress

## Criar ambiente virtual

```bash
python3 -m venv venv
```

## Ativar ambiente virtual
 
```bash
source venv/bin/activate
```

## Instalar dependências

```pip
pip3 install -r requirements.txt
```

## Crie um arquivo .ENV

> Por motivos de segurança não disponibilizamos nossa SECRET_KEY aqui, mas você pode criar um arquivo .env na raiz do seu projeto

```bash
echo SECRET_KEY="your-secret-here" > .env
```

## Faça as migrações

```bash
python3 manage.py migrate
```

## Iniciar server

```pip
python3 manage.py runserver
```

## Tests

```bash
python3 manage.py test
```

## Carregar Banco de Dados (opcional)

```bash
python3 manage.py loaddata initdata.json
```
