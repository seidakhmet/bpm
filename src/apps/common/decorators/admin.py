from django.template.response import TemplateResponse


def require_confirmation(action: str):
    def _require_confirmation(func):
        def wrapper(modeladmin, request, queryset):
            if request.POST.get("confirmation") is None:
                request.current_app = modeladmin.admin_site.name
                context = {
                    "action": action,
                }
                return TemplateResponse(request, "admin/action_confirmation.html", context)

            return func(modeladmin, request, queryset)

        wrapper.__name__ = func.__name__
        return wrapper

    return _require_confirmation
