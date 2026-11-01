from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, ValidationError
from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)

# --- SCHEMAS (Serialization & Schema Validations) ---
class ExerciseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Exercise
        load_instance = True
    id = ma.auto_field()
    # SCHEMA VALIDATION 1
    name = ma.auto_field(validate=validate.Length(min=3))
    category = ma.auto_field()
    equipment_needed = ma.auto_field()

class WorkoutExerciseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
    id = ma.auto_field()
    # SCHEMA VALIDATION 2
    reps = ma.auto_field(validate=validate.Range(min=0))
    sets = ma.auto_field(validate=validate.Range(min=0))
    duration_seconds = ma.auto_field()
    exercise = ma.Nested(ExerciseSchema)

class WorkoutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Workout
        load_instance = True
    id = ma.auto_field()
    date = ma.auto_field()
    duration_minutes = ma.auto_field()
    notes = ma.auto_field()
    workout_exercises = ma.Nested(WorkoutExerciseSchema, many=True)

exercise_schema, exercises_schema = ExerciseSchema(), ExerciseSchema(many=True)
workout_schema, workouts_schema = WorkoutSchema(), WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

# --- ENDPOINTS ---
@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        return make_response(workouts_schema.dump(Workout.query.all()), 200)
    elif request.method == 'POST':
        try:
            new_w = workout_schema.load(request.get_json(), session=db.session)
            db.session.add(new_w); db.session.commit()
            return make_response(workout_schema.dump(new_w), 201)
        except Exception as e:
            return make_response({"errors": [str(e)]}, 400)

@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    w = Workout.query.get(id)
    if not w: return make_response({"error": "Workout not found"}, 404)
    if request.method == 'GET': return make_response(workout_schema.dump(w), 200)
    db.session.delete(w); db.session.commit(); return make_response({}, 204)

@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        return make_response(exercises_schema.dump(Exercise.query.all()), 200)
    elif request.method == 'POST':
        try:
            new_e = exercise_schema.load(request.get_json(), session=db.session)
            db.session.add(new_e); db.session.commit()
            return make_response(exercise_schema.dump(new_e), 201)
        except Exception as e:
            return make_response({"errors": [str(e)]}, 400)

@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def exercise_by_id(id):
    e = Exercise.query.get(id)
    if not e: return make_response({"error": "Exercise not found"}, 404)
    if request.method == 'GET': return make_response(exercise_schema.dump(e), 200)
    db.session.delete(e); db.session.commit(); return make_response({}, 204)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        data = request.get_json()
        new_we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(new_we); db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except Exception as e:
        return make_response({"errors": [str(e)]}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
