import time

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from user.models import User
from user.constants import two_days_in_seconds
from website.settings import JWT_SECRET, JWT_ALGORITHM


class Auth:
    def authenticate(self, body: dict):
        """Authenticate a user.

        :body: request['POST']
        :returns: None if user not found, False if incorrect password,
        (pk, email) if correct
        """

        user = User.objects.filter(email=body['email'])
        if len(user) == 1:
            try:
                PasswordHasher().verify(user[0].password, body['password'])
            except VerificationError:
                return False
            return (user[0].pk, user[0].email)

    def authorize(self, request, uid: int, email: str):
        """Authorize a user in 15 days."""
        request.session.set_expiry(1296000)
        request.session['token'] = jwt.encode(
            {'uid': uid, 'email': email,
             'exp': time.time() + two_days_in_seconds},
            JWT_SECRET, JWT_ALGORITHM
        )

    def decode_token(self, token: str):
        """Method decode token and return payload, if token is not expired."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        return payload
