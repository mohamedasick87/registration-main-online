from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.widgets import ManyToManyWidget
from .models import Registration, Event, RegistrationStatus

# Custom filter for technical events
class TechnicalEventFilter(admin.SimpleListFilter):
    title = 'Technical Events'
    parameter_name = 'technical_events'

    def lookups(self, request, model_admin):
        technical_events = Event.objects.filter(event_type='technical')
        return [(event.id, event.name) for event in technical_events]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(technical_events__id=self.value())
        return queryset

# Custom filter for non-technical events
class NonTechnicalEventFilter(admin.SimpleListFilter):
    title = 'Non-Technical Events'
    parameter_name = 'non_technical_events'

    def lookups(self, request, model_admin):
        non_technical_events = Event.objects.filter(event_type='non_technical')
        return [(event.id, event.name) for event in non_technical_events]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(non_technical_events__id=self.value())
        return queryset

# Define the import-export resource for the Registration model
class RegistrationResource(resources.ModelResource):
    technical_events = fields.Field(
        column_name='technical_events',
        attribute='technical_events',
        widget=ManyToManyWidget(Event, field='name')
    )
    non_technical_events = fields.Field(
        column_name='non_technical_events',
        attribute='non_technical_events',
        widget=ManyToManyWidget(Event, field='name')
    )
    payment_mode = fields.Field(
        column_name='payment_mode',
        attribute='payment_mode'
    )
    paid_status = fields.Field(
        column_name='paid_status',
        attribute='paid_status'
    )

    class Meta:
        model = Registration
        fields = (
            'id', 'member_id', 'name', 'college', 'department', 'phone', 'email',
            'paper_title', 'paper_abstract', 'technical_events', 'non_technical_events',
            'payment_mode', 'payment_link', 'transaction_number', 'paid_status'
        )
        export_order = (
            'id', 'member_id', 'name', 'college', 'department', 'phone', 'email',
            'paper_title', 'paper_abstract', 'technical_events', 'non_technical_events',
            'payment_mode', 'payment_link', 'transaction_number', 'paid_status'
        )

class RegistrationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RegistrationResource

    # Specify fields to display in the list view
    list_display = ('name', 'college', 'department', 'email', 'phone', 'payment_mode', 'paid_status')  # Include paid_status

    # Add `paid_status` to be editable directly from the list view
    list_editable = ('paid_status',)  # Make paid_status editable

    # Add custom filters for technical and non-technical events
    list_filter = (TechnicalEventFilter, NonTechnicalEventFilter, 'paid_status')  # Include paid_status filter

    # Display fields for better searching
    search_fields = ('name', 'college', 'email')

    # Use filter_horizontal to make selecting many-to-many fields easier in forms
    filter_horizontal = ('technical_events', 'non_technical_events')

@admin.register(RegistrationStatus)
class RegistrationStatusAdmin(admin.ModelAdmin):
    list_display = ('is_open',)  # Display the is_open field in the admin list view
    list_filter = ('is_open',)    # Add a filter option for is_open
    search_fields = ('is_open',)

# Register the models and the admin classes
admin.site.register(Event)
admin.site.register(Registration, RegistrationAdmin)
