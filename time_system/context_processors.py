
from settings import SESSION_TIMEOUT


def timeout(request):
    return {"SESSION_TIMEOUT": SESSION_TIMEOUT}
