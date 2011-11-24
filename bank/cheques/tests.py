"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""


"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from django.test.client import Client
import unittest

from cheques.models import Account, ChequeBook, Cheque, Employee, Customer
from cheques.views import SearchAccountNumberForm, ChequePaymentForm, EmployeeLoginForm, CustomerLoginForm, IssueChequeBookForm, ChequeStatusForm
import datetime
from datetime import timedelta
from django.forms.fields import DateField, TimeField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect
try:
    from decimal import Decimal
except ImportError:
    from django.utils._decimal import Decimal

class NavigationTestCase(TestCase):
    
    
    def test_ChequeCancellation(self):

	from cheques.views import ChequeCancellationForm
       
	first_cheque_number= 111113
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2011-11-11', first_cheque_number= first_cheque_number)
	cheque_number= 111113
	c = Client()
        response = c.post('/cheques/employeeMenu/e_chequeCancellation/?account_number=30446461991',{'cheque_number':cheque_number})
	for num in Cheque.objects.all():
		a_num=num.cheque_number
		if cheque_number==a_num:
			cheque_status=num.status
	
	self.assertEqual(cheque_status,'cancelled')
        self.assertEqual(response.status_code,200)

    def test_invalid_Chequenumber_cancellation(self):

	from cheques.views import ChequeCancellationForm
       
	first_cheque_number= 111113
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2011-11-11', first_cheque_number= first_cheque_number)
	cheque_number= 111211
	c = Client()
        response = c.post('/cheques/employeeMenu/e_chequeCancellation/?account_number=30446461991',{'cheque_number':cheque_number})
	self.assertEqual(response.context['message'], "Invalid Cheque number")
        self.assertEqual(response.status_code,200)

   
      
    def test_valid_employeelogin(self):
	newEmployee = Employee.objects.create(employee_id= '123', name='sakshi', password="verma")
	c = Client()
	
        response = c.post('/cheques/employeeLogin/',{'employee_id': '123', 'password': 'verma'})
	self.assertEqual(response.status_code,200)
	

    def test_invalid_employeelogin(self):
	newEmployee = Employee.objects.create(employee_id= '123', name='sakshi', password="verma")
	c = Client()
	
        response = c.post('/cheques/employeeLogin/',{'employee_id': '12321', 'password': 'verma'})
	
	self.assertEqual(response.context['error_message'], "Invalid ID or Password")
        self.assertEqual(response.status_code,200)
     
    def test_valid_customerlogin(self):
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=0)
	newCustomer = Customer.objects.create(username= '123', name='sakshi', password="verma", account_number=newAccount)
	c = Client()
	
        response = c.post('/cheques/customerLogin/',{'username': '123', 'password': 'verma'})
	self.assertEqual(response.status_code,200)
	

    def test_invalid_customerlogin(self):
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=0)
	newCustomer = Customer.objects.create(username= '123', name='sakshi', password="verma", account_number=newAccount)
	c = Client()
	
        response = c.post('/cheques/customerLogin/',{'username': '123', 'password': 'sakshi'})
	
	self.assertEqual(response.context['error_message'], "Invalid username or password")
        self.assertEqual(response.status_code,200)   


