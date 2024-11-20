from flask import Flask, render_template, request,  jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Asteroid(db.Model):
    id_num = db.Column(db.Integer, primary_key=True, index=True)
    id = db.Column(db.String(64), index=False)
    number = db.Column(db.Integer, primary_key=False)
    name = db.Column(db.String(64), index=False)
    orb_class = db.Column(db.String(256))
    a = db.Column(db.Float)
    e = db.Column(db.Float)
    i = db.Column(db.Float)
    orb_period = db.Column(db.Float)
    family_number = db.Column(db.Integer)
    family_name = db.Column(db.String(120))
    albedo = db.Column(db.Float)
    absolute_magnitude = db.Column(db.Float)
    density = db.Column(db.Float)
    diameter = db.Column(db.Float)
    tax_class = db.Column(db.String(12))
    thermal_inertia = db.Column(db.Float)
    spin = db.Column(db.Float)

    def to_dict(self):
        return {
            'id_num': self.id_num,
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'class': self.orb_class,
            'a': self.a,
            'e': self.e,
            'i': self.i,
            'orbital_period': self.orb_period,
            'family_number': self.family_number,
            'family_name': self.family_name,
            'albedo': self.albedo,
            'mag': self.absolute_magnitude,
            'density': self.density,
            'diameter': self.diameter,
            'taxonomy class': self.tax_class,
            'thermal inertia': self.thermal_inertia,
            'spin': self.spin,


        }


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('welcome_page.html')


@app.route('/asteroid_table')
def asteroid_table():
    return render_template('asteroid_table.html')


@app.route('/user_guide')
def user_guide():
    return render_template('user_guide.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


# @app.route('/api/data')
# def data():
#     return {'data': [ast.to_dict() for ast in Asteroid.query]}

@app.route('/api/data')
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

@app.route('/filter_results', methods=['POST'])
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

# @app.route("/download_csv", methods=["POST"])
# def download_csv():
#     data = request.form.get('sqlite:///sqlite.db')
#
#     #data = request.form.get('data')
#     print('Save button clicked')
#     print("Received data:", data)
#     if not data:
#         return "No data provided.", 400
#
#     try:
#         data = pd.read_json(data)
#     except ValueError as e:
#         return f"Invalid data format: {e}", 400
#
#     if data.empty:
#         return "No data to download."
#
#     # Use BytesIO to save the CSV in memory
#     bytes_io = BytesIO()
#     data.to_csv(bytes_io, index=False)
#     bytes_io.seek(0)
#
#     return send_file(bytes_io, as_attachment=True, download_name="asteroids.csv", mimetype='text/csv')

@app.route("/api/data")
def get_data():
    asteroids = Asteroid.query.all()
    data = [ast.to_dict() for ast in asteroids]
    return jsonify(data=data)

def run_app(*args, **kwargs):
    app.run(debug=False)


# if __name__ == "__main__":
#     app.run(debug=False)