"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Person, Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/planet', methods=['POST', 'GET'])
def get_planet():
    all_planet = Planet.query.all()
    if all_planet is None:
        return jsonify("Sorry! No star wars planet found!"), 404
    else:
        all_planet = list(map(lambda x: x.serialize(), all_planet))
        return jsonify(all_planet), 200


@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    single_planet = db.session.get(Planet, planet_id)
    if single_planet is None:
        raise APIException(
            f"Planet ID {planet_id} was not found", status_code=404)

    single_planet = single_planet.serialize()
    return jsonify(single_planet), 200


@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    single_planet = db.session.get(Planet, planet_id)
    # all_planet = Planet.query.all()
    if single_planet is None:
        raise APIException("Planet was not valid!", status_code=404)

    single_planet = single_planet.serialize()
    return jsonify(single_planet), 200


@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    data = request.get_json()
    user_id = data.get("user_id")
    planet = db.session.get(Planet, planet_id)
    user = db.session.get(User, user_id)
    if user is None or planet is None:
        raise APIException("Planet or user cannot found", status_code=404)

    if planet in user.favorite_planet:
        user.favorite_planet.remove(planet)
        db.session.commit()
        return jsonify(f"{planet.name} removed successfully"), 200
    else:
        return jsonify(f"{planet.name} is not in favorites"), 400


@api.route('/people', methods=["GET"])
def get_people():
    all_people = Person.query.all()
    if all_people is None:
        return jsonify("Sorry! No star wars characters found!"), 404
    else:
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200


@api.route('/people/<int:person_id>', methods=['GET'])
def get_single_person(person_id):

    single_person = db.session.get(Person, person_id)
    if single_person is None:
        raise APIException(
            f"Person ID {person_id} was not found", status_code=404)

    single_person = single_person.serialize()
    return jsonify(single_person), 200


@api.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user = request.get_json()
    print(user)
    user = db.session.get(User.user["user_id"])
    person = db.session.get(Person, person_id)

    user.favorite_people.append(person)
    db.session.commit()

    return jsonify(f'User {user.username} has added {person.name} to their favorites,'), 200


@api.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def remove_favorite_person(person_id):
    data = request.get_json()
    user_id = data.get("user_id")
    person = db.session.get(Person, person_id)
    user = db.session.get(User, user_id)
    if user is None or person is None:
        raise APIException("Person or user cannot found", status_code=404)

    if person in user.favorite_people:
        user.favorite_people.remove(person)
        db.session.commit()
        return jsonify(f"{person.name} removed successfully"), 200
    else:
        return jsonify(f"{person.name} is not in favorites"), 400


@api.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    if all_users is None:
        return jsonify('Sorry! No user found!'), 404
    else:
        all_users = list(map(lambda x: x.serialize(), all_users))
        return jsonify(all_users), 200


@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    current_users = db.session.get(User, user_id)
    if current_users is None:
        return APIException('Sorry! No user found!', status_code=404)

    all_people = [each_person.serialize()
                  for each_person in current_users.favorite_people]

    response = {
        "message": f'User {current_users.username}\'s list of favorite people',
        "data": all_people,
    }

    return jsonify(response), 200
