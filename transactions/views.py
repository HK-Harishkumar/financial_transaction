from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from masters.models import *
import pandas as pd

from transactions.models import validation_log, Transaction


# Create your views here.


def hello(request):
    return HttpResponse("Hello",content_type='application/json')


def transaction(request):
    return render(request,'transaction.html')


def upload_transaction(request):
    try:
        success_count = 0
        error_count = 0

        if request.method == "POST":

            excel_file = request.FILES['excel_file']

            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():

                try:

                    voucher_no = str(row['Voucher No']).strip()

                    vendor_code = str(row['Vendor Code']).strip()

                    gl_code = str(row['GL Code']).strip()

                    branch_code = str(row['Branch Code']).strip()

                    amount = float(row['Amount'])

                    dr_cr = str(row['DR_CR']).strip()

                    # Vendor Validation

                    vendor = Vendor.objects.filter(
                        vendor_code=vendor_code,status=1
                    ).first()

                    if not vendor:
                        validation_log.objects.create(
                            row_no=index + 2,
                            voucher_no=voucher_no,
                            error_type="INVALID_VENDOR",
                            error_message="Vendor Not Found"
                        )

                        error_count += 1

                        continue
                    else:
                        vendor_id = vendor.id

                    # GL Validation

                    gl = GL.objects.filter(
                        gl_no=gl_code,status=1
                    ).first()

                    if not gl:
                        validation_log.objects.create(
                            row_no=index + 2,
                            voucher_no=voucher_no,
                            error_type="INVALID_GL",
                            error_message="GL Code Not Found"
                        )

                        error_count += 1

                        continue


                    # Branch Validation

                    branch = Branch.objects.filter(
                        branch_code=branch_code,status=1
                    ).first()

                    if not branch:
                        validation_log.objects.create(
                            row_no=index + 2,
                            voucher_no=voucher_no,
                            error_type="INVALID_BRANCH",
                            error_message="Branch Not Found"
                        )

                        error_count += 1

                        continue
                    else:
                        branch_id = branch.id

                    # Amount Validation

                    if amount <= 0:
                        validation_log.objects.create(
                            row_no=index + 2,
                            voucher_no=voucher_no,
                            error_type="INVALID_AMOUNT",
                            error_message="Amount Must Be Greater Than Zero"
                        )

                        error_count += 1

                        continue

                    # Duplicate Voucher Validation

                    duplicate = Transaction.objects.filter(
                        voucher_no=voucher_no
                    ).exists()

                    if duplicate:
                        validation_log.objects.create(
                            row_no=index + 2,
                            voucher_no=voucher_no,
                            error_type="DUPLICATE_VOUCHER",
                            error_message="Voucher Already Exists"
                        )

                        error_count += 1

                        continue

                    # Save Transaction

                    if dr_cr == 'DR':
                        dr_cr_in =1
                    else:
                        dr_cr_in  = 2

                    Transaction.objects.create(

                        voucher_no=voucher_no,

                        transaction_date=row['Date'],

                        vendor_id=vendor_id,

                        gl_no=gl_code,

                        branch_id=branch_id,

                        amount=amount,

                        dr_cr_in=dr_cr_in

                    )

                    success_count += 1

                except Exception as e:

                    validation_log.objects.create(

                        row_no=index + 2,

                        voucher_no=voucher_no,

                        error_type="SYSTEM_ERROR",

                        error_message=str(e)

                    )

                    error_count += 1

        return render(
            request,
            "transaction.html",
            {
                "success_count": success_count,
                "error_count": error_count
            }
        )
    except Exception as e:
        return render(
            request,
            "transaction.html",
            {
                "errors": str(e),
            }
        )


def transaction_summary(request):
    data = Transaction.objects.select_related(
    'vendor','branch').order_by('-id')

    voucher_no = request.GET.get(
        'voucher_no'
    )

    vendor = request.GET.get(
        'vendor'
    )

    branch_id = request.GET.get(
        'branch'
    )

    if voucher_no:
        data = data.filter(
            voucher_no__icontains=voucher_no
        )

    if vendor:
        data = data.filter(
            vendor_id=vendor
        )

    if branch_id:
        data = data.filter(
            branch_id=branch_id
        )

    vendors =  Vendor.objects.all()
    branches = Branch.objects.all()

    return render(request,'transaction_summary.html',{"data":data,"vendors":vendors,"branches":branches})\


