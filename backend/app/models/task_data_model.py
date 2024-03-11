#
# """
# Task Data Model
# """
#
# from sqlalchemy import Column, Integer, String, Boolean
# from .base_model import Base  # pylint: disable=relative-beyond-top-level
#
#
# class TaskData(Base):  # pylint: disable=too-few-public-methods
#     """
#     This is the Task class involving different details about a task.
#     """
#     __tablename__ = 'tasks'
#     TriggerID = Column(String(38), primary_key=True)
#     id = Column(Integer, primary_key=True)
#     resourceID = Column(String(50), nullable=False)
#     resource_name = Column(String(150), nullable=False)
#     parentID = Column(String(50), nullable=False)
#     completion_state = Column(Boolean, default=False)
#     enabled = Column(Boolean, default=False)
#     deleted = Column(Boolean, default=False)
