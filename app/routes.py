from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from .models import db, Record
from .recognition.vosk_engine import SpeechRecognizer

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.username)

@main_bp.route('/record/upload', methods=['POST'])
@login_required
def upload_audio():
    if 'audio_blob' not in request.files:
        return jsonify({"error": "No audio file"}), 400
    
    audio_file = request.files['audio_blob']
    filename = secure_filename(f"{uuid.uuid4()}.webm")
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(file_path)

    try:
        recognizer = SpeechRecognizer()
        # Convert and transcribe
        wav_path = recognizer.convert_to_wav(file_path)
        raw_text = recognizer.transcribe(wav_path)
        command, identifier = recognizer.parse_command(raw_text)

        # Save to DB
        new_record = Record(
            user_id=current_user.id,
            audio_file_path=os.path.basename(wav_path), # Save relative path for wav
            raw_text=raw_text,
            command=command,
            identifier=identifier,
            status='pending'
        )
        db.session.add(new_record)
        db.session.commit()

        # Clean up original webm file
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "id": new_record.id,
            "raw_text": raw_text,
            "command": command,
            "identifier": identifier,
            "audio_url": url_for('static', filename=f"uploads/audio/{os.path.basename(wav_path)}")
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main_bp.route('/record/<int:record_id>/confirm', methods=['POST'])
@login_required
def confirm_record(record_id):
    record = Record.query.get_or_404(record_id)
    data = request.get_json()

    if 'command' in data:
        record.command = data['command']
    if 'identifier' in data:
        record.identifier = data['identifier']
    if 'corrected_text' in data:
        record.corrected_text = data['corrected_text']
    
    record.status = 'confirmed'
    record.confirmed_by_id = current_user.id
    db.session.commit()

    return jsonify({"status": "success"})

@main_bp.route('/history')
@login_required
def history():
    command_filter = request.args.get('command')
    identifier_filter = request.args.get('identifier')
    
    query = Record.query
    if command_filter:
        query = query.filter(Record.command == command_filter)
    if identifier_filter:
        query = query.filter(Record.identifier.like(f"%{identifier_filter}%"))
        
    records = query.order_by(Record.created_at.desc()).all()
    return render_template('history.html', records=records)
