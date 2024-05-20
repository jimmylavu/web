from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from . import views
from .views import PlanListView

urlpatterns = [
    path('', TemplateView.as_view(template_name='blog/index.html')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account_logout/', views.login, name='login'),
    path('reports/', views.reports, name='reports'),
    path('planlist/', views.planlist, name='planlist'),
    path('planlist/update/<int:id>', views.update, name='planlist'),
    path('plan/delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('planlist/update/update/<int:plan_id>', views.update_plan, name = 'update_plan'),
    path('plans/', views.plan, name='plan'),
    path('plans/reservation/<int:id>',  PlanListView.as_view(), name='plan_reserv'),
    path('plans/reservation/payment/<int:id>', views.payment, name='payment'),
    path('plans/reservation/payment/planresev/<int:id>', views.planresev, name='planresev'),
    path('plans/reservation/payment/planresev/settlement/<int:id>', views.settlement, name='settlement'),
    path('plans/reservation/payment/planresev/settlement/paypal/<int:id>', views.display_payment, name='display_payment'),
    path('todos1/<int:id>/', views.todos1, name='todos1'),
    path('upload/', views.upload_image, name = 'upload_image'),
    path('users/', views.users, name = 'users'),
    path('reservationlist/', views.reservationlist, name = 'reservationlist'),
    path('history/', views.userresdips, name = 'userresdips'),
    path('paymenthistory/', views.paymenthistory, name = 'paymenthistory'),
    path('paymenthistory/userpaymenthistory/<int:id>', views.userpaymenthistory, name = 'userpaymenthistory'),
    path('transactions/', views.displaydate, name='transactions_by_date'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('saction/', views.transactionlist, name='transactionlist'),
    path('reminder/', views.payment_reminder_view, name='payment_reminder_view'),
    path('profile/', views.account, name='account'),
    path('updateaccount/<int:id>', views.update_account, name='update_account'),
]   