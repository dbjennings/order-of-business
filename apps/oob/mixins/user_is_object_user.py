from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

class UserIsObjectUserMixIn(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user