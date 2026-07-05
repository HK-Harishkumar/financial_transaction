from django.urls import path

from transactions import views
app_name = 'transactions'

urlpatterns = [
    path('hello',views.hello,name='hello'),
    path('transaction', views.transaction, name='transaction'),
    path('upload_transaction', views.upload_transaction, name='upload_transaction'),
    path('transaction_summary', views.transaction_summary, name='transaction_summary'),
]
