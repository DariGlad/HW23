import os

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from classes.query import Query
from config import DATA_DIR
from generators import generator_commands
from models.request_params import RequestParams

main_bp = Blueprint("main", __name__)


@main_bp.route("/perform_query/", methods=["POST"])
def perform_query():
    # Проверка правильности запроса
    try:
        req_value = RequestParams().load(request.values)
    except ValidationError as e:
        return e.messages, 400

    file_path = os.path.join(DATA_DIR, req_value["file_name"])  # Получаем путь к файлу
    query = Query(file_path)

    # Проверяем, существует ли файл
    try:
        params = generator_commands(req_value)
        result = query.get_query(params)
    except FileNotFoundError:
        return "FileNotFound", 400
    return jsonify(result)
