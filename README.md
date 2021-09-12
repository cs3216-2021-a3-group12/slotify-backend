# Slotify Backend
Home to the REST API server for Slotify.

# Setup Guide
1. git clone the repository (either via GitHub desktop or CLI)
  - `git clone <Project A>  # Cloning project repository`
2. change to project directory
 - `cd <Project A> # Enter to project directory`
3. create virtual environment
 - `python -m venv venv` # If not created, creating virtualenv
 - NOTE: for Mac, you may need to specify `python3` instead of `python`
4. activate virtual environment
 - Windows: `venv\Scripts\activate.bat`
 - Mac: `source ./venv/bin/activate` # Activating virtualenv
 - (Better) using VSCode, select the python interpreter within the `venv` folder and the above is done automatically
5. install dependencies
 - `pip install -r requirements.txt` # Installing dependencies
6. retrieve `.env` file from google drive
- https://drive.google.com/drive/folders/1BX8SO2EFzaKZPgH5Oh0fcTnit-xm4GOb
- place the `.env` file in the same directory as `slotify/settings.py`
- note that `.env` file must be ignored by Git
7. setup database
- according to the postgresql detail in `.env` file, create the database locally and the relevant database user.
8. apply migration
- `python manage.py migrate`

# Update dependencies
- to add a new package, go to the root directory and
  - `pip install packageName` # venv should be active
  - `pip freeze > requirements.txt` # update requirements.txt
  - NOTE: for Mac, you may need to specify `pip3` instead of `pip`

# Running the development server
Start the django development server by running the following in command-line (make sure that you are in the `slotify` directory with manage.py):
- `cd slotify`
- `python manage.py runserver`

