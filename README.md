# VotaExpress

## Criar ambiente virtual

```python
python3 -m venv venv
```

## Ativar ambiente virtual
 
```python
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

## Iniciar server

```pip
python3 manage.py runserver
```

## Tests

```python
python3 manage.py test
```

## Carregar Banco de Dados (opcional)

```python
python3 manage.py loaddata initdata.json
```