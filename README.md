# Campus Lost & Found Portal

Flask web app extracted from the supplied Google Colab notebook. It lets users submit Lost/Found reports and search the report list. MongoDB Atlas is used when `MONGO_URI` is configured; without it, the app displays sample/demo records and new reports are temporary in-memory data.

## Project structure

```text
campus-lost-found/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── render.yaml
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables `MONGO_URI` (your MongoDB Atlas connection string) and `SECRET_KEY` (a long random secret). You can copy `.env.example` as a reference, but this project does not automatically load `.env` files.
5. Start the development server:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000

## Deploy to Render

1. Push this folder to a GitHub repository.
2. In Render, create a Web Service and connect that repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add `MONGO_URI` and `SECRET_KEY` as Render environment variables.
6. Make sure MongoDB Atlas network access allows the hosted service to connect. Avoid committing credentials or using broad database access rules unless necessary.

`render.yaml` is provided as an optional Render Blueprint configuration. You still need to set the secret environment variables in Render.

## Important notes

- The original notebook's interface and report fields are preserved.
- The original app uses a hardcoded secret; this package changes it to read `SECRET_KEY` from the environment.
- The app currently falls back to demo mode if MongoDB is unavailable. Demo submissions are not persistent. Confirm the page says **Connected to MongoDB** and test persistence before using it with real campus reports.
- Report contact information is displayed publicly in the current UI. Use fictional details for demos; before a real deployment, consider a safer contact workflow and moderation.
