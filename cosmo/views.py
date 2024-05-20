from django.shortcuts import render
import requests
from .models import *
from django.shortcuts import render, HttpResponse,HttpResponseRedirect, reverse, get_object_or_404
from django.http import HttpResponseBadRequest, HttpRequest
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect #new
from .forms import * #new
from django.contrib.auth.decorators import login_required
from django.views import View
from decimal import Decimal
from django.db.models import Sum, Count
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
from .models import Booking, PaymentReminder
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.dispatch import receiver
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from decimal import Decimal
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.contrib import messages
from paypal.standard.models import ST_PP_COMPLETED
from .models import Booking
from .paypal_utils import get_transaction_details
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.

def login(requests):
  template = loader.get_template('account/login.html')
  return HttpResponse(template.render())

def plan(request):
    plan = Plan.objects.all().order_by('-id')
    template = loader.get_template('blog/plan.html')
    context = {
        'plan' : plan,
    }
    return HttpResponse(template.render(context, request))

def planlist(request):
    plan = Plan.objects.all().order_by('-id')
    template = loader.get_template('blog/planslist.html')
    context = {
        'plan' : plan,
    }
    return HttpResponse(template.render(context, request))

def reserva(request,id):
    reservation = Plan.objects.get(id=id)
    template = loader.get_template('blog/reservation.html')
    context = {
        'plan' : reservation,
    }
    return HttpResponse(template.render(context, request))

def upload_image(request): #new
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect(planlist)
    else:
        form = PlanForm()
        context = {
            'form': form
        }
    return render(request, 'upload.html', context)

def update(request, id):
  plan = Plan.objects.get(id=id)
  template = loader.get_template('blog/planslist.html')
  context = {
    'plan' : plan,
  }
  return HttpResponse(template.render(context, request))

def update_plan(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)

    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES, instance=plan)

        if form.is_valid():
            form.save()
            return redirect('planlist')
    else:
        form = PlanForm(instance=plan)

    return render(request, 'updateplan.html', {'form': form, 'plan': plan})

@login_required
def payment(request, id):
    plan = Plan.objects.get(id=id)
    template = loader.get_template('blog/paymentform.html')
    context = {
    'plan' : plan,
    }
    return HttpResponse(template.render(context, request))
 

def reservationlist(request):
  booking = Booking.objects.all().order_by('-id')
  template = loader.get_template('blog/reservationlist.html')
  context = {
    'booking' : booking,
  }
  return HttpResponse(template.render(context, request))

def settlement(request, id):
    booking = get_object_or_404(Booking, id=id)

    plan = booking.plan
    plan_name = plan.name
    plan_price = plan.price

    booking_mop = booking.mop
    total_years = 5

    total_price = plan_price * total_years

    if booking_mop == 'annually':
        total_price = plan_price / total_years
    elif booking_mop == 'semi-annually':
        total_price = plan_price / (total_years * 2)  
    elif booking_mop == 'quarterly':
        total_price = plan_price / (total_years * 4) 
    elif booking_mop == 'monthly':
        total_price = plan_price / (total_years * 12) 
    else:
        total_price = plan_price  

    
    context = {
    'booking': booking,
    'plan_name': plan_name,
    'plan_price': plan_price,
    'booking_mop': booking_mop,
    'total_price': total_price,
}

    
    return render(request, 'blog/settlement.html', context)

    
def least(request):
  booking = Booking.objects.all()
  template = loader.get_template('blog/bookinghistory.html')
  context = {
    'booking' : booking,
  }
  return HttpResponse(template.render(context, request))

def userresdips(request):
    booking = Booking.objects.filter(user=request.user).order_by('-id')
    template = loader.get_template('blog/bookinghistory.html')
    context = {
    'booking' : booking,
  }
    return HttpResponse(template.render(context, request))

