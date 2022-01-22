
<h1 align="center">Insider Unlocked</h1>
<div align="center">
Insider Unlocked is an ongoing web application we have been co-developing for the past few months which aggregates stock trading data of US senators and presents it in a digestible manner for the average retail investor.
</div>
<div align="center">
  <h3>
    <a href="https://insiderunlocked.web.app/">
      Website
    </a>
    <span> | </span>
    <a href="https://github.com/InsiderUnlocked/Insider-Unlocked/blob/main/Data%20Science/notebook.ipynb">
      Data Analysis
    </a>
    <span> | </span>
    <a href="https://github.com/InsiderUnlocked/Insider-Unlocked/tree/main/Product%20Managmento">
      Product Management
    </a>
    <span> | </span>
        <a href="https://github.com/InsiderUnlocked/Backend#readme">
      API
    </a>
  </h3>
</div>



## Table of Contents
- [Tech-Stack](#Tech-Stack)
- [Usage](#Usage)
- [Documentation](#Documentation)
- [License](#License)

# Tech-Stack
- [Django](https://docs.djangoproject.com/en/4.0/)
- [SQLite](https://www.sqlite.org/docs.html)

# Installation

### Code and dependencies
```console
$ git clone https://github.com/InsiderUnlocked/Backend.git
$ cd Backend
$ pip install -r requirements.txt
```
### Usage
Run Migrations
```console
$ python manage.py makemigrations
$ python manage.py migrate
```

Populate Database (>6 hours to run)
```console
$ python manage.py populateDB
```

Run Server
```console
$ python manage.py runserver
```

# Documentation


# License
[MIT](https://tldrlegal.com/license/mit-license)
