## Warehouse-control-API

### Description:
App for warehouse control by API.

### get started:
git clone project:
https://github.com/AxmetES/Warehouse-control-API.git

### got to project rep:
```cd /Warehouse-control-API```

### make .env file.
for example:
```
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_DB=db
POSTGRES_PORT=5432
POSTGRES_HOST=db

LOG_LEVEL = WARNING
LOG_FILE_PATH = app.log
```


### start app:
```docker-compose up --build```

### run tests:
```docker-compose run tests```

### Docs:
Swagger openapi.json

http://localhost:8000/docs#/


### example data:
products file with products list, 
for fill data base with example data.

### endpoint:
```/products/bulk```