class PlanListView(View):
    template_name = 'blog/reservation.html'

    def get(self, request, id=None):
        if id is not None:
            plan = get_object_or_404(Plan, pk=id)
            total_price = self.calculate_total_price(plan)

            if not total_price:
                return render(request, 'error.html', {'message': 'Plan detaix   ls not found.'})

            return render(request, 'blog/reservation.html', total_price)

        plan = Plan.objects.all()
        return render(request, self.template_name, {'plan': plan})

    def calculate_total_price(self, plan):
        plan_price = plan.price  
        total_years = 5  

       
        total_price = plan_price * total_years

        
        annually = plan_price / total_years  
        semi_annually = plan_price / (total_years * 2)  
        quarterly = plan_price / (total_years * 4)  
        monthly = plan_price / (total_years * 12)  
        
        annually = round(annually, 2)
        semi_annually = round(semi_annually, 2)
        quarterly = round(quarterly, 2)
        monthly = round(monthly, 2)
        return {
            'plan': plan,
            'total_price': total_price,
            'annually': annually,
            'semi_annually': semi_annually, 
            'quarterly': quarterly,
            'monthly': monthly,
        }
    
class Boking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    mop = models.CharField(max_length=255, null=True)
    phone = models.IntegerField()

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    @property
    def total_price(self):
        # Calculate total price based on plan and mode of payment
        if self.mop == 'annually':
            return self.plan.price  # Total price for one year
        elif self.mop == 'semi_annually':
            return self.plan.price / 2  # Total price for six months
        elif self.mop == 'quarterly':
            return self.plan.price / 4  # Total price for three months
        elif self.mop == 'monthly':
            return self.plan.price / 12  # Total price for one month
        else:
            return self.plan.price  # Default to annual price if mode is unspecified

    def __str__(self):
        return f"{self.user.username} - {self.plan}"
    
def reports(request):
    total_reservations = Booking.objects.count()
    total_sale = Transaction.objects.aggregate(total_sale=Sum('amount'))['total_sale'] or 0
    total_users = Booking.objects.values('user_id').distinct().count()

    bookings = Booking.objects.all().order_by('-id')
    transactions = Transaction.objects.all().order_by('-id')

    return render(request, 'blog/reports.html', {
        'bookings': bookings,
        'transactions': transactions,
        'total_reservations': total_reservations,
        'total_sale': total_sale,
        'total_users': total_users
    })

def paymenthistory(request):
    bookings = Booking.objects.filter(user=request.user)
    transaction = Transaction.objects.filter(booking__in=bookings).order_by('-id')

    template = 'blog/userpaylist.html'
    context = {'transaction': transaction}
    return render(request, template, context)

def userpaymenthistory(request, id):
    # Retrieve the transaction and payment reminder objects
    transaction = get_object_or_404(Transaction, id=id)

    # Retrieve booking information for the payment
    booking = transaction.booking
    payment_frequency = booking.mop  # Mode of payment (e.g., 'monthly', 'quarterly', 'semi_annually', 'annually')
    start_date = transaction.date  # Start date of the plan
    
    # Calculate the next payment date based on payment frequency
    if payment_frequency == 'monthly':
        next_payment_date = start_date + timedelta(days=30)
    elif payment_frequency == 'quarterly':
        next_payment_date = start_date + timedelta(days=91)  # 3 months (quarterly)
    elif payment_frequency == 'semi_annually':
        next_payment_date = start_date + timedelta(days=182)  # 6 months (semi-annually)
    elif payment_frequency == 'annually':
        next_payment_date = start_date + timedelta(days=365)  # 1 year (annually)
    else:
        next_payment_date = None  # Default to no next payment date if payment frequency is undefined

    # Pass both objects to the template
    context = {
        'transaction': transaction,
        'next_payment_date': next_payment_date,
    }

    return render(request, 'blog/userpayment.html', context)

def displaydate(request):
    selected_date = request.GET.get('selected_date')
    transactions = []

    if selected_date:
        try:
            date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            transactions = Transaction.objects.filter(date__date=date)
        except ValueError:
            selected_date = None  # Reset if date format is incorrect

    return render(request, 'blog/transaction.html', {
        'selected_date': selected_date,
        'transactions': transactions
    })

