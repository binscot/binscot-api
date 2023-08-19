from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette.templating import Jinja2Templates

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="resource/templates")
