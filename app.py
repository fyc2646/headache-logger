from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
from io import BytesIO

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'headache.db')
db = SQLAlchemy(app)

class HeadacheLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    # Triggers
    food_drink = db.Column(db.Text)
    stress_level = db.Column(db.String(50))
    sleep_hours = db.Column(db.Float)
    sleep_quality = db.Column(db.String(50))
    weather = db.Column(db.String(100))
    screen_time = db.Column(db.String(50))
    menstrual = db.Column(db.String(50))
    
    # Symptoms
    symptoms = db.Column(db.Text)
    
    # Medication
    medication = db.Column(db.Text)
    medication_effectiveness = db.Column(db.Integer)
    
    # Notes
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': self.duration,
            'severity': self.severity,
            'location': self.location,
            'food_drink': self.food_drink,
            'stress_level': self.stress_level,
            'sleep_hours': self.sleep_hours,
            'sleep_quality': self.sleep_quality,
            'weather': self.weather,
            'screen_time': self.screen_time,
            'menstrual': self.menstrual,
            'symptoms': self.symptoms,
            'medication': self.medication,
            'medication_effectiveness': self.medication_effectiveness,
            'notes': self.notes
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def log_headache():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['duration', 'severity', 'location']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Validate severity range
        try:
            severity = int(data['severity'])
            if not 1 <= severity <= 10:
                return jsonify({
                    'status': 'error',
                    'message': 'Severity must be between 1 and 10'
                }), 400
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Severity must be a number'
            }), 400

        # Handle optional numeric fields
        try:
            sleep_hours = float(data['sleep_hours']) if data.get('sleep_hours') else None
            medication_effectiveness = int(data['medication_effectiveness']) if data.get('medication_effectiveness') else None
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Sleep hours must be a number (e.g., 7.5) and medication effectiveness must be a number between 1-10'
            }), 400

        # Create log entry
        log = HeadacheLog(
            duration=data['duration'],
            severity=severity,
            location=data['location'],
            food_drink=data.get('food_drink'),
            stress_level=data.get('stress_level'),
            sleep_hours=sleep_hours,
            sleep_quality=data.get('sleep_quality'),
            weather=data.get('weather'),
            screen_time=data.get('screen_time'),
            menstrual=data.get('menstrual'),
            symptoms=data.get('symptoms'),
            medication=data.get('medication'),
            medication_effectiveness=medication_effectiveness,
            notes=data.get('notes')
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Log added successfully',
            'log_id': log.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = HeadacheLog.query.order_by(HeadacheLog.timestamp.desc()).all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/api/log/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    log = HeadacheLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Log deleted successfully'})

@app.route('/api/export', methods=['GET'])
def export_logs():
    logs = HeadacheLog.query.order_by(HeadacheLog.timestamp.desc()).all()
    
    # Create a BytesIO object to write CSV data
    si = BytesIO()
    # Write the BOM for Excel to correctly detect UTF-8
    si.write(b'\xef\xbb\xbf')
    
    output = []
    # Write headers
    headers = ['Date & Time', 'Duration', 'Severity', 'Location', 'Food/Drink', 
              'Stress Level', 'Sleep Hours', 'Sleep Quality', 'Weather', 
              'Screen Time', 'Menstrual', 'Symptoms', 'Medication', 
              'Medication Effectiveness', 'Notes']
    output.append(','.join(headers))
    
    # Write data rows
    for log in logs:
        row = [
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            str(log.duration),
            str(log.severity),
            str(log.location),
            str(log.food_drink) if log.food_drink else '',
            str(log.stress_level) if log.stress_level else '',
            str(log.sleep_hours) if log.sleep_hours else '',
            str(log.sleep_quality) if log.sleep_quality else '',
            str(log.weather) if log.weather else '',
            str(log.screen_time) if log.screen_time else '',
            str(log.menstrual) if log.menstrual else '',
            str(log.symptoms) if log.symptoms else '',
            str(log.medication) if log.medication else '',
            str(log.medication_effectiveness) if log.medication_effectiveness else '',
            str(log.notes) if log.notes else ''
        ]
        # Escape quotes and wrap fields in quotes to handle commas in text
        escaped_row = []
        for field in row:
            escaped_field = field.replace('"', '""')
            escaped_row.append(f'"{escaped_field}"')
        output.append(','.join(escaped_row))
    
    # Write all data to BytesIO
    si.write('\n'.join(output).encode('utf-8'))
    si.seek(0)
    
    return send_file(
        si,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'headache_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
