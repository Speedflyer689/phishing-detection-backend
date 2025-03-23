# Phishing Detection Backend

This project is a backend service for detecting phishing emails and URLs using machine learning models. It is built using Flask and Flask-RESTful.

## Project Structure


### `src/app.py`

The main entry point of the application. It initializes the Flask app, sets up CORS, registers error handlers, and adds resources to the API.

### `src/Procfile`

Defines the command to run the application using Gunicorn.

### `src/requirements.txt`

Lists the dependencies required to run the application.

### `src/interfaces/`

Contains the API interfaces.

- `api.py`: Imports necessary components from the `library.api` module.

### `src/library/`

Contains utility modules and configurations.

- `api.py`: Defines the base classes and utility functions for handling API requests and responses.
- `config.py`: Contains configuration settings for the application.
- `exceptions.py`: Defines custom exceptions used in the application.
- `flask.py`: Contains Flask middleware and error handling functions.
- `logger.py`: Sets up logging for the application.

### `src/resources/`

Contains the main resources and controllers for the application.

- `controller.py`: Defines the base controller and service factory for the application.
- `ml_models/`: Contains the machine learning models for phishing detection.
  - `phishing_email_detection/`: Contains the phishing email detection model.
  - `phishing_url_detection/`: Contains the phishing URL detection model.
- `modules/`: Contains the modules for handling phishing detection.
  - `is_phishing_email/`: Contains the components for phishing email detection.
    - `compute.py`: Defines the computation logic for phishing email detection.
    - `handler.py`: Handles the phishing email detection requests.
    - `input.py`: Defines the input schema for phishing email detection.
  - `is_phishing_url/`: Contains the components for phishing URL detection.
    - `compute.py`: Defines the computation logic for phishing URL detection.
    - `handler.py`: Handles the phishing URL detection requests.
    - `input.py`: Defines the input schema for phishing URL detection.

## Running the Application

To run the application locally, follow these steps:

1. Create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate
```
2. Install the dependencies:

```sh
pip install -r [requirements.txt](http://_vscodecontentref_/26)
```

3. Run the application

```sh
python [app.py](http://_vscodecontentref_/27)
```