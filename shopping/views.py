from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from itertools import groupby

from .models import Einkauf, Laden
from .forms import EinkaufForm, EinkaufEditForm


@login_required
def liste(request):
    """Main shopping list view: open items grouped by store."""
    # Offene Einkäufe, gruppiert nach Laden
    offene = (
        Einkauf.objects
        .filter(gekauft=False)
        .select_related('laden')
        .order_by('laden__reihenfolge', 'laden__name', 'artikel')
    )

    # Gruppierung nach Laden
    gruppen = {}
    for einkauf in offene:
        laden_name = einkauf.laden.name if einkauf.laden else 'Egal'
        if laden_name not in gruppen:
            gruppen[laden_name] = []
        gruppen[laden_name].append(einkauf)

    # Sort: 'Egal' kommt zuoberst
    def sort_key(item):
        if item[0] == 'Egal':
            return (0, '')
        return (1, item[0])

    gruppen_sorted = sorted(gruppen.items(), key=sort_key)

    # Form for new item
    if request.method == 'POST':
        form = EinkaufForm(request.POST)
        if form.is_valid():
            einkauf = form.save(commit=False)
            einkauf.erstellt_von = request.user
            einkauf.save()
            messages.success(request, f'„{einkauf.artikel}" wurde hinzugefügt.')
            return redirect('liste')
    else:
        form = EinkaufForm()

    context = {
        'gruppen': gruppen_sorted,
        'form': form,
        'offene_count': offene.count(),
        'active_tab': 'offen',
    }
    return render(request, 'shopping/liste.html', context)


@login_required
def gekauft_liste(request):
    """List of purchased items."""
    gekauft = (
        Einkauf.objects
        .filter(gekauft=True)
        .select_related('laden')
        .order_by('-geaendert')
    )
    context = {
        'einkäufe': gekauft,
        'active_tab': 'gekauft',
        'gekauft_count': gekauft.count(),
    }
    return render(request, 'shopping/gekauft.html', context)


@login_required
def toggle_gekauft(request, pk):
    """Toggle the purchased state of an item."""
    einkauf = get_object_or_404(Einkauf, pk=pk)
    einkauf.gekauft = not einkauf.gekauft
    einkauf.save()
    status = 'gekauft' if einkauf.gekauft else 'offen'
    messages.success(request, f'„{einkauf.artikel}" als {status} markiert.')
    next_url = request.POST.get('next', request.GET.get('next', '/'))
    return redirect(next_url)


@login_required
def einkauf_edit(request, pk):
    """Edit a shopping item."""
    einkauf = get_object_or_404(Einkauf, pk=pk)
    if request.method == 'POST':
        form = EinkaufEditForm(request.POST, instance=einkauf)
        if form.is_valid():
            form.save()
            messages.success(request, f'„{einkauf.artikel}" wurde aktualisiert.')
            return redirect('liste')
    else:
        form = EinkaufEditForm(instance=einkauf)
    return render(request, 'shopping/edit.html', {'form': form, 'einkauf': einkauf})


@login_required
def einkauf_delete(request, pk):
    """Delete a shopping item."""
    einkauf = get_object_or_404(Einkauf, pk=pk)
    if request.method == 'POST':
        name = einkauf.artikel
        einkauf.delete()
        messages.success(request, f'„{name}" wurde gelöscht.')
        return redirect('liste')
    return render(request, 'shopping/confirm_delete.html', {'einkauf': einkauf})


@login_required
def alle_als_offen(request):
    """Mark all purchased items as open again (reset)."""
    if request.method == 'POST':
        count = Einkauf.objects.filter(gekauft=True).update(gekauft=False)
        messages.success(request, f'{count} Artikel wieder als offen markiert.')
    return redirect('liste')


@login_required
def gekaufte_loeschen(request):
    """Delete all purchased items."""
    if request.method == 'POST':
        count, _ = Einkauf.objects.filter(gekauft=True).delete()
        messages.success(request, f'{count} gekaufte Artikel gelöscht.')
    return redirect('liste')
