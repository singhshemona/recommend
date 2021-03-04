# Broadening Recommendations

Let's build a world where recommendations give you a breadth of knowledge, not just depth.

1. `git clone https://github.com/singhshemona/recommmend.git`
2. `cd recommmend`

## To run backend (Django):
1. `cd backend`
2. `pip install -r requirements.txt` to install all python packages (must have pip installed) or `conda install --yes --file requirements.txt` if using conda or `python -m pip install -r requirements.txt` if running on a mac  
3. `python manage.py migrate`
4. `python manage.py runserver`
5. click on development server in terminal [http://localhost:8000/](http://localhost:8000)
6. Navitage to [Books](http://127.0.0.1:8000/api/books/) to see a json of books
7. Navigate to [Registration](http://127.0.0.1:8000/register/)

## To run frontend:
1. `npm install`
2. `npm start`
3. Open [http://localhost:3000](http://localhost:3000) in browser. The page will reload if you make edits.

## To Contribute:
1. Make desired changes 
2. Add, commit, push
3. Open pull request