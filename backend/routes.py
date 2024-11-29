from fastapi import APIRouter
from message import get_messages

test_router = APIRouter(prefix='/message')


@test_router.get('/')
def get_message():
    return get_messages()

