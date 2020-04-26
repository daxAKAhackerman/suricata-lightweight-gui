from flask import jsonify, request
from app.api import bp
from config import Config
from file_read_backwards import FileReadBackwards
import json


@bp.route('/eve', methods=['GET'])
def get_eve():

    data = request.args

    if 'size' not in data.keys():
        return jsonify({'error': 'Missing size'}), 400

    size = int(data['size'])

    if not size <= 10000 or not size > 0: 
        return jsonify({'error': 'Size must be between 0 and 10000'}), 400

    eve_json = []
    line_count = 0

    with FileReadBackwards(Config.SURICATA_EVE_FILE, encoding="utf-8") as file: 
        for line in file:
            eve_json.append(json.loads(line))
            line_count += 1
            if line_count == size:
                break


    return jsonify({'alerts': eve_json}), 200
