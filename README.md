# NGO Support Finder 3

NGO Support Finder 3 is a responsive web application that helps donors, volunteers, and beneficiaries discover NGOs by category, location, and purpose. It includes a searchable directory, a support request form, and a lightweight SQLite database backend.

## Features
- Search NGOs by name, cause, or location
- Filter NGOs by category
- View NGO contact and support details
- Submit support requests from the web interface
- Built with Python Flask and SQLite
- Fully responsive interface using HTML5, CSS3, JavaScript, and Bootstrap

## Tech Stack
- Frontend: HTML5, CSS3, JavaScript, Bootstrap
- Backend: Python Flask
- Database: SQLite

## Project Structure
- `app.py` – Flask application and database initialization
- `templates/index.html` – main web interface
- `static/css/style.css` – custom styling
- `static/js/script.js` – frontend logic and API calls
- `ngo_support_finder.db` – SQLite database created at runtime

## Run Locally
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python app.py
   ```
4. Open your browser at:
   ```text
   http://127.0.0.1:5000
   ```

## Default NGO Categories
- Education
- Environment
- Women Empowerment
- Healthcare
- Food Security
- Housing

## License
This project is licensed under the MIT License.
