from django.urls import path
from . import views


urlpatterns = [
    path('account-activate/<uidb64>/<token>', views.activate_user, name='account-activate'),
]
