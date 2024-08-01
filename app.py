import os
from dotenv import load_dotenv
from work_hours_app import app
from work_hours_app.models import User, Entry


if __name__ == "__main__":
    # Load dotenv vars
    load_dotenv()
    environment = os.getenv('ENVIRONMENT',  'development')

    if environment == "production":
        load_dotenv('.env.production')
    elif environment == "development":
        load_dotenv('.env.development')
    else:
        raise ValueError("Invalid environment name")

    app.run(debug=os.getenv("DEBUG_LEVEL"))