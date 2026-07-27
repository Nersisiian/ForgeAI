import factory
from app.db.models.user import User
from app.core.security import get_password_hash


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    hashed_password = factory.LazyFunction(lambda: get_password_hash("testpass"))
    full_name = factory.Faker("name")
    is_active = True
    is_superuser = False
