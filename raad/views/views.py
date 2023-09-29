from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from raad.models import Company, Device, MessengerAdmin
from raad.forms import MessengerAdminForm, DeviceNameUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import UpdateView, FormView
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView



@login_required
def dashboard_view(request):
    companies = Company.objects.filter(client=request.user)
    devices = Device.objects.filter(company__client=request.user)
    messenger_admins = MessengerAdmin.objects.filter(company__client=request.user)

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

def user_can_add_messenger_admin(user, pk):
    company = get_object_or_404(Company, pk=pk)


def add_messenger_admin(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    if not (request.user.is_authenticated or company.user == request.user):
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


def user_can_update_messenger_admin(user, pk):
    messenger_admin = get_object_or_404(MessengerAdmin, pk=pk)
    return user.is_authenticated and user == messenger_admin.company.user


# @user_passes_test(user_can_update_messenger_admin)
class MessengerAdminUpdateView(UpdateView):
    model = MessengerAdmin
    fields = ['messenger', 'admin_messenger_id']
    template_name = 'dashboard/update_messenger_admin.html'


# @method_decorator(login_required, name='dispatch')
class MessengerAdminDeleteView(DeleteView):
    model = MessengerAdmin
    template_name = 'dashboard/delete_messenger_admin.html'
    success_url = reverse_lazy('raad:dashboard')



class DeviceNameUpdateView(FormView):
    form_class = DeviceNameUpdateForm
    template_name = 'dashboard/device.html'  # Create this template
    success_url = '/dashboard/'

    def get_object(self):
        # Retrieve the Device instance you want to update based on its ID or other criteria
        device_id = self.kwargs['pk']  # Assuming 'pk' is the device's primary key in the URL
        return get_object_or_404(Device, pk=device_id)

    def get_form_kwargs(self):
        # Get the current device instance and set its name as the initial value for the form
        device = Device.objects.get(pk=self.kwargs['pk'])  # Assuming 'pk' is the device's primary key in the URL
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'name': device.name, 'license_key': device.license_key}
        return kwargs

    def form_valid(self, form):
        # Save the updated 'name' field to the Device instance
        device = self.get_object()
        device.name = form.cleaned_data['name']
        device.save()
        return super().form_valid(form)
