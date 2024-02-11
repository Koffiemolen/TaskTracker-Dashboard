"""This module contains the database router for the FastAPI application."""
from typing import Optional
from decimal import Decimal
from sqlalchemy import Column, String, Integer, DECIMAL, Text
from sqlmodel import Field, SQLModel


class WorkflowLinkConstruct(SQLModel, table=True):
    """
    This class models the database table workflowlinkconstructs.

    Attributes:
    ID (str): The primary key.
    WorkflowID (str): The ID of the workflow.
    SourceID (Optional[str]): The source ID. Can be null.
    DestinationID (Optional[str]): The destination ID. Can be null.
    LinkType (Optional[int]): The link type. Can be null.
    ResultType (Optional[int]): The result type. Can be null.
    Value (Optional[str]): The value. Can be null.
    SourceHorizontalPosition (Optional[Decimal]): The source's horizontal position. Can be null.
    SourceVerticalPosition (Optional[Decimal]): The source's vertical position. Can be null.
    DestinationHorizontalPosition (Optional[Decimal]): The destination's horizontal position. Can be null.  # pylint: disable=line-too-long
    DestinationVerticalPosition (Optional[Decimal]): The destination's vertical position. Can be null.  # pylint: disable=line-too-long
    """
    __tablename__ = "workflowlinkconstructs"
    ID: str = Field(sa_column=Column("ID", String(38), primary_key=True))
    WorkflowID: str = Field(default=None, sa_column=Column("WorkflowID", String(38), nullable=False))  # pylint: disable=line-too-long
    SourceID: Optional[str] = Field(default=None, sa_column=Column("SourceID", String(38)))
    DestinationID: Optional[str] = Field(default=None, sa_column=Column("DestinationID", String(38)))  # pylint: disable=line-too-long
    LinkType: Optional[int] = Field(default=None, sa_column=Column("LinkType", Integer))
    ResultType: Optional[int] = Field(default=None, sa_column=Column("ResultType", Integer))  # pylint: disable=line-too-long
    Value: Optional[str] = Field(default=None, sa_column=Column("Value", Text))
    SourceHorizontalPosition: Optional[Decimal] = Field(default=None, sa_column=Column("SourceHorizontalPosition", DECIMAL(18, 0)))  # pylint: disable=line-too-long
    SourceVerticalPosition: Optional[Decimal] = Field(default=None, sa_column=Column("SourceVerticalPosition", DECIMAL(18, 0)))  # pylint: disable=line-too-long
    DestinationHorizontalPosition: Optional[Decimal] = Field(default=None, sa_column=Column("DestinationHorizontalPosition", DECIMAL(18, 0)))  # pylint: disable=line-too-long
    DestinationVerticalPosition: Optional[Decimal] = Field(default=None, sa_column=Column("DestinationVerticalPosition", DECIMAL(18, 0)))  # pylint: disable=line-too-long
