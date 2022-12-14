from fastapi import FastAPI, Depends
from utils.utils import get_db
from schemas.game import GameplayInit
from rps_remote_simulator.database.models import Game as GameModel, User as UserModel
from rps_remote_simulator.game import Gameplay
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from datetime import datetime

game = FastAPI()


@game.post("/api/v1/game/play", tags=["games"])
async def create_game(
    choice: str, user_id: int, db: Session = Depends(get_db)
) -> GameModel | None:
    # you can handle the choice if it is correct
    # before you continue with the game schema
    # same goes with the user_id
    new_game = GameplayInit(
        user_id=user_id,
        game_result=Gameplay.play(play=choice),
        date_played=datetime.now(),
    )
    db_game = GameModel(**new_game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


@game.get("/api/v1/game/{user_id}/games", tags=["games"])
async def get_user_games(
    user_id: int, offset=0, limit=100, db: Session = Depends(get_db)
) -> List[GameModel] | None:
    # remember to check if the user is not deleted or a game is deleted
    db_user = db.get(UserModel, user_id)

    if db_user.is_deleted is True:
        # handle this exception well too
        raise Exception("User not found!")

    return db.scalars(
        select(GameModel)
        .where(GameModel.user_id == user_id)
        .offset(offset)
        .limit(limit)
    ).all()
