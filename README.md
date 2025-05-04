# fastapi-example

## Setup Instructions
1. Clone this repo
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file based on `.env.example`
5. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Navigate to `http://localhost:8000/docs` to access Swagger UI
