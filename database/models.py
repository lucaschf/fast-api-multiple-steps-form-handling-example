import uuid as uuid

from sqlalchemy import Column, Integer, String, ForeignKey, false, JSON, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Model(Base):
    """Base que contém os campos base de qualquer tabela."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    uuid = Column(
        postgresql.UUID(as_uuid=True),
        nullable=False,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )


class User(Model):
    __tablename__ = "user"

    username: str = Column(String, nullable=false)


class FormType(Model):
    __tablename__ = "form_type"

    description: str = Column(String, nullable=false, unique=True, index=True)


class Form(Model):
    __tablename__ = "form"

    user_id: int = Column(Integer, ForeignKey(User.id), nullable=False)
    form_type_id = Column(Integer, ForeignKey("form_type.id"), nullable=False)
    answers = relationship("Answer", back_populates="form", lazy="selectin")


class Question(Model):

    __tablename__ = "form_question"

    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    required: bool = Column(Boolean, nullable=False, default=True)

    form_type_id: int = Column(Integer, ForeignKey("form_type.id"), nullable=False)


class Answer(Model):
    __tablename__ = "form_answer"

    form_question_id: int = Column(Integer, ForeignKey(Question.id), nullable=False)
    form_id: int = Column(Integer, ForeignKey(Form.id), nullable=False)
    form = relationship(Form, back_populates="answers", lazy="selectin")
    answer_object = Column(JSON, default=None)
