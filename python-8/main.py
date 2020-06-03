import jwt, logging

logging.basicConfig(level=logging.DEBUG)

# https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
# https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html#token-storage-on-client-side
def create_token(data, secret):
    return jwt.encode(data, secret, algorithm='HS256')


def verify_signature(token, secret="acelera"):
    try:
        signature = jwt.decode(token, secret, algorithms='HS256')
        return signature
    except jwt.InvalidSignatureError as ex:
        logging.error(ex)
        return {"error": 2}
    except jwt.InvalidTokenError as ex:
        logging.error(ex)
        return {"error": 2}
    except Exception as ex:
        logging.error(ex)
        raise ex
