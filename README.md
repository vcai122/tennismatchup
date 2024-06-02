This project uses `pipenv` (See: https://pipenv.pypa.io/en/latest/). 

- Make sure you have `pipenv` installed. (Install with something like `pip install --user --upgrade pipenv`)
- Once installed, run `pipenv install` to install everything in the Pipfile.
- Use `pipenv shell` to activate the environment

Run Django commands in the environment
- `python3 manage.py runserver` to start the server
- Custom commands (See: https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/) can be run using `python3 manage.py command_name`
  - e.g. `python3 manage.py solve_schedule`
