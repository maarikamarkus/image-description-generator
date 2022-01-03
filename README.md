# Image Description Generator

Simple Python/Flask web application to generate a description for your uploaded image.

At first Google Cloud Vision is used to generate keywords from your image.
These keywords are then fed to OpenAI-s GPT-3 engine to generate a description. 
If your image has EXIF data and it contains GPS information, then the information is reverse geocoded
using Google Geocoding API. Retrieved location details (city/town and country) is given in the prompt to the
GPT-3 engine to generate descritpion.

# Prepare

Create `.env` file:

    > cp .env.example .env

Get [OpenAI API key](https://beta.openai.com/account/api-keys) and add it to `.env`.

Get [Google API key](https://developers.google.com/maps/documentation/embed/get-api-key) and add it to `.env`.

Get [Google Credentials](https://cloud.google.com/vision/docs/labels#set-up-your-gcp-project-and-authentication) encode with base64 and add it to `.env`.

For encoding the credentials in CLI (assuming you have base64 in terminal and your secret file is named key.json):

    > cat key.json | base64 -w 0

# Build

Create virtualenv:

    > python -m venv venv

Activate virtualenv (Windows):

    > source venv/Scripts/activate

Or in UNIX:

    > source venv/bin/activate

Install necessary dependencies:

    > pip install -r requirements.txt

Create folder for temporarily storing uploaded files:

    > mkdir imgs

# Run

    > export FLASK_APP=server
    > flask run

**For auto reloading in development mode**, run this before `flask run`:

    > export FLASK_ENV=development

After you're finished with developing you can deactivate the venv:
  
    > deactivate

You can visit your application at `http://localhost:5000`.


