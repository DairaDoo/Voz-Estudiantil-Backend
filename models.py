# import datetime
# from sqlalchemy import Enum
# from enum import Enum as Enum2
# from flask_sqlalchemy import SQLAlchemy

# # Instancia de SQLAlchemy
# db = SQLAlchemy()

# # Enum global para el estado
# state_enum = Enum('pendiente', 'aprobado', 'rechazado', name='state_enum')

# class Campus(db.Model):
#     __tablename__ = 'campus'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     university_id = db.Column(db.Integer, db.ForeignKey('universities.university_id'))

#     university = db.relationship('University', back_populates='campuses')

# class Comment(db.Model):
#     __tablename__ = 'comment'
#     comment_id = db.Column(db.Integer, unique=True, primary_key=True)
#     review_id = db.Column(db.Integer, db.ForeignKey('review.review_id'), nullable=False)
#     comment = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

#     review = db.relationship('Review', backref='comments', lazy=True)
#     user = db.relationship('User', backref='comments', lazy=True)
# \
# class Department(db.Model):
#     __tablename__ = 'department'
#     department_id = db.Column(db.Integer, unique=True, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     university_id = db.Column(db.Integer, db.ForeignKey('universities.university_id'), nullable=False)

#     university = db.relationship('University', back_populates='departments')
#     professors = db.relationship('Professors', back_populates='department')

# class Event(db.Model):
#     __tablename__ = 'event'
#     event_id = db.Column(db.Integer, primary_key=True, unique=True)
#     event_title = db.Column(db.String(120), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
#     up_vote = db.Column(db.Integer, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     university_id = db.Column(db.Integer, nullable=False)
#     state = db.Column(state_enum, default='pendiente', nullable=False)
#     image_name = db.Column(db.String(200), nullable=True)

#     user = db.relationship('User', backref='events', lazy=True)

# class Moderation(db.Model):
#     __tablename__ = 'moderation'
#     moderation_id = db.Column(db.Integer, unique=True, primary_key=True)
#     related_content_id = db.Column(db.Integer)
#     content_type = db.Column(db.String(100), nullable=False)
#     state = db.Column(state_enum, default='pendiente', nullable=False)
#     rejection_reason = db.Column(db.Text, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     revision_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

#     user = db.relationship('User', backref='moderations', lazy=True)

# class Professors_Questions(db.Model):
#     __tablename__ = 'professors_questions'
#     question_id = db.Column(db.Integer, primary_key=True)
#     question_text = db.Column(db.String(120), nullable=False)
#     is_question_active = db.Column(db.Boolean, nullable=False)

# class Professors_Responses(db.Model):
#     __tablename__ = 'professors_responses'
#     responses_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     professor_id = db.Column(db.Integer, db.ForeignKey('professors.professors_id'), nullable=False)
#     question_id = db.Column(db.Integer, db.ForeignKey('professors_questions.question_id'), nullable=False)
#     answer = db.Column(db.Integer, nullable=False)
#     response_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
#     state = db.Column(state_enum, default='pendiente', nullable=False)

#     user = db.relationship('User', backref='professors_responses', lazy=True)
#     professor = db.relationship('Professors', backref='professors_responses', lazy=True)
#     question = db.relationship('Professors_Questions', backref='professors_responses', lazy=True)

# class Professors(db.Model):
#     __tablename__ = 'professors'
#     professors_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), nullable=False)
#     overall_rating = db.Column(db.Float, nullable=False)
#     state = db.Column(state_enum, default='pendiente', nullable=False)

#     department = db.relationship('Department', back_populates='professors')

# class Report_category(db.Model):
#     __tablename__ = 'report_category'
#     report_category_id = db.Column(db.Integer, primary_key=True)
#     category_name = db.Column(db.String(120), unique=True, nullable=False)

# class Report(db.Model):
#     __tablename__ = 'report'
#     report_id = db.Column(db.Integer, primary_key=True, unique=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     report_category_id = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(100), nullable=True)
#     review_id = db.Column(db.Integer, nullable=False)

# class Review(db.Model):
#     __tablename__ = 'review'
#     review_id = db.Column(db.Integer, primary_key=True, unique=True)
#     review = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     image_name = db.Column(db.String(200), nullable=True)
#     create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
#     up_vote = db.Column(db.Integer, nullable=True)
#     down_vote = db.Column(db.Integer, nullable=True)
#     university_id = db.Column(db.Integer, db.ForeignKey('universities.university_id'), nullable=False)
#     state = db.Column(state_enum, default='pendiente', nullable=False)

#     user = db.relationship('User', backref='review', lazy=True)
#     university = db.relationship('University', back_populates='reviews')

# class University(db.Model):
#     __tablename__ = 'universities'
#     university_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

#     campuses = db.relationship('Campus', back_populates='university')
#     departments = db.relationship('Department', back_populates='university')
#     reviews = db.relationship('Review', back_populates='university')

# class User(db.Model):
#     __tablename__ = 'users'
    
#     class RoleEnum(Enum2):
#         usuario = "usuario"
#         moderador = "moderador"
#         administrador = "administrador"

#     user_id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
#     university_id = db.Column(db.Integer, db.ForeignKey('universities.university_id'), nullable=True)
#     rol = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.usuario)
    
#     university = db.relationship('University', backref='users', lazy=True)

#     def __repr__(self):
#         return f'<User {self.name}, Email: {self.email}>'
