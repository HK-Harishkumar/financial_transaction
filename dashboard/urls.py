from django.urls import path

from dashboard import views
app_name = 'dashboard'

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('download_vendor_analysis',views.download_vendor_analysis_excel,name='download_vendor_analysis'),
]
