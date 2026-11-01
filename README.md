# Sumative Lab - Workout Tracker API

A Flask REST API for tracking workouts, exercises, and the connection between them. Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Validation](#validation)
- [Getting Started](#getting-started)
- [Seeding the Database](#seeding-the-database)
- [Running the App](#running-the-app)

## Tech Stack

- **Framework:** Flask 2.2.2
- **ORM:** Flask-SQLAlchemy 3.0.3
- **Migrations:** Flask-Migrate 3.1.0
- **Serialization:** Marshmallow 3.20.1 + Flask-Marshmallow
- **DB Constraint Naming:** SQLAlchemy MetaData naming convention
- **Python:** 3.13

## Project Structure

```
sumative-lab/
├── Pipfile                  # Dependency management (Pipenv)
├── Pipfile.lock             # Locked dependencies
└── server/
    ├── app.py               # Flask app, schemas, and routes
    ├── models.py            # SQLAlchemy models
    ├── seed.py              # Database seeding script
    ├── migrations/          # Alembic migration files
    └── instance/            # SQLite database location
```

## Database Schema

Three tables with the following relationships:

### Exercises
Stores individual exercise definitions.
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String | NOT NULL, UNIQUE |
| category | String | NOT NULL |
| equipment_needed | Boolean | Default: False |

### Workouts
Stores workout sessions.
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| date | String | NOT NULL |
| duration_minutes | Integer | |
| notes | Text | |

### Workout Exercises
Junction table connecting workouts to exercises with session details.
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| workout_id | Integer | FK -> workouts.id, NOT NULL |
| exercise_id | Integer | FK -> exercises.id, NOT NULL |
| reps | Integer | CheckConstraint: >= 0 |
| sets | Integer | |
| duration_seconds | Integer | |

### Relationships
- One workout to many workout_exercises (cascade delete)
- One exercise to many workout_exercises (cascade delete)

## API Endpoints

All endpoints return JSON. Base URL: `http://localhost:5555`

### Workouts
| Method | Path | Description |
|--------|------|-------------|
| GET | `/workouts` | List all workouts (includes nested workout_exercises) |
| POST | `/workouts` | Create a new workout |
| GET | `/workouts/<id>` | Get a single workout by ID |
| DELETE | `/workouts/<id>` | Delete a workout by ID |

### Exercises
| Method | Path | Description |
|--------|------|-------------|
| GET | `/exercises` | List all exercises |
| POST | `/exercises` | Create a new exercise |
| GET | `/exercises/<id>` | Get a single exercise by ID |
| DELETE | `/exercises/<id>` | Delete an exercise by ID |

### Workout Exercises
| Method | Path | Description |
|--------|------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps/sets/duration |

## Validation

### Model-Level (SQLAlchemy `@validates`)
- **Exercise name:** Must be at least 3 characters long
- **Workout duration:** If provided, must be a positive integer

### Schema-Level (Marshmallow)
- **Exercise name:** `validate.Length(min=3)`
- **WorkoutExercise reps:** `validate.Range(min=0)`
- **WorkoutExercise sets:** `validate.Range(min=0)`

### Database-Level
- **Exercise name:** `UNIQUE` constraint
- **WorkoutExercise reps:** `CheckConstraint('reps >= 0')`

## Getting Started

### Prerequisites
- Python 3.13
- Pipenv

### Installation
```bash
pipenv install
pipenv shell
```

### Database Setup
```bash
cd server
flask db init              # Initialize migrations (first time only)
flask db migrate -m "Initial migration"
flask db upgrade head
```

## Seeding the Database

Run the seed script to populate the database with starter data:
```bash
cd server
pipenv run python seed.py
```

This creates:
- 2 exercises: Pushups (Calisthenics), Squats (Weights)
- 1 workout: Full body day on 2023-10-30 (60 minutes)
- 1 workout exercise: Pushups linked to the workout (15 reps, 4 sets)

## Running the App

```bash
cd server
pipenv run python app.py
```

The server will start on `http://localhost:5555` with debug mode enabled.