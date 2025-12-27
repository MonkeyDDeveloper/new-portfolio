from decouple import config
from database.utils.password import get_password_hash

admin_password = config("ADMIN_PASSWORD")

password_hash = get_password_hash(admin_password)

print(password_hash)