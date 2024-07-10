from django.contrib.auth.models import Group

def group_name_processor(request):
    if request.user.is_authenticated:
        group_id = request.session.get('group')
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                return {'group_name': group.name}
            except Group.DoesNotExist:
                return {'group_name': None}
    return {'group_name': None}