from jpl import errors

def authenticate_request(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        try:
            r = None
            super(args[0].__class__, args[0]).perform_authentication(args[1])
            r = args[1].user
            if r is not None:
                pass
            else:
                raise Exception(errors.USER_ACCESS_DENY)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)
        return fn(r, *args, **kwargs)
    return decorated

def is_js(fn):
    def decorated(u, *args, **kwargs):
        try:
            if not u.groups.filter(name='JobSeekers').exists():
                raise Exception(errors.USER_ACCESS_DENY)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)
        return fn(*args, **kwargs)
    return decorated

def is_es(fn):
    def decorated(u, *args, **kwargs):
        try:
            if not u.groups.filter(name='Employers').exists():
                raise Exception(errors.USER_ACCESS_DENY)
        except Exception as e:
            raise errors.JPLException(e.__str__(), 500)
        return fn(*args, **kwargs)
    return decorated