from .models import OrganizationSetting


def company_detail(request):
    company_detail = OrganizationSetting.objects.first()
    return{
        'company_detail': company_detail
    }