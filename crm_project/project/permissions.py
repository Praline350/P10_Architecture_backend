from functools import wraps


def require_permission(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.authenticated_user.has_permission(permission_name):
                raise PermissionError(
                    f"You do not have permission to {permission_name}."
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def is_authenticated_user(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.authenticated_user:  # Vérifie si l'utilisateur est authentifié
            print("is authenticated user permission")
            raise PermissionError("You do not have permission")

        return func(self, *args, **kwargs)

    return wrapper


def view_authenticated_user(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.controller.authenticated_user:
            print("view permission")
            raise PermissionError("You do not have permission")

        print(f" AUTH :: {self.controller.authenticated_user.first_name}")
        return func(self, *args, **kwargs)

    return wrapper


def decorate_all_methods(decorator):
    """Applique un décorateur à toutes les méthodes d'une classe."""

    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, decorator(attr_value))
        return cls

    return class_decorator
