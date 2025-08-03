from django.shortcuts import render, redirect
from django.views import View
from leads.helpers.services import LeadsHandler, CountriesHandler
from django.contrib import messages

# Create your views here.


class LeadsListView(View):
    template_name = "leads_list.html"

    def get(self, request):
        success, request_data = LeadsHandler.get_all()
        context = {}
        if success:
            context["leads"] = request_data["data"]["leads"]
        return render(request, self.template_name, context)


class LeadDetailView(View):
    template_name = "leads_detail.html"

    def get(self, request, lead_id):
        success, request_data = LeadsHandler.get_by_id(lead_id=lead_id)
        context = {}
        if success:
            context["lead"] = request_data["data"]
        return render(request, self.template_name, context)

    def post(self, request, lead_id):
        success, request_data = LeadsHandler.delete(lead_id=lead_id)
        if success:
            messages.success(request, "Lead deleted")
        else:
            messages.error(request, "Error")
        return redirect("leads:list")


class LeadCreateView(View):
    template_name = "leads_create.html"

    def get(self, request):
        countries = CountriesHandler.get_countries()
        context = {"countries": countries}
        return render(request, self.template_name, context)

    def post(self, request):
        body = {
            "email": request.POST["email"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "country_code": request.POST["country_code"],
        }
        success, request_data = LeadsHandler.create(body=body)
        if success:
            messages.success(request, "Lead created successfully")
        else:
            messages.error(request, "Error")
        return redirect("leads:list")
