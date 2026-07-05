from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from masters.models import Vendor, GL, Branch


# Create your views here.


def hello(request):
    return HttpResponse("Hello",content_type='application/json')


# Create your views here.\
def index(request):
    return render(request,'login.html')
def login(request):
    return render(request,'base.html')

def vendor_temp(request):
    return render(request,'vendor_master.html')

def create_vendor(request):
    print("VIEW CALLED")

    if request.method == "POST":
        print("POST CALLED")
        vendor_code = request.POST.get('vendor_code')
        vendor_name = request.POST.get('vendor_name')
        status = request.POST.get('status')

        if status != None and status != '' :
            if status == '':
                status_value = 1
            if status == '':
                status_value = 0
            else:
                status_value = 1
        else:
            status_value = 1

        Vendor.objects.create(
            vendor_code=vendor_code,
            vendor_name=vendor_name,
            status=status_value
        )

        return redirect(
            'masters:vendor_list'
        )

    return render(request,'vendor_master.html')


def vendor_list(request):
    vendors = Vendor.objects.all().order_by('-id')
    vendor_name = request.GET.get(
        'vendor_name'
    )
    if vendor_name:
        vendors = vendors.filter(
            vendor_name__icontains=vendor_name
        )
    return render(request, 'vendor_list.html',{"vendors":vendors})

def gl_temp(request):
    return render(request,'gl_master.html')

def create_gl(request):
    if request.method == "POST":
        gl_code = request.POST.get('gl_code')

        # gl_name = request.POST.get('gl_name')

        gl_type = request.POST.get('gl_type')
        gl_desc = request.POST.get('gl_desc')

        status = request.POST.get('status')

        if status != None and status != '' :
            if status == '':
                status_value = 1
            if status == '':
                status_value = 0
            else:
                status_value = 1
        else:
            status_value = 1
        GL.objects.create(
            gl_no=gl_code,
            # gl_name=gl_name,
            gl_desc=gl_desc,
            gl_type=gl_type,
            status=status_value

        )

        return redirect(
            'masters:gl_list'
        )

    return render(
        request,
        'gl_master.html'
    )


def gl_list(request):
    gls = GL.objects.all().order_by('-id')
    gl_code = request.GET.get(
        'gl_code'
    )
    if gl_code:
        gls = gls.filter(
            gl_no__icontains=gl_code
        )
    return render(request,'gl_list.html', {'gls': gls})




def branch_temp(request):
    return render(request,'branch_master.html')

def create_branch(request):
    if request.method == "POST":
        branch_code = request.POST.get('branch_code')
        branch_name = request.POST.get('branch_name')

        status = request.POST.get('status')

        if status != None and status != '' :
            if status == '':
                status_value = 1
            if status == '':
                status_value = 0
            else:
                status_value = 1
        else:
            status_value = 1

        Branch.objects.create(
            branch_code=branch_code,
            branch_name=branch_name,
            status=status_value

        )

        return redirect(
            'masters:branch_list'
        )

    return render(
        request,
        'branch_master.html'
    )


def branch_list(request):
    branchs = Branch.objects.all().order_by('-id')
    branch_name = request.GET.get(
        'branch_name'
    )
    if branch_name:
        branchs = branchs.filter(
            branch_name__icontains=branch_name
        )

    return render(request,'branch_list.html', {'branchs': branchs})


