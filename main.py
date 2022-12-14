from http import HTTPStatus
from typing import Dict, Any
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from database.connection import async_session
from database.models import Question, FormType, User, Form, Answer

app = FastAPI()


class FormTypeRequest(BaseModel):
    description: str


class FormTypeAddQuestionRequest(BaseModel):
    title: str
    body: str
    required: bool


@app.post("/form_type/create")
async def form_create(r: FormTypeRequest):
    form_type = FormType(
        description=r.description
    )
    async with async_session() as session:
        session.add(form_type)
        await session.commit()
        await session.refresh(form_type)

    return form_type


@app.post("/form_type/add_question")
async def form_type_add_question(type_uuid: UUID, question: FormTypeAddQuestionRequest):
    async with async_session() as session:
        form_type: FormType = (await session.execute(
            select(FormType).where(FormType.uuid == type_uuid)
        )).scalar()

        if form_type is None:
            raise HTTPException(400)

        q = Question(
            title=question.title,
            description=question.body,
            required=question.required,
            form_type_id=form_type.id
        )
        session.add(q)
        await session.commit()
        await session.refresh(q)
        return q


@app.post("/create_user")
async def form_create(name: str):
    async with async_session() as session:
        user = User(username=name)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


@app.post("/create_form")
async def form_create(user_name: str):
    async with async_session() as session:
        user: User = (await session.execute(
            select(User).where(User.username == user_name)
        )).scalar()

        if user is None:
            raise HTTPException(400)

        f = Form(user_id=user.id, form_type_id=1)
        session.add(f)
        await session.commit()
        await session.refresh(f)
        return f


@app.post("/form/{form_uuid}/{question_uuid}/add_answer/", status_code=HTTPStatus.NO_CONTENT)
async def form_add_question(form_uuid: UUID, question_uuid: UUID, answer: Dict[str, Any]):
    async with async_session() as session:
        form: Form = (await session.execute(
            select(Form).where(Form.uuid == form_uuid)
        )).scalar()

        if form is None:
            raise HTTPException(400)

        q: Question = (await session.execute(
            select(Question).where(Question.uuid == question_uuid)
        )).scalar()

        if q is None:
            raise HTTPException(400)

        a = Answer(
            form_id=form.id,
            form_question_id=q.id,
            answer_object=answer
        )
        session.add(a)
        await session.commit()


@app.get("/form/{form_uuid}")
async def form_get(form_uuid: UUID):
    async with async_session() as session:
        form: Form = (await session.execute(
            select(Form).where(Form.uuid == form_uuid)
        )).scalar()

        if form is None:
            raise HTTPException(400)

        return form
