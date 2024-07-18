# Create your models here.
import random
#from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import datetime
from django.db import models
import random_word
from decimal import Decimal
import string
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

def generate_custom_primary_key():
    random_word_str = random_word.RandomWords().get_random_word()
    random_number = random.randint(1000, 9999)
    return f"{random_word_str}{random_number}"

# Create your models here.

class Gender(models.Model):
    Name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.Name
    
class MaritalStatus(models.Model):
    Name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.Name

class MyUser(AbstractUser):
    INACTIVE = 'inactive'
    INCOMPLETE = 'incomplete'
    RENEWAL = 'renewal'
    ACTIVE = 'active'
    STATUS_CHOICES = [
        (INACTIVE, 'inactive'),
        (RENEWAL, 'incomplete'),
        (ACTIVE, 'renewal'),
        (INCOMPLETE,'active'),
    ]
    usercode = models.CharField(max_length=8)
    dateofbirth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    marital_status = models.ForeignKey('MaritalStatus', on_delete=models.CASCADE, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(max_length=250, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    keyBonus = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,)
    phone_number_1 = models.CharField(max_length=250, blank=True, null=True)
    phone_number_2 = models.CharField(max_length=250, blank=True, null=True)
    my_status = models.CharField(max_length=255, choices=STATUS_CHOICES,null=True, blank=True, default='incomplete' )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',  # Custom related_name for groups
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set_permissions',  # Custom related_name for user_permissions
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created for the first time
            self.is_staff = True
        if not self.usercode:
            self.usercode = self.generate_unique_usercode()
        super().save(*args, **kwargs)
    def generate_unique_usercode(self):
        length = 8
        while True:
            usercode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not MyUser.objects.filter(usercode=usercode).exists():
                break
        return usercode
    


    def __str__(self):
        return self.username
class State(models.Model):
    Name = models.CharField(max_length=200, null=True)
    special = models.CharField(max_length=200, default=generate_custom_primary_key)
    def __str__(self):
        return self.Name
    

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=20,null=True)
    package_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0),MaxValueValidator(10000000)],null=True)
    bonus = models.ManyToManyField('Product_bonus')
    

    def save(self, *args, **kwargs):
        if not self.product_id:
            last_instance = Products.objects.order_by('product_id').last()
            if last_instance:
                self.product_id = last_instance.product_id + 100
            else:
                self.product_id = 100  # Initial value if no instances exist yet
        super(Products, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.product_id} - {self.package_name}'





