from django.db import models
import datetime

def get_choices(lst):
    return [(i, i) for i in lst]


#
# Person
#

pprint_pan = lambda pan: "%s %s %s" % (pan[:5], pan[5:9], pan[9:])

class Person(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    fathers_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    status = models.CharField(max_length=32, choices=get_choices([

        'Individual', 
        'HUF', 
        'Partnership Firm', 
        'Domestic Company', 
        'LLP',
        'Trust(ITR 7)', 
        ]), default='Individual Salaried')
    employer = models.CharField(max_length=64, null=True, blank=True)
    self_occupied = models.BooleanField()

    pan_number = models.CharField(max_length=32, unique=True)
    user_id = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)

    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_branch = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=32, null=True, blank=True)
    micr = models.CharField(max_length=32, blank=True, null=True)
    ifsc_code = models.CharField(max_length=32, null=True, blank=True)
    account_type =  models.CharField(max_length=32, choices=get_choices(['SB', 'CA', 'CC']), default='SB')

    contact_number = models.CharField(max_length=13, null=True, blank=True, db_index=True)
    email = models.EmailField(null=True, blank=True, db_index=True)
    address =  models.TextField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    pincode = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    date_of_birth_or_incarnation = models.DateField(null=True, blank=True)

    def pan_number_pprint(self):
        return pprint_pan(self.pan_number)

    pan_number_pprint.admin_order_field = 'pan_number_pprint'
    pan_number_pprint.short_description = 'Pan Number'

  
    def _trim(self, *args):
        for field in args:
            value = getattr(self, field)
            setattr(self, field, value.replace(' ', ''))

    def save(self):
        self._trim('pan_number')
        super(Person, self).save()

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.pan_number)

class MetadataPerson(models.Model):
    person =  models.ForeignKey(Person)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)



#
#  Report
#


class Report(models.Model):
    finanyr = lambda yr: "%s - %s" % (yr, yr+1) 
    years = [(finanyr(i), finanyr(i)) for i in xrange(1980, 2020)]
    person =  models.ForeignKey(Person)
    financial_year = models.CharField(max_length=11, choices=years, default=finanyr(datetime.datetime.now().year - 1))
    assessment_year = models.CharField(max_length=11, choices=years, default=finanyr(datetime.datetime.now().year))
    return_filed_on = models.DateField() 
    returned_income = models.DecimalField(max_digits=12, decimal_places=2)


    #Advanced Tax
    july = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    september = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    december = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    march = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    #Interest Detail
    interest_234_a = models.DecimalField("Interest 234(a)", max_digits=12, decimal_places=2, null=True, blank=True)
    interest_234_b = models.DecimalField("Interest 234(b)", max_digits=12, decimal_places=2, null=True, blank=True)
    interest_234_c = models.DecimalField("Interest 234(c)", max_digits=12, decimal_places=2, null=True, blank=True)

    
    #Tax detail
    tds = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    self_assessment_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    acknowledgement_number = models.CharField("Ack no.", max_length=64, null=True, blank=True)

    
    #Bill Detail
    bill_raised_on = models.DateField(null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bill_received = models.BooleanField("Bill received ?")
    mode_of_payment = models.CharField(max_length=16, choices=get_choices(['Cash', 'Cheque', 'DD', 'Bank Transfer']), null=True, blank=True)
    payment_detail = models.CharField(max_length=16, null=True, blank=True)


    #Order 143(1)
    order_received_on_143_1 = models.DateField("143(1) Order received on", null=True, blank=True)
    assessed_income_143_1 = models.DecimalField("Assessed income", max_digits=12, decimal_places=2, null=True, blank=True)
    assessed_tax_143_1 = models.DecimalField("Assessed tax", max_digits=12, decimal_places=2, null=True, blank=True)
    refund_amount_143_1 = models.DecimalField("Refund amount", max_digits=12, decimal_places=2, null=True, blank=True)
    demand_raised_amount_143_1 = models.DecimalField("Demand raised for ", max_digits=12, decimal_places=2, null=True, blank=True)
    refund_received_on_143_1 = models.DateField("Refund received on", null=True, blank=True)

    #Order 143(2)
    order_received_on_143_2 = models.DateField("Notice received on", null=True, blank=True)


    #Order 143(3)
    order_received_on_143_3 = models.DateField("Order received on", null=True, blank=True)
    assessed_income_143_3 = models.DecimalField("Assessed income", max_digits=12, decimal_places=2, null=True, blank=True)
    assessed_tax_143_3 = models.DecimalField("Assessed tax", max_digits=12, decimal_places=2, null=True, blank=True)
    refund_amount_143_3 = models.DecimalField("Refund amount", max_digits=12, decimal_places=2, null=True, blank=True)
    demand_raised_amount_143_3 = models.DecimalField("Demand raised for", max_digits=12, decimal_places=2, null=True, blank=True)
    refund_received_on_143_3 = models.DateField("Refund received on", null=True, blank=True)


    #Appeal before cit
    filed_on_cit = models.DateField("Filed on", null=True, blank=True)
    order_received_on_cit = models.DateField("Order received on", null=True, blank=True)
    assessed_income_cit = models.DecimalField("Assessed income", max_digits=12, decimal_places=2, null=True, blank=True)
    assessed_tax_cit = models.DecimalField("Assessed tax", max_digits=12, decimal_places=2, null=True, blank=True)


    #Appeal before tribunal
    filed_on_tribunal = models.DateField("Filed on", null=True, blank=True)
    order_received_on_tribunal = models.DateField("Order received on", null=True, blank=True)
    filed_by_tribunal = models.CharField("Filed by", max_length=16, choices=get_choices(['assessee', 'department']), null=True, blank=True)
    assessed_income_tribunal = models.DecimalField("Assessed income", max_digits=12, decimal_places=2, null=True, blank=True)
    assessed_tax_tribunal = models.DecimalField("Assessed tax", max_digits=12, decimal_places=2, null=True, blank=True)



    def got_reimbursement(self):
        return self.refund_amount_143_1 > 0

    got_reimbursement.admin_order_field = 'got_reimbursement'
    got_reimbursement.boolean = True
    got_reimbursement.short_description = 'Got reimbursement ?'


    def tax_paid(self):
        tax = sum([i for i in (self.march, self.september, self.december, self.july) if i is not None])
        
        if tax == 0 and self.tds is not None:
            tax = self.tds
        return tax

    tax_paid.admin_order_field = 'tax_paid'
    tax_paid.boolean = False
    tax_paid.short_description = 'Tax Paid'


    class Meta:
        unique_together = ('person', 'financial_year')

    def __unicode__(self):
        return u'%s - %s' % (self.person, self.financial_year)


class MetadataReport(models.Model):
    report =  models.ForeignKey(Report)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

