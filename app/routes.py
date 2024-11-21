from flask import Blueprint, render_template, request, jsonify
from app.models import Asteroid
from app.extensions import db

main = Blueprint('main', __name__, template_folder='../templates', static_folder='../static')

@main.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@main.route('/asteroid_table')
def asteroid_table():
    return render_template('asteroid_table.html')


@main.route('/user_guide')
def user_guide():
    return render_template('user_guide.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@main.route('/api/data')
def data():
    query = Asteroid.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Asteroid.id_num.like(f'%{search}%'),
            Asteroid.a.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['id_num', 'a']:
            col_name = 'id_num'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Asteroid, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [ast.to_dict() for ast in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Asteroid.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@main.route('/filter_results', methods=['POST'])
def filter_results():
    keyword = request.form.get('keyword')
    min_value = request.form.get('min_value')
    max_value = request.form.get('max_value')
    filtered_results = []
    print("Received data:", keyword, min_value, max_value)

    if keyword and min_value and max_value:
        if keyword == 'SSO Number':
            filtered_results = [result.to_dict() for result in
                                Asteroid.query.filter(Asteroid.number.between(min_value, max_value)).all()]
            print(len(filtered_results))
            print(filtered_results)
        # Add more conditions for other filters
    return jsonify(data=filtered_results)


@main.route("/api/data")
def get_data():
    asteroids = Asteroid.query.all()
    data = [ast.to_dict() for ast in asteroids]
    return jsonify(data=data)