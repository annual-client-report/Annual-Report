from django.contrib import admin
from report.models import Person
from report.models import MetadataPerson
from report.models import MetadataReport
from report.models import Report
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
import datetime

finanyr = lambda yr: "%s - %s" % (yr, yr+1) 
class FinancialYear(SimpleListFilter):
    title = _('financial year')
    parameter_name = 'financial_year'

    def lookups(self, request, model_admin):
        yr = datetime.datetime.now().year
        return [ (finanyr(y), _(str(finanyr(y)))) for y in xrange(yr-1, yr+1)]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        else:
            return queryset.filter(financial_year=self.value())

class RefundStatus(SimpleListFilter):
    title = _('refund status - 143(1)')
    parameter_name = 'refund'

    def lookups(self, request, model_admin):
        return (
            ('completed', _('received')),
            ('not_known', _('not_known')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'received':
            return queryset.filter(refund_received_on_143_1__isnull=False)
        elif self.value() == 'not_known':
            return queryset.filter(refund_received_on_143_1__isnull=True)

class RefundAmount(SimpleListFilter):
    title = _('refund amount')
    parameter_name = 'refund_amount'

    def lookups(self, request, model_admin):
        return (
            ('100000,-1', _(' >= 1,00,000')),
            ('50000,100000', _(' >= 50,000')),
            ('0,50000', _(' < 50,000')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            _min, _max = self.value().split(',')
            results = queryset.filter(refund_amount_143_1__gt=_min)
            if _max != '-1':
                results = results.filter(refund_amount_143_1__lt=_max)
            return results

class MetadataPersonInline(admin.TabularInline):
    model = MetadataPerson
    extra = 2

class MetadataReportInline(admin.TabularInline):
    model = MetadataReport
    extra = 2

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {
                                'fields': 
                                [
                                    'name', 'status', 'fathers_name', 'employer', 'self_occupied'
                                ]}),
        ('Bank Detail',     {
                                'fields': 
                                [
                                    'account_type', 'bank_name', 'bank_branch', 'account_number', 'ifsc_code', 'micr'
                                ]}),
        ('Income Tax Identifier',     
                            {
                                'fields': 
                                [
                                    'pan_number', 'user_id', 'password'
                                ]}),
        ('Personal Detail',     {
                                'fields': 
                                [
                                    'contact_number', 
                                    'email', 
                                    'date_of_birth_or_incarnation', 
                                    'address',
                                    'city',
                                    'pincode',
                                ]}),
    ]

    inlines = [MetadataPersonInline]
    list_display = ['name', 'pan_number_pprint', 'status', 'employer', 'contact_number']
    search_fields = ['name', 'fathers_name', 'contact_number', 'pan_number', 'email']
    list_filter = ['employer', 'city', 'status', 'bank_name']
    list_per_page = 15 

class ReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {  
                                'fields': 
                                [   
                                    'person', 
                                    'financial_year', 
                                    'assessment_year', 
                                    'return_filed_on', 
                                    'returned_income'
                                ]}),
        


        ('Advance Tax',      {  
                                'classes': ('collapse',), 
                                'fields': 
                                [   
                                    'july', 
                                    'september', 
                                    'december', 
                                    'march'
                                ]}),
        ('Interest Details', {
                                'classes':('collapse',), 
                                'fields': 
                                [
                                    'interest_234_a', 
                                    'interest_234_b', 
                                    'interest_234_c'
                                ]}),
        ('Tax Details',      {
                                'fields': 
                                [
                                    'tds', 
                                    'self_assessment_tax', 
                                    'acknowledgement_number'
                                ]}),
        ('Bill Details',      {
                                'fields': 
                                [
                                    'bill_raised_on', 
                                    'bill_amount', 
                                    'mode_of_payment', 
                                    'payment_detail', 
                                    'bill_received'
                                ]}),



        ('Order 143(1)',      {
                                'fields': 
                                [
                                    'order_received_on_143_1', 
                                    'assessed_income_143_1', 
                                    'assessed_tax_143_1', 
                                    'refund_amount_143_1', 
                                    'demand_raised_amount_143_1', 
                                    'refund_received_on_143_1'
                                ]}),
        ('Notice 143(2)',      {
                                'classes':('collapse',), 
                                'fields': 
                                [
                                    'order_received_on_143_2'
                                ]}),
        ('Order 143(3)',      {
                                'classes':('collapse',), 
                                'fields': 
                                [
                                    'order_received_on_143_3', 
                                    'assessed_income_143_3', 
                                    'assessed_tax_143_3', 
                                    'refund_amount_143_3', 
                                    'demand_raised_amount_143_3', 
                                    'refund_received_on_143_3'
                                ]}),



        ('Appeal field before Cit',      
                                {
                                'classes':('collapse',), 
                                'fields': 
                                [
                                    'filed_on_cit', 
                                    'order_received_on_cit', 
                                    'assessed_income_cit', 
                                    'assessed_tax_cit'
                                ]}),
        ('Appeal field before Tribunal',      
                                {
                                'classes':('collapse',), 
                                'fields': 
                                [
                                    'filed_on_tribunal', 
                                    'order_received_on_tribunal', 
                                    'assessed_income_tribunal', 
                                    'assessed_tax_tribunal'
                                ]}),

    ]


    raw_id_fields = ('person',)
    list_display =  [
                        'person', 
                        'financial_year', 
                        'return_filed_on', 
                        'returned_income', 
                        'tax_paid', 
                        'bill_received', 
                        'got_reimbursement', 
                        'acknowledgement_number', 
                        'order_received_on_143_1'
                    ]

    search_fields = [
                        'person__name', 
                        'person__contact_number', 
                        'person__pan_number', 
                        'person__email'
                    ]

    list_filter = [FinancialYear, RefundStatus, RefundAmount, 'bill_received', 'person__city', 'person__status']
    list_per_page = 15 

admin.site.register(Person, PersonAdmin)
admin.site.register(Report, ReportAdmin)

