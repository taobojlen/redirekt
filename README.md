# redirekt

A web app that lets you create short URLs that grab data on anyone who clicks them. Includes an admin web interface.

**This is a research project. Do not use it for illegal or malicious purposes.**

## Developing

- Install dependencies:

```
pip install -r requirements.txt
yarn install
```

- Build JS: `yarn webpack`
- Run migrations: `python manage.py migrate`
- Run dev server: `python manage.py runserver`
- Visit `localhost:8000/admin`
