from fastapi import FastAPI
from sqladmin import Admin
import uvicorn
from app.admin.views import SubstationAdmin, UsersAdmin, UsersTGAdmin
from app.users_tg.router import router as router_users_tg
from app.users.router import router as router_users
from app.substation.router import router as router_substation
from app.database import engine
from app.admin.auth import authentication_backend

app = FastAPI()

app.include_router(router_users)
app.include_router(router_substation)
app.include_router(router_users_tg)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(UsersTGAdmin)
admin.add_view(SubstationAdmin)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=9999, reload=True)
