from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    deadline = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="goal")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    deadline = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    goal = relationship("Goal", back_populates="tasks")

engine = create_engine('sqlite:///database/database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
