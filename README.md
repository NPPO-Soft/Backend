# Backend

This repository contains the backend implementation for a web application that manages testimonials, team members, recruitments, and historical records.

## Project Structure

```
├── .env                    # Environment configuration
├── .gitignore             # Git ignore rules
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── database/
│   └── mongo_database.py  # MongoDB database connection handling
├── routes/
│   └── route.py          # API and route definitions
├── scripts/
│   └── scripts.py        # Utility scripts
├── templates/            # HTML templates
│   ├── history.html
│   ├── index.html
│   ├── recruitments.html
│   ├── teams.html
│   └── testimonials.html
└── utils/
    └── utils.py         # Utility functions
```

## Features

The backend provides the following main functionalities:

### Testimonials Management
- View testimonials
- Add new testimonials
- Delete testimonials
- API endpoint for testimonials data

### Team Management
- View team members
- Add new team members
- Delete team members
- API endpoint for team data

### Recruitment System
- Submit recruitment applications
- Check interview status
- Manage recruitment records
- Set interview dates

### Historical Records
- View historical records
- Add new records
- Delete records
- API endpoint for history data

## Setup

1. Clone the repository
2. Create and configure `.env` file with necessary environment variables
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
python app.py
```

## API Endpoints

The application exposes several API endpoints:

- `GET /api/testimonials` - Retrieve testimonials
- `GET /api/teams` - Retrieve team members
- `GET /api/history` - Retrieve historical records

## Database

The application uses MongoDB as its database, with connection handling implemented in `database/mongo_database.py`. The database interface provides methods for:
- Getting database collections
- Accessing specific databases

## File Upload

The system includes file upload functionality with supported file types verification through the `allowed_file()` function.

## Templates

The application uses HTML templates for rendering different pages:
- `index.html` - Main landing page
- `testimonials.html` - Testimonials management
- `teams.html` - Team members management
- `recruitments.html` - Recruitment system
- `history.html` - Historical records
