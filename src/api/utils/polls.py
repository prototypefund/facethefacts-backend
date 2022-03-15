from typing import List

from src.api.schemas import BundestagPollData
import src.api.crud as crud
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.db import models


def get_politcianIds_by_BundestagPollData_and_followIds(
    polls: List[BundestagPollData], followIds: List[int], db: Session
):
    current_legislature_period = 132
    for poll in polls:
        politician_list = []
        query_data = (
            db.query(models.CandidacyMandate)
            .join(models.Vote)
            .filter(
                and_(
                    models.CandidacyMandate.politician_id.in_(followIds),
                    models.CandidacyMandate.parliament_period_id
                    == current_legislature_period,
                    models.Vote.poll_id == poll["poll_id"],
                    models.Vote.vote != "no_show",
                )
            )
            .all()
        )
        if query_data:
            [politician_list.append(item.politician_id) for item in query_data]
        if len(politician_list) < 5:
            random_query_data = (
                db.query(models.CandidacyMandate)
                .join(models.Vote)
                .filter(
                    and_(
                        models.CandidacyMandate.parliament_period_id
                        == current_legislature_period,
                        models.Vote.poll_id == poll["poll_id"],
                        models.Vote.vote != "no_show",
                    )
                )
                .order_by(func.random())
                .limit(5 - len(politician_list))
                .all()
            )
            [
                politician_list.insert(0, item.politician_id)
                for item in random_query_data
            ]
        poll["politicians"] = politician_list
        poll["last_politician"] = crud.get_entity_by_id(
            db, models.Politician, poll["politicians"][-1]
        ).label
        # get with politician_id candidacymandate_id where legislature_period is Bundestag_id
    return polls
