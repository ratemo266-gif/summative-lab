from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    # TABLE CONSTRAINT 1: Unique name
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade="all, delete-orphan")

    # MODEL VALIDATION 1: Exercise name length
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError("Exercise name must be at least 3 characters long.")
        return name

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade="all, delete-orphan")

    # MODEL VALIDATION 2: Duration must be positive
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is not None and duration <= 0:
            raise ValueError("Workout duration must be a positive integer.")
        return duration

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # TABLE CONSTRAINT 2: Reps must be non-negative
    __table_args__ = (db.CheckConstraint('reps >= 0', name='check_reps_positive'),)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
