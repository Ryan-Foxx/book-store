from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegisterRateThrottle(AnonRateThrottle):
    scope = "register"


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class ActivationRateThrottle(AnonRateThrottle):
    scope = "activation"


class ResendActivationRateThrottle(AnonRateThrottle):
    scope = "resend_activation"


class ResetPasswordRateThrottle(AnonRateThrottle):
    scope = "reset_password"


class ResetUsernameRateThrottle(AnonRateThrottle):
    scope = "reset_username"


class ResetPasswordConfirmRateThrottle(AnonRateThrottle):
    scope = "reset_password_confirm"


class SetPasswordRateThrottle(UserRateThrottle):
    scope = "set_password"


class SetUsernameRateThrottle(UserRateThrottle):
    scope = "set_username"


# For DEFAULT_THROTTLE_RATES => in config/settings.py
# Apply ONLY to authenticated users. Anonymous users are ignored.
class StrictUserRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None
        return super().get_cache_key(request, view)
