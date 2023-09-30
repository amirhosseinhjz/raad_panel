from django.views.generic import ListView
from ticket.models import Ticket, TicketReply
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ticket.forms import TicketForm, TicketReplyForm


class UserTicketListView(ListView):
    model = Ticket
    template_name = 'ticket/tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user).order_by('-created_at')


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    replies = ticket.replies.all().order_by('created_at')

    if request.method == 'POST':
        form = TicketReplyForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            reply = TicketReply.objects.create(ticket=ticket, created_by=request.user, message=message)
            reply.save()
            return redirect('ticket:ticket_detail', ticket_id=ticket.id)

    else:
        form = TicketReplyForm()

    return render(request, 'ticket/detail.html', {'ticket': ticket, 'replies': replies, 'form': form})


def new_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'تیکت با موفقیت ایجاد شد.')
            return redirect('ticket:tickets')
        else:
            messages.error(request, 'لطفاً اطلاعات معتبر وارد کنید.')
    else:
        form = TicketForm()

    return render(request, 'ticket/new_ticket.html', {'form': form})
