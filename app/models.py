from app.extensions import db


class Asteroid(db.Model):
    AstNumber = db.Column(db.Integer, primary_key=True, index=True)
    AstName = db.Column(db.String(256), index=False)
    ProvisDesign = db.Column(db.String(64), index=False)
    orb_class = db.Column(db.String(10))
    a = db.Column(db.Float)
    e = db.Column(db.Float)
    i = db.Column(db.Float)
    H = db.Column(db.Float)
    diameter = db.Column(db.Float)
    diam_err = db.Column(db.Float)
    albedo = db.Column(db.Float)
    albedo_err = db.Column(db.Float)
    taxonomy_class = db.Column(db.String(12))

    def to_dict(self):
        return {
            'ast_number': self.AstNumber,
            'ast_name': self.AstName,
            'designation': self.ProvisDesign,
            'orb_class': self.orb_class,
            'a': self.a,
            'e': self.e,
            'i': self.i,
            'absolute_magnitude': self.H,
            'diameter': self.diameter,
            'diameter_err': self.diam_err,
            'albedo': self.albedo,
            'albedo_err': self.albedo_err,
            'taxonomy class': self.taxonomy_class
        }
