from app import app
from models import db, Exercise, Workout, WorkoutExercise
with app.app_context():
    print("Clearing tables...")
    WorkoutExercise.query.delete(); Workout.query.delete(); Exercise.query.delete()
    print("Adding starter exercises...")
    e1 = Exercise(name="Pushups", category="Calisthenics"); e2 = Exercise(name="Squats", category="Weights")
    db.session.add_all([e1, e2]); db.session.commit()
    print("Adding starter workouts...")
    w1 = Workout(date="2023-10-30", duration_minutes=60, notes="Full body day")
    db.session.add(w1); db.session.commit()
    print("Connecting exercises to workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=4)
    db.session.add(we1); db.session.commit()
    print("Seed successful!")
