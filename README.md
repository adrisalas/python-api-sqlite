[![Python Version](https://img.shields.io/badge/Python-3.8-blue)](https://hub.docker.com/_/python) [![License](https://img.shields.io/github/license/adrisalas/python-sqlite-api)](https://coveralls.io/github/shotgunsoftware/python-api?branch=master) [![Twitter Follow](https://img.shields.io/twitter/follow/adrisalas_.svg?style=social)](https://twitter.com/adrisalas_)  

# Python API with SQLite

Simple project to serve as a basis for creating APIs in Python using Flask and SQLite

## Installation

##### Option 1: Default
```bash
git clone https://github.com/adrisalas/python-sqlite-api.git
cd ./api/
pip install Flask
pip install sqlite
python app.py
```
##### Option 2: In a Docker container
```bash
git clone https://github.com/adrisalas/python-sqlite-api.git
docker build -t pythonapi
docker run -p 4000:80 pythonapi
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Screenshots