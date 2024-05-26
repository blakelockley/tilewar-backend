# django-docker-template

Template stack with Django/Django REST framework, PostgreSQL and Docker.

## Featues

- Custom EmailUser model
- Includes Django REST Framework
- Includes Django CORS Headers

## Environment Variables

### Production

Please provide an .env file.

### Development

The .env.dev file has been included.
**It is recommended you update the provided environemnt variables even if you are only running on localhost!**

- SECRET_KEY
- DB_PASSWORD
- POSTGRES_PASSWORD (in docker-compose.yaml)
