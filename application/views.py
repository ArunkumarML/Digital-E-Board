from django.db import transaction
from django.db.models import Func, Count, F
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from application.models import District, State, Customer, Application, PinCode
from core.utils.general import JSONApi
from rest_framework import views
from rest_framework.parsers import MultiPartParser



class NewApplication(views.APIView):
    parser_classes = [MultiPartParser]
    @staticmethod
    @transaction.atomic
    def post(request):
        try:
            data = request.data
            customer = Customer.objects.create(name=data['name'], gender=data['gender'],
                                               government_id_type=data['government_id_type'],
                                               government_id_number=data['govt_num']
                                               ,district_id=data['district'], state_id=data['state'],
                                               pin_code_id=data['pincode'], ownership=data['ownership'])
            Application.objects.create(customer_id=customer.id, category=data['category']
                                       , load=data['load'], remarks=data['remarks'], created_by_id=request.user.id)
            return render(request, template_name="application_list.html", context=data)
        except Exception as e:
            transaction.set_rollback(rollback=True)
            return Response({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApplicationDetails(JSONApi):
    @staticmethod
    def get(request):
        try:
            result = list(Application.objects.filter(id=request.GET['id']).values('id', 'customer__name',
                                                                                  'customer__gender',
                                                                                  'customer__district__pincode',
                                                                                  'customer__district',
                                                                                  'customer__state',
                                                                                  'customer__government_id_type',
                                                                                  'customer__government_id_number',
                                                                                  'created_at__date',
                                                                                  'customer__application__category',
                                                                                  'customer__ownership',
                                                                                  'status', 'load',
                                                                                  'created_by',
                                                                                  'remarks'))
            return Response({"status": True, "data": result},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApplicationList(JSONApi):
    @staticmethod
    def get(request):
        try:
            filters = Application.apply_filters(request, {})
            result = list(Application.objects.filter(**filters).values('id', 'customer__name',
                                                                       'created_at__date',
                                                                       'customer__application__category',
                                                                       'customer__ownership',
                                                                       'status', 'load'))
            return Response({"status": True, "data": result},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GraphData(JSONApi):
    @staticmethod
    def get(request):
        try:
            queryset = Application.objects.annotate(month=Func(F('created_at'), function='EXTRACT',
                                                               template='%(function)s(MONTH from %(expressions)s)'))\
                .values(
                'month').annotate(count=Count('id'))
            for obj in queryset:
                obj['month_name'] = Application.objects.filter(created_at__month=obj['month'],status=request.GET['status']).values_list(
                    Func(F('created_at'), function='to_char', template='%(function)s(%(expressions)s, \'Month\')'),
                    flat=True).first()

            return Response({"status": True, "data": queryset},
                            status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(rollback=True)
            return Response({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DistrictList(JSONApi):
    @staticmethod
    def get(request):
        filters = {
            "valid": True
        }
        if request.GET.get('query'):
            filters["name__icontains"] = request.GET.get('query')

        result_list = list(District.objects.filter(**filters).values("id", "name"))
        return Response({"status": "success", "results": result_list})


class StateList(JSONApi):
    @staticmethod
    def get(request):
        filters = {
            "valid": True
        }
        if request.GET.get('query'):
            filters["name__icontains"] = request.GET.get('query')

        result_list = list(State.objects.filter(**filters).values("id", "name"))

        return Response({"status": "success", "results": result_list})


class PincodeList(JSONApi):
    @staticmethod
    def get(request):
        filters = {
            "valid": True
        }
        if request.GET.get('query'):
            filters["name__icontains"] = request.GET.get('query')

        result_list = list(PinCode.objects.filter(**filters).values("id","value"))

        return Response({"status": "success", "results": result_list})

def application_form(request):
    context = dict()
    return render(request, template_name="application_latest.html", context=context)


def application_list(request):
    context = dict()
    return render(request, template_name="application_list.html", context=context)
