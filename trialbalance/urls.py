from django.urls import path

from trialbalance import views
app_name = 'trialbalance'

urlpatterns = [
    path('trailbalance_temp', views.trailbalance_temp, name='trailbalance_temp'),
    path('generate_trial_balance', views.generate_trial_balance, name='generate_trial_balance'),
    path('trialbalance_summary', views.trialbalance_summary, name='trialbalance_summary')

]
