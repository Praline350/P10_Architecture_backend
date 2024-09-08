from functools import wraps

def require_permission(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.authenticated_user.has_permission(permission_name):
                raise PermissionError(f"You do not have permission to {permission_name}.")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator