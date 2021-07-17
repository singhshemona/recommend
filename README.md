# Wrec - Readme.md
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Let's build a world where recommendations give you a breadth of knowledge, not just depth.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
	- [Generator](#generator)
- [Example Readmes](#example-readmes)
- [Related Efforts](#related-efforts)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)


## Background
This idea started off with the idea of "I don't know what I don't know" when it comes to consuming things like books, music and movies. Every recommendation system is trying to keep you within your bubble of interests but we want to build something that makes you aware of what else is out there, especially to try something new for the first time.

## Install

1. `git clone https://github.com/singhshemona/recommmend.git`
2. `cd recommmend`


## To run backend (Flask):

1. Set up a new virtual environment using venv or conda
2. `cd backend_flask`
3. make sure `pip` is installed
4. Install all packages from the `requirements.txt` - only need to do this once
	- Using pip: `pip install -r requirements.txt`
	- Using conda:`conda install --yes --file requirements.txt`
	- If using a mac: `python -m pip install -r requirements.txt` if running on a mac 
5. Add environment variables or set them in your current terminal (see next section)
6. `flask run` to run the app
7. click on development server in terminal [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
8. Navitage to [/john/books](http://127.0.0.1:5000/john/books/) to see a json of books under username 'John'


### Environment variables:

**For Linux and macOS**
export FLASK_APP=wrec.py
export FLASK_DEBUG=1

**Microsoft Window**
set FLASK_APP=wrec.py
set FLASK_DEBUG=1


## To run frontend:
1. `npm install`
2. `npm start`
3. Open [http://localhost:3000](http://localhost:3000) in browser. The page will reload if you make edits.

## Contributing:
Please follow along this excellent [step-by-step guide](https://www.dataschool.io/how-to-contribute-on-github/) to learn how to contribute to an open-source project

**Quick summary**
1. Make desired changes 
2. Add, commit, push
3. Open pull request

## License