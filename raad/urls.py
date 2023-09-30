from django.urls import path
from raad.views.authorization_views import LoginView, RegisterView, logout_view
from raad.views.views import (
    dashboard_view, add_messenger_admin, MessengerAdminUpdateView,
    delete_messenger_admin, DeviceUpdateView)

app_name = 'raad'

urlpatterns = [
    # path('', LoginView.as_view(), name='home'), # TODO: remove this
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('company/<int:company_id>/add_messenger_admin/', add_messenger_admin, name='add_messenger_admin'),
    path('edit_messenger_admin/<int:pk>/', MessengerAdminUpdateView.as_view(), name='edit_messenger_admin'),
    path('delete_messenger_admin/<int:admin_id>/', delete_messenger_admin, name='delete_messenger_admin'),
    path('device/<int:pk>/', DeviceUpdateView.as_view(), name='device_update'),
]
