from asyncore import poll
from django.shortcuts import render
from .models import *
from .forms import AddPolls, NewPollingUnit
from django.db.models import Sum
from django.contrib import messages
# Create your views here.
def polling_results(request, unique_id):
    category = ElectionCategory.objects.get(category_name='presidential')
    results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=unique_id, voting_category=category)
    print(results)
    context = {'results':results, 'results_name':results[0].polling_unit_uniqueid}
    return render (request, 'election_results/index.html', context)

   
def add_poll_results(request):
    form = AddPolls()
    if request.method == 'POST':
        form = AddPolls(request.POST)
        if form.is_valid():
            category = form.cleaned_data['voting_category']
            party_abbr = form.cleaned_data['party']
            form.save(commit=False)
            
            poll = New_Polling_unit.objects.all().filter(voting_category=category, party=party_abbr)
            poll_score = poll.aggregate(Sum('party_score'))
            print(poll_score)
            poll_score = poll_score.get("party_score__sum")
            return render (request,'election_results/poll.html',{'form':form , 'poll_score':poll_score,'poll':poll})
            
                 
        else:
            form = AddPolls()

        
    return render (request,'election_results/poll.html',{'form':form})

def new_polling_unit(request):
    form = NewPollingUnit()
    if request.method == 'POST':
        form = NewPollingUnit(request.POST)
        if form.is_valid():
            f= form.save()
            f.Polling_unit = form.cleaned_data['polling_unit']
            f.party = form.cleaned_data['party']
            f.party_score = form.cleaned_data['party_score']
            
            form.save()

            messages.success(request, f'A new polling unit has been !')
            
    else: 
        form = NewPollingUnit()

    return render(request, 'election_results/new_poll.html',{'form':form})
def display(request):
    results =  New_Polling_unit.objects.all()
    context = {'results':results}

    return render (request, 'election_results/display.html',context)
            
def collate_results(request, voting_category):
    parties = Party.objects.all()
    results = []
    for party in parties:
        result_store = {}
        polling_units = New_Polling_unit.objects.filter(party=party,voting_category__category_name=voting_category)

        score = polling_units.aggregate(Sum("party_score"))
        print(score.get("party_score__sum"))
        result_store["partyname"] = party.partyname
        result_store["party_score"] = score.get("party_score__sum")

        results.append(result_store)
    print(results)

    
    # for r in results:
    #     print(r.pu_results.all())
    return render(request, 'election_results/test.html',{"results": results,'voting_category':voting_category})