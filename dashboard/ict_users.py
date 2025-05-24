from django.shortcuts import render, redirect
from user.decorators import ict_required

@ict_required
def ict_dashboard(request):
    """
    ICT Dashboard view.
    """
    if request.user.is_authenticated and request.user.profile.user_type.lower() == 'ict':
        return render(request, 'Dashboard/HOD/index.html', context={})
    else:
        return redirect('login')