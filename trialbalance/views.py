from datetime import datetime

from django.db.models import Sum, Q
from django.shortcuts import render, redirect

from transactions.models import Transaction
from trialbalance.models import trial_balance


# Create your views here.
def generate_trial_balance(request):
    year = request.GET.get(
        'year'
    )

    month = request.GET.get(
        'month'
    )

    if not year:
        year = datetime.now().year

    if not month:
        month = datetime.now().month

    # remove old generated data
    trial_balance.objects.filter(
        financial_year=year,
        financial_month=month
    ).delete()

    data = Transaction.objects.filter(

        transaction_date__year=year,

        transaction_date__month=month

    ).values(
        'branch_id',
        'gl_no'
    ).annotate(

        debit_total=Sum(
            'amount',
            filter=Q(
                dr_cr_in=1
            )
        ),

        credit_total=Sum(
            'amount',
            filter=Q(
                dr_cr_in=2
            )
        )

    )

    for row in data:
        debit = row['debit_total'] or 0

        credit = row['credit_total'] or 0

        opening = 0

        closing = (
                opening
                + debit
                - credit
        )

        trial_balance.objects.create(

            financial_year=year,

            financial_month=month,

            branch_id=row['branch_id'],

            gl=row['gl_no'],

            opening_balance=opening,

            debit=debit,

            credit=credit,

            closing_balance=closing,

            status=1

        )

    return redirect(
        'trialbalance:trialbalance_summary'
    )

def trailbalance_temp(request):
    return render(request,'trialbalance.html')

def trialbalance_summary(request):
    data = trial_balance.objects.all().order_by('-id')

    year = request.GET.get('year')

    month = request.GET.get('month')
    gl_code = request.GET.get('gl_no')

    if year:
        data = data.filter(
            financial_year=year
        )

    if month:
        data = data.filter(
            financial_month=month
        )

    if gl_code:
            data = data.filter(
                gl=gl_code
            )


    total_debit = data.aggregate(
        Sum('debit')
    )['debit__sum'] or 0

    total_credit = data.aggregate(
        Sum('credit')
    )['credit__sum'] or 0

    return render(
        request,
        'trialbalance_summary.html',
        {
            'data': data,
            'total_debit': total_debit,
            'total_credit': total_credit
        }
    )
