# Phase 3 Project. Therapist Connect- A Directory with Many_to_many relationship

from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///therapist.db')

Base = declarative_base()

therapist_speciality = Table(
    'therapist_speciality',
    Base.metadata,
    Column('therapist_id', Integer, ForeignKey('therapists.id')),
    Column('specialty_id', Integer, ForeignKey('specialties.id')),
    extend_existing=True
)

therapist_patient = Table(
    'therapist_patient',
    Base.metadata,
    Column('therapist_id', Integer, ForeignKey('therapists.id')),
    Column('patient_id', Integer, ForeignKey('patients.id')),
    extend_existing=True
)


class Therapist(Base):
    __tablename__ = 'therapists'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    location = Column(String())
    rating = Column(Float())
    total_ratings = Column(Integer())
    specialities = relationship(
        'Specialty', secondary=therapist_speciality, back_populates='therapists')
    patients = relationship(
        'Patient', secondary=therapist_patient, back_populates='therapists')

    def __repr__(self):
        return f'Therapist ID: {self.id}, ' + \
            f'Name: {self.name}, ' + \
            f'Location: {self.location}, ' + \
            f'Rating: {self.rating}, ' + \
            f'Total Ratings: {self.total_ratings})'


class Specialty(Base):
    __tablename__ = 'specialties'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    therapists = relationship(
        "Therapist", secondary=therapist_speciality, back_populates='specialities')

    def __repr__(self):
        return f'Specialty ID: {self.id}, ' + \
            f' Name: {self.name})'


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    therapists = relationship(
        'Therapist', secondary=therapist_patient, back_populates='patients')

    def __repr__(self):
        return f'Patient ID: {self.id}, ' + f'Name: {self.name}'


class TherapistDatabase:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def populate_sample_data(self):
        if self.session.query(Therapist).count() > 0:
            print("Sample data already exists. Skipping population.")
            return

        specialty1 = Specialty(name='Anxiety')
        specialty2 = Specialty(name='Depression')
        specialty3 = Specialty(name='ADHD')

        therapist1 = Therapist(
            name='John Opiyo', location='Kisumu', rating=4.8, total_ratings=20)
        therapist1.specialities.append(specialty1)

        therapist2 = Therapist(name='Jane Wanjiru',
                               location='Nakuru', rating=4.5, total_ratings=15)
        therapist2.specialities.append(specialty2)

        therapist3 = Therapist(
            name='Faith Kamau', location='Nairobi', rating=4.8, total_ratings=10)
        therapist3.specialities.append(specialty3)

        self.session.add_all([therapist1, therapist2, therapist3])
        self.session.commit()

    def get_all_therapists(self):
        return self.session.query(Therapist).all()

    def filter_therapists(self, filter_option, filter_value):
        return self.session.query(Therapist).filter(getattr(Therapist, filter_option).like(f'%{filter_value}%')).all()

    def review_therapist(self, therapist_id, rating):
        therapist = self.session.query(Therapist).filter(
            Therapist.id == therapist_id).first()
        if therapist:
            therapist.total_ratings += 1
            therapist.rating = (
                therapist.rating * (therapist.total_ratings - 1) + rating) / therapist.total_ratings
            self.session.commit()
            print("Thank you for your review!")
        else:
            print("Therapist not found.")

    def __del__(self):
        self.session.close()


# from sqlalchemy import create_engine
# from sqlalchemy import ForeignKey, Table, Column, Integer, String, Float
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///therapist.db')

# Base = declarative_base()

# therapist_speciality = Table(
#     'therapist_speciality',
#     Base.metadata,
#     Column('therapist_id', Integer, ForeignKey('therapists.id')),
#     Column('specialty_id', Integer, ForeignKey('specialties.id')),
#     extend_existing=True
# )


# class Therapist(Base):
#     __tablename__ = 'therapists'

#     id = Column(Integer(), primary_key=True)
#     name = Column(String())
#     location = Column(String())
#     rating = Column(Float())
#     total_ratings = Column(Integer())
#     specialities = relationship(
#         'Specialty', secondary=therapist_speciality, back_populates='therapists')

#     def __repr__(self):
#         return f'Therapist ID: {self.id}, ' + \
#             f'Name: {self.name}, ' + \
#             f'Location: {self.location}, ' + \
#             f'Rating: {self.rating}, ' + \
#             f'Total Ratings: {self.total_ratings})'


# class Specialty(Base):
#     __tablename__ = 'specialties'

#     id = Column(Integer(), primary_key=True)
#     name = Column(String())
#     therapists = relationship(
#         "Therapist", secondary=therapist_speciality, back_populates='specialities')

#     def __repr__(self):
#         return f'Specialty ID: {self.id}, ' + \
#             f' Name: {self.name})'
