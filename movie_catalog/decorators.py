from django.core.exceptions import PermissionDenied

from movie_catalog.models import Comment


def is_user_author(edit_obj_func):
    def inner(request, **kwargs):
        try:
            Comment.objects.get(user=request.user, id=request.POST['comment_id'])
        except Comment.DoesNotExist:
            raise PermissionDenied
        return edit_obj_func(request, **kwargs)
    return inner

