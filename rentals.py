from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

rentals_bp = Blueprint('rentals', __name__)

# 렌탈 일정 신청
# 특정 시간의 렌탈 일정 추가
@rentals_bp.route('/create', methods=['POST'])
def rentals_create():

    data = request.json
    spaceid = data.get('spaceid')
    starttime = data.get('starttime')
    endtime = data.get('endtime')
    curtime = datetime.utcnow

    # TODO : Rentals, ClubTimeslot, 조교 재량 시간?? 에 대한 체크 수행 후 가능하면 추가.
    
    
# 렌탈 일정 조회(주 단위)
@rentals_bp.route('/week', methods=['GET'])
def rentals_week():
    data = request.json
    spaceid = data.get('spaceid')
    week = data.get('week')

    week_start = datetime.strptime(week, '%Y-%m-%d')

    week_end = week_start + timedelta(days=7)

    rentals_in_week = Rentals.query.filter(Rentals.spaceid==spaceid,Rentals.starttime >= week_start, Rentals.starttime < week_end).all()

    if not rentals_in_week:
        return jsonify({'error': 'no rentals in the week'}), 404

    rentals_data = []
    for rental in rentals_in_week:
        rentals_data.append({
            'rentalid': rental.rentalid,
            'spaceid': rental.spaceid,
            'userid': rental.userid,
            'starttime': rental.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            'endtime': rental.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            'createtime': rental.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'status': rental.status,
            'minpeoplemet': rental.minpeoplemet
        })

    return jsonify(rentals_data), 200

# 렌탈 일정 조회(일 단위)
# TODO for front :
# 'TYPE' 속성을 통해 rental 과 clubrental 을 구분하여 관리해야 합니다.
@rentals_bp.route('/day', methods=['GET'])
def rentals_day():
    data = request.json
    spaceid = data.get('spaceid')
    day = data.get('day')

    day_start = datetime.strptime(day, '%Y-%m-%d')
    day_end = day_start + timedelta(days=1)
    day_of_week = methods_convert_dayofweek(day_start.strftime('%A'))

    rentals_in_day = Rentals.query.filter_by(Rentals.spaceid==spaceid, Rentals.starttime >= day_start, Rentals.endtime < day_end).all()
    
    if not rentals_in_day :
        return jsonify({'msg' : "No rentals in day"}), 200

    rentals_data = []
    for rental in rentals_in_day:

        rentalid = rental.rentalid
        userid = rental.userid
        starttime = rental.starttime.strftime('%Y-%m-%d %H:%M:%S')
        endtime = rental.endtime.strftime('%Y-%m-%d %H:%M:%S')
        createtime = rental.createtime.strftime('%Y-%m-%d %H:%M:%S')
        maxpeolple = rental.maxpeolple
        people = rental.people
        minpeolple = rental.minpeolple
        if rental.status == 2 :
            status = "Failed"
        else :
            status = methods_convert_status(maxpeolple,people,minpeolple).json.get('status')

        rentals_data.append({
            'rentalid': rentalid,
            'userid': userid,
            'starttime': starttime,
            'endtime': endtime,
            'createtime': createtime,
            'status': status,
            'people': people,
            'maxpeople' : maxpeople,
        })
    return jsonify(rentals_data), 200


# 렌탈 일정 참가
# TODO for front :
# rental 과 clubrental 에 대한 참가 신청을 구분하여 수행해야 합니다.
@rentals_bp.route('/join', methods=['GET'])
def rentals_join():
    data = request.json
    rentalid = data.get('rentalid')
    userid = data.get('userid')

    # TODO : Rentals 의 status 를 통해 참여 가능한지 확인하고, 가능한 경우 RentalParticipants 에 등록

@rentals_bp.route('/clubrental/join', methods=['GET'])
def rentals_join():
    data = request.json
    rentalid = data.get('rentalid')
    userid = data.get('userid')

    # TODO : Rentals 의 status 를 통해 참여 가능한지 확인하고, 가능한 경우 RentalParticipants 에 등록

