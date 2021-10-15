from django import template
from library.models import Notification,LibraryMember

register = template.Library()


@register.inclusion_tag('library/show_notifications.html', takes_context=True)
def show_notifications(context):
    # Get current user information
    request_user = context['request'].user
    # Filter through all notification objects to find the matched user id and filter out the notifcation that users already seen, and order the notifications by date.
    member=LibraryMember.objects.get(user=request_user)
    notifications = Notification.objects.filter(
        to_member=member).exclude(user_has_seen=True).order_by('-date')
    return {'notifications': notifications}
