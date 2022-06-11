from datetime import date
from pydantic import BaseModel, root_validator


class BaseModelWithDatesFiled(BaseModel):
    since: date = ...
    until: date | None = None

    @root_validator
    def validate_dates(cls, values):
        """If until isn't after since or since is None raise ValidationError"""
        since, until = values.get("since"), values.get("until")

        if until is not None:
            if since is None:
                raise ValueError("Until date can't be without since")
            if since > until:
                raise ValueError("Since date can't be after until date")

        return values
