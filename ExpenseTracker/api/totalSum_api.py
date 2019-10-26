from django.db import models
from rest_framework import serializers
from expense.models import Expenses
from django.db.models import Sum
from rest_framework import viewsets


class ExpenseSerializer(serializers.ModelSerializer):

    totalExpense = serializers.IntegerField()
    many=True

    class Meta:
        model = Expenses
        fields = ['User_ID_id','Amount', 'Catagory', 'Date_Time','totalExpense']

class ExpenseViewSet(viewsets.ModelViewSet):

    Model = Expenses
    # queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):

        id = self.request.query_params.get('UserID')
        if id is None:
            #queryset = Expenses.objects.all().aggregate(Sum('Amount'))
            queryset= Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount'))
        else:
            queryset = Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).filter(User_ID_id=id)
            #queryset = Expenses.objects.raw('SELECT *,SUM("expense_expenses"."Amount") as totalExpense, "expense_expenses"."Catagory" From "expense_expenses" WHERE "expense_expenses"."User_ID_id"=13 GROUP BY "expense_expenses"."Catagory" ,"expense_expenses"."id";')
        return queryset