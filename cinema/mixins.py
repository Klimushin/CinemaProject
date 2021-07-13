from django.core.exceptions import PermissionDenied


class AdminRequiredMixin:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        # noinspection PyUnresolvedReferences
        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )