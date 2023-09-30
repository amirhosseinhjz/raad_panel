from django.urls import path
from ticket.views import UserTicketListView, ticket_detail, new_ticket

app_name = 'ticket'

urlpatterns = [
    path('', UserTicketListView.as_view(), name='tickets'),
    path('<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('new/', new_ticket, name='new_ticket'),
]
