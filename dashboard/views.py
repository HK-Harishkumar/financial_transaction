from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse
from django.shortcuts import render

from transactions.models import Transaction
from openpyxl import Workbook


# Create your views here.


def dashboard(request):
    # Vendor Payment Trend

    vendor_analysis = Transaction.objects.select_related(
    'vendor'
).values(
        'vendor','vendor__vendor_name'
    ).annotate(

        total_amount=Sum('amount'),

        transaction_count=Count('id')

    ).order_by(
        '-total_amount'
    )

    # GL Pattern Analysis

    gl_analysis = Transaction.objects.values(
        'gl_no'
    ).annotate(

        total_amount=Sum('amount'),

        count=Count('id')

    ).order_by(
        '-total_amount'
    )

    # Branch Analysis

    branch_analysis = Transaction.objects.select_related(
    'branch'
).values(
        'branch','branch__branch_name'
    ).annotate(

        total_amount=Sum('amount'),

        count=Count('id')

    ).order_by(
        '-total_amount'
    )

    # Repeated Transaction Detection

    repeated = Transaction.objects.values(

        'vendor_id',
        'gl_no',
        'amount'

    ).annotate(

        repeat_count=Count('id')

    ).filter(

        repeat_count__gt=1

    )

    monthly_trend = Transaction.objects.annotate(

        month=ExtractMonth(
            'transaction_date'
        )

    ).values(

        'month'

    ).annotate(

        amount=Sum('amount'),

        count=Count('id')

    ).order_by('month')

    # 6. High Value Transactions
    high_value = Transaction.objects.select_related(
        'vendor',
        'branch'
    ).order_by(
        '-amount'
    )[:10]

    # 7. Debit Credit Analysis
    dc_analysis = Transaction.objects.values(
        'dr_cr_in'
    ).annotate(

        total=Sum('amount'),

        count=Count('id')

    )

    # Dashboard Cards
    total_transactions = Transaction.objects.count()

    total_amount = Transaction.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    vendor_count = Transaction.objects.values(
        'vendor'
    ).distinct().count()

    gl_count = Transaction.objects.values(
        'gl_no'
    ).distinct().count()


    return render(
        request,
        'dashboard.html',
        {

            'vendor_analysis':
                vendor_analysis,

            'gl_analysis':
                gl_analysis,

            'repeated':
                repeated,

            'branch_analysis':
                branch_analysis,

            'monthly_trend':
                monthly_trend,

            'high_value':
                high_value,

            'dc_analysis':
                dc_analysis,

            'total_transactions':
                total_transactions,

            'total_amount':
                total_amount,

            'vendor_count':
                vendor_count,

            'gl_count':
                gl_count

        }
    )



def download_vendor_analysis_excel(request):


    data = Transaction.objects.select_related(
        'vendor',
        'branch'
    ).values(
        'vendor__vendor_name',
        'gl_no',
        'branch__branch_name'
    ).annotate(
        total_amount=Sum('amount'),
        transaction_count=Count('id')
    ).order_by('-total_amount')



    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Vendor Analysis"



    # Header

    sheet.append([
        "Vendor Name",
        "GL No",
        "Branch",
        "Total Amount",
        "Transaction Count"
    ])



    # Data

    for row in data:

        sheet.append([

            row['vendor__vendor_name'],

            row['gl_no'],

            row['branch__branch_name'],

            row['total_amount'],

            row['transaction_count']

        ])



    response = HttpResponse(
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


    response['Content-Disposition'] = (
        'attachment; filename=vendor_analysis.xlsx'
    )


    workbook.save(response)


    return response