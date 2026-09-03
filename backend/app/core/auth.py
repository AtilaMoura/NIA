from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido.")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