def generate_pdf(request):
    selected_date = request.GET.get('selected_date')
    transactions = Transaction.objects.filter(date__date=selected_date) if selected_date else []

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transactions_{selected_date}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    style_heading = styles['Heading1']
    style_body = styles['BodyText']

    # Add heading to the PDF
    elements.append(Paragraph(f'Transactions for {selected_date}', style_heading))
    elements.append(Paragraph('', style_body))  # Add empty paragraph for spacing

    # Add table of transactions
    if transactions:
        data = [['Transaction ID', 'User', 'Amount', 'Date']]
        for transaction in transactions:
            data.append([
                str(transaction.id), 
                str(transaction.booking.user.username), 
                f"{transaction.amount:.2f}", 
                str(transaction.date)
            ])

        table = Table(data)

        # Define table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),        # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Center-align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),    # Header row font style
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),     # Body row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black)          # Border grid color and width
        ])

        # Apply table style
        table.setStyle(table_style)

        # Add table to PDF elements
        elements.append(table)
    else:
        elements.append(Paragraph('No transactions found for the selected date.', style_body))

    # Build the PDF document
    doc.build(elements)
    return response

 
def users(request):
  user = User.objects.all().order_by('-id')
  template = loader.get_template('blog/users.html')
  context = {
    'user' : user,
  }
  return HttpResponse(template.render(context, request))

@login_required
def planresev(request, id):
    if request.method == 'POST':
        user_id = request.user.id
        plan = get_object_or_404(Plan, id=id)

        phone = request.POST.get('phone')
        mop = request.POST.get('mop')
        amount_paid = Decimal(request.POST.get('amount', '0.00'))  # Default to 0.00 if not provided

        # Determine the total price for the plan over 5 years
        total_years = 5
        if mop == 'annually':
            total_price = Decimal(plan.price) / total_years
            next_payment_due = datetime.now() + timedelta(days=365)
        elif mop == 'semi-annually':
            total_price = Decimal(plan.price) / (2 * total_years)
            next_payment_due = datetime.now() + timedelta(days=182)
        elif mop == 'quarterly':
            total_price = Decimal(plan.price) / (4 * total_years)
            next_payment_due = datetime.now() + timedelta(days=91)
        elif mop == 'monthly':
            total_price = Decimal(plan.price) / (12 * total_years)
            next_payment_due = datetime.now() + timedelta(days=30)
        elif mop == 'spot':
            total_price = Decimal(plan.price)
            next_payment_due = None  # No next payment needed for one-time payment
        else:
            total_price = Decimal(plan.price) / total_years
            next_payment_due = datetime.now() + timedelta(days=365)

        # Calculate the remaining balance after the initial payment
        balance = plan.price

        # Create the booking
        booking = Booking.objects.create(
            user_id=user_id,
            plan=plan,
            mop=mop,
            total=total_price,
            balance=balance
        )

        # Create payment reminder if applicable
        if next_payment_due:
            reminder = PaymentReminder.objects.create(
                next_payment_date=next_payment_due
            )
            booking.reminder = reminder
            booking.save()

        # Record the initial payment as a transaction
        transaction = Transaction.objects.create(
            booking=booking,
            title='Initial Payment',
            amount=amount_paid,
            date=timezone.now()
        )
        transaction.save()

        return redirect('settlement', id=booking.id)

    # Retrieve the plan based on the provided ID for rendering the form
    plan = get_object_or_404(Plan, id=id)
    total_price = plan.price

    return render(request, 'blog/settlement.html', {'plan': plan, 'total_price': total_price})

def display_payment(request, id):
    booking = get_object_or_404(Booking, id=id)

    plan = booking.plan
    total_price = calculate_total_price(plan, booking.mop)

    context = {
        'booking': booking,
        'total_price': total_price,
    }

    return render(request, 'blog/payment.html', context)

