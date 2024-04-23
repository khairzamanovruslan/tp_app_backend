from pydantic import BaseModel


class SUsersTG(BaseModel):
    full_name: str
    access_bot: bool = True


class SUsersTg_FullData(SUsersTG):
    id_tg: str