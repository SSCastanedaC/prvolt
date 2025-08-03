from django.urls import path
from leads.views import LeadsListView, LeadDetailView, LeadCreateView

app_name = "leads"

urlpatterns = [
    path("list", LeadsListView.as_view(), name="list"),
    path("list/<int:lead_id>", LeadDetailView.as_view(), name="detail"),
    path("create", LeadCreateView.as_view(), name="create"),
]
