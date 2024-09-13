# Tracking Number Generator API

## Overview

This is a Django REST Framework API that generates unique tracking numbers for parcels. The API is designed to be scalable, efficient, and capable of handling high concurrency.

## Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone https://github.com/sanjaymehar/tracking-number.git
   
3. **Setup a virtual environment in Python:**
  - Create: `python -m venv venv`
  - To activate:
    - Windows CMD: `venv/Scripts/activate.bat`
    - Windows PowerShell: `./venv/bin/activate`
    - macOS / Linux: `source venv/bin/activate`
  
    - Note: if you are using pycharm then virtual env will automatically create

3. **Install Dependencies**
- `pip install -r requirements.txt`

4. **Apply Migrations**
- `python manage.py makemigrations`
- `python manage.py migrate`

5. **Run the Development Server**
- `python manage.py runserver`