class Occurance(models.Model):
        INSTANT = 'instant'
        WEEKLY = 'weekly'
        WEEKEND = 'weekend'
        MONTHLY = 'monthly'
        MONTHEND = 'monthend'
        OCCURRENCE_CHOICES = [
            (INSTANT, 'Instant'),
            (WEEKLY, 'Weekly'),
            (WEEKEND, 'Weekend'),
            (MONTHLY, 'Monthly'),
            (MONTHEND, 'Month-End'),
        ]
        occurrence_type = models.CharField(max_length=10,choices=OCCURRENCE_CHOICES,default=INSTANT)
        
        def __str__(self):
            return f'{self.get_occurrence_type_display()} Occurrence'

        class Meta:
            verbose_name = 'Occurrence'
            verbose_name_plural = 'Occurrences'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('home.MyUser', on_delete=models.CASCADE)
    package = models.ForeignKey('home.Products', on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = Orders.objects.order_by('-order_id').first()
            if last_order:
                last_id = last_order.order_id
            else:
                last_id = 0
            self.order_id = last_id + 1
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the instance is being created
        super().save(*args, **kwargs)
        acc_type= AccType.objects.get(id=3)
        if created:
            accType=acc_type
            package_price = self.package.package_price
            package_name = self.package.package_name
            trans_code = Transaction_codes.objects.get(tran_code=100)
            # Create a transaction for this order
            Transaction.objects.create(
                accType=acc_type,
                order_date=self.order_date,
                user=self.user,
                tran_code=trans_code,  # Assuming 100 is the initial transaction code
                desc=f'Txn - {package_name} - {trans_code.tran_bonus.bonus}',
                amount=package_price,  # Assuming package has a price field
                  # Assuming user has a balance field
            )
        if created:
            acc_type= AccType.objects.get(id=1)
            accType=acc_type
            package_price = self.package.package_price
            package_name = self.package.package_name
            
            trans_code = Transaction_codes.objects.get(tran_code=100)
            bonus = self.package.bonus.all()
            amt = Decimal('0.00')
            percent = [bonus.percentage for bonus in bonus]
            for per in percent:
                print(per)
                perc = (per/100)
                amt += perc * package_price
            
            Transaction.objects.create(
                accType=acc_type,
                order_date=self.order_date,
                user=self.user,
                tran_code=trans_code,  # Assuming 100 is the initial transaction code
                desc=f'Txn - {package_name} - {trans_code.tran_bonus.bonus}',
                amount=amt,  # Assuming package has a price field
                  # Assuming user has a balance field
            )

    def __str__(self):
        return f'PD-{self.order_id}'

class Transaction(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    accType = models.ForeignKey('AccType',on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE, blank=True, null=True)
    tran_code = models.ForeignKey("Transaction_codes", on_delete=models.CASCADE)
    desc = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new instance
            super().save(*args, **kwargs)  # Save the transaction first to get the ID
            # Update or create corresponding Account
            try:
                account = Account.objects.get(acc_holder=self.user, acc_type=self.accType)
                account.transaction_type=self.tran_code.transaction_type
                account.amount = self.amount
                account.save()
            except Account.DoesNotExist:
                # Handle if Account doesn't exist
                account = Account.objects.create(
                acc_type=self.accType,
                acc_holder=self.user,
                amount=self.amount,
                transaction_type=self.tran_code.transaction_type,
                )
                account.save()

        else:
            super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Trans-{self.id}'


class Product_bonus(models.Model):
    bonus = models.CharField(max_length=50,null=True)
    occurance = models.ForeignKey('Occurance',on_delete=models.CASCADE,)
    percentage = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    def __str__(self):
        return f'{self.bonus}'


class Bonus_tran(models.Model):
    trandate = models.DateTimeField(auto_now_add=True)
    rundate = models.DateTimeField()
    user = models.ForeignKey('home.MyUser', on_delete=models.CASCADE)
    acc_type = models.ForeignKey('AccType', on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    tc = models.ForeignKey('Transaction_codes', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=(('Processed', 'Processed'), ('Pending', 'Pending')), default='Pending')
    def create_and_process_transaction(self):
        package_price = self.order.package.package_price
        package_name = self.order.package.package_name
        trans_code = self.tc

        # Create a transaction for this order
        transaction = Transaction.objects.create(
            accType=self.acc_type,
            order_date=timezone.now(),
            user=self.user,
            tran_code=trans_code,
            desc=f'Txn - {package_name} - {trans_code.tran_bonus.bonus}',
            amount=package_price,
          # Set status directly when creating Transaction
        )
        print(self.status)
        self.status = 'Processed'
        self.save()
        # Update status of Bonus_tran object to 'Processed' and save it
       
        return transaction 





class AccType(models.Model):
    name = models.CharField(max_length=255,null=True)
    status = models.CharField(choices=(('Active','Active'),('Inactive','Inactive')),max_length=25)
    def __str__(self):
        return f'{self.name}'

class Transaction_codes(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        (1, 'Credit'),
        (-1, 'Debit'),
    )

    tran_code = models.AutoField(primary_key=True)
    tran_bonus = models.OneToOneField('Product_bonus', on_delete=models.CASCADE, unique=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        if self.tran_code is None:
            last_tran_code = Transaction_codes.objects.all().order_by('-tran_code').first()
            if last_tran_code is not None:
                self.tran_code = last_tran_code.tran_code + 50
            else:
                self.tran_code = 100  # Initial value if table is empty
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.tran_code}- {self.tran_bonus}'

    """def post_to_account(self, amount):
        # Create Account instance and save it
        account = Account(
            acc_type=self.tran_bonus.acc_type,
            acc_holder=self.tran_bonus.acc_holder,
            amount=amount,
            transaction_type=self.transaction_type,
        )
        account.save()"""

class Account(models.Model):
    acc_type = models.ForeignKey(AccType, on_delete=models.CASCADE)
    acc_holder = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    desc = models.CharField(max_length=255, null=True,blank=True,)
    transaction_type = models.IntegerField(choices=Transaction_codes.TRANSACTION_TYPE_CHOICES, default=1)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    cur_bal = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            # Initialize cur_bal based on amount and transaction_type
            if self.amount is not None:
                self.cur_bal = self.amount * self.transaction_type
            else:
                self.cur_bal = 0  # Default value
        else:  # Existing instance
            # Update cur_bal based on amount and transaction_type
            if self.amount is not None:
                self.cur_bal = self.amount * self.transaction_type + self.cur_bal
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.acc_holder}'
    