@csrf_exempt
@login_required
def todos1(request, id):    
    if request.method == 'POST':
        try:
            # Parse the request body to get transaction_id, amount, and date
            data = json.loads(request.body)
            transaction_id = data.get('transaction_id')
            amount = data.get('amount')
            date = data.get('date')
            
            # Ensure all necessary data is present
            if not transaction_id or not amount or not date:
                return JsonResponse({"error": "Missing transaction_id, amount, or date"}, status=400)
            
            # Retrieve the Booking object using the id from the URL
            booking = get_object_or_404(Booking, id=id)
            
            # Create a new transaction object
            transaction = Transaction(
                title=transaction_id,
                amount=amount,
                date=date,
                booking=booking  # Associate the transaction with the booking
            )

            # Save the transaction data to the database
            transaction.save()

            booking.calculate_balance()

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "GET method not allowed"}, status=405)    

def calculate_total_price(plan, mop):
    # Calculate the total price based on the plan and payment frequency
    total_price = plan.price

    if mop == 'annually':
        total_price /= 5
    elif mop == 'semi-annually':
        total_price /= (5 * 2)
    elif mop == 'quarterly':
        total_price /= (5 * 4)
    elif mop == 'monthly':
        total_price /= (5 * 12)

    return total_price

def transactionlist(request):
  items = Transaction.objects.all().order_by('-id')
  template = loader.get_template('after_payment.html')
  context = {
    'todos' : items,
  }
  return HttpResponse(template.render(context, request))

def payment_reminder_view(request):
    user = request.user
    payment_reminders = PaymentReminder.objects.filter(booking__user=user).order_by('-id')
    
    reminders_with_balance = []
    for reminder in payment_reminders:
        booking = reminder.amount
        total_years = Decimal(5)  # Convert to Decimal
        
        if booking.mop == 'monthly':
            total_plan_price = booking.plan.price / Decimal(12 * total_years)
        elif booking.mop == 'quarterly':
            total_plan_price = booking.plan.price / Decimal(4 * total_years)
        elif booking.mop == 'semi-annually':
            total_plan_price = booking.plan.price / Decimal(2 * total_years)
        elif booking.mop == 'annually':
            total_plan_price = booking.plan.price / Decimal(total_years)
        elif booking.mop == 'spot':
            total_plan_price = booking.plan.price  # One-time payment
        else:
            total_plan_price = booking.plan.price / Decimal(total_years)

        

        reminders_with_balance.append({
            'reminder': reminder,
        })
    
    context = {
        'reminders_with_balance': reminders_with_balance
    }

    return render(request, 'blog/paymentreminder.html', context)

def account(request):
    try:
        user_account = Account.objects.get(auth_user=request.user.id)
    except Account.DoesNotExist:
        user_account = None
    context = {
        'user_account': user_account,
    }

    return render(request, 'blog/userprofile.html', context)

def update_account(request, id):
    try:
        user_id = User.objects.get(pk=id)
        account = Account.objects.get(auth_user=user_id)
    except Account.DoesNotExist:
        account = None

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        contact = request.POST['contact']
        address = request.POST['address']
        birthday = request.POST['birthday']

        if account:
            account.contact = firstname
            account.contact = lastname
            account.contact = contact
            account.address = address
            account.birthday = birthday
            account.save()
        else:
            Account.objects.create(firstname=firstname, lastname=lastname, contact=contact, address=address, birthday=birthday, auth_user=user_id)

        return HttpResponseRedirect(reverse('plan'))

    return render(request, 'user/account.html', {'account': account})

@login_required
def delete_plan(request, plan_id):
    if not request.user.is_staff:
        return redirect('login')  # or any other appropriate action

    plan = get_object_or_404(Plan, id=plan_id)
    
    if request.method == 'POST':
        plan.delete()
        return redirect('planlist')  # Redirect to the plan list after deletion
    
    return render(request, 'confirm_delete.html', {'plan': plan})