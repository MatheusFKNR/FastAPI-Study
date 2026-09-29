from models import db
from sqlalchemy.orm import sessionmaker

def catch_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session 
        # Yeild funciona parecido a um return, mas ele permite 
        # que a função seja pausada e retomada posteriormente. 
        # Isso é útil para criar geradores ou corrotinas.

        # Yeild works similarly to a return, but it allows
        # that the function to be a paused and resumed later.
        # that is useful for creating generators or coroutines.
    finally:
        session.close()
        # o try executa o código que pode dar erro, 
        # e o finally roda sempre depois dele, com erro ou sem erro.

        # The try executer the code than can give error,
        # and the finally runs always after it, with error or without error.