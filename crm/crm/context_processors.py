from organization.models import Organization

def user_context(request):

    request.user.ownedorgs = Organization.objects.filter(
        administrator=request.user.id)
    return dict()

