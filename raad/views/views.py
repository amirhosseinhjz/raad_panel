from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from raad.models import Company, Device, MessengerAdmin
from raad.forms import MessengerAdminForm, DeviceUpdateForm
from django.views.generic.edit import UpdateView, FormView
from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import UserPassesTestMixin


@login_required
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('raad:login')
    companies = request.user.companies.all()
    devices = Device.objects.filter(company__user=request.user)
    messenger_admins = MessengerAdmin.objects.filter(company__user=request.user)

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'user': request.user,
            'companies': companies,
            'devices': devices,
            'messenger_admins': messenger_admins,
        }
    )


def add_messenger_admin(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    if not company.user == request.user:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = MessengerAdminForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.company = company
            admin.save()
            return redirect('raad:dashboard')
    else:
        form = MessengerAdminForm()

    return render(request, 'dashboard/add_messenger_admin.html', {'form': form, 'company': company})


class MessengerAdminUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        messenger_admin = self.get_object()
        return self.request.user == messenger_admin.company.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_id'] = self.get_object().id
        return context

    model = MessengerAdmin
    fields = ['id', 'messenger', 'admin_messenger_id']
    template_name = 'dashboard/update_messenger_admin.html'


def delete_messenger_admin(request, admin_id):
    admin = get_object_or_404(MessengerAdmin, pk=admin_id)
    print(admin)
    if not (request.user.is_authenticated or admin.company.user == request.user):
        return HttpResponseNotFound()
    admin.delete()
    return redirect('raad:dashboard')


class DeviceUpdateView(UserPassesTestMixin, FormView):
    form_class = DeviceUpdateForm
    template_name = 'dashboard/device.html'
    success_url = '/dashboard/'

    def test_func(self):
        device = self.get_object()
        return self.request.user == device.company.user

    def get_object(self):
        device_id = self.kwargs['pk']
        return get_object_or_404(Device, pk=device_id)

    def get_form_kwargs(self):
        device = Device.objects.get(pk=self.kwargs['pk'])
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'name': device.name}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = self.get_object().company.name
        return context

    def form_valid(self, form):
        device = self.get_object()
        device.name = form.cleaned_data['name']
        device.save()
        return super().form_valid(form)
