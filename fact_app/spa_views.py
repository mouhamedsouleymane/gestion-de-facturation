from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def spa_index(request):
    # Single Page App entrypoint
    return render(request, 'spa.html')
