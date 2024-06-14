from django.contrib import admin
from django.core.cache import cache
from django.core.paginator import Paginator

from communications.models import PrivateChatRoom, PrivateRoomChatMessage

admin.site.register(PrivateChatRoom)
admin.site.register(PrivateRoomChatMessage)

