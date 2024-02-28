from semantic_search_app import create_app
from semantic_search_app.defaultsettings import config
import string
import secrets
import fire

secret = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(9))
#secret = 'ys060p4PT'
# test_config.update(
#     SESSION_COOKIE_HTTPONLY=True,
#     REMEMBER_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE="Strict",
#     DEBUG=True)
port = 9003
secret = 'abc'
def debug():
    test_config = config['development']
    test_config.SECRET_KEY = secret
    flask_app = create_app(test_config)
    flask_app.run(port=port)

def dev():
    test_config = config['production']
    test_config.SECRET_KEY = secret
    flask_app = create_app(test_config)
    flask_app.run(port=port)

if __name__ == '__main__':
    fire.Fire()
