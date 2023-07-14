from django.shortcuts import render
#from .models import AnnouncedPUResult

def polling_unit_result(request):
    #results = AnnouncedPUResult.objects.filter(polling_unit__polling_unit_id=polling_unit_id)
    # You can also join the PollingUnit model to get additional information about the polling unit if needed
    polling_unit_id = request.GET.get('polling_unit_id')
    results = None

    if polling_unit_id:
        results = [{"party_score": 400, "party_abbreviation": "APC"}]

    return render(request, 'polling_unit_result.html', {'results': results, 'polling_unit_id': polling_unit_id})

def homepage(request):
    return render(request, 'home.html')

def summed_total_result(request):
    #local_govts = PollingUnit.objects.values('lga_id', 'lga__lga_name').distinct()
    local_govts =  [{"id": 1, "lga_name": "Asa"}, {"id": 2, "lga_name": "Sed"}, {"id": 3, "lga_name": "Asa2"}]
    selected_lga_id = request.GET.get('local_govt')
    result = None
    selected_lga = None

    if selected_lga_id:
        #selected_lga = PollingUnit.objects.filter(lga_id=selected_lga_id).first()
        selected_lga = {"id": 1, "lga_name": "Asa"}
        if selected_lga:
            #result = AnnouncedPUResult.objects.filter(polling_unit__lga_id=selected_lga_id).values('party_abbreviation').annotate(score_sum=models.Sum('party_score'))
            result = [{'party_abbreviation': "APC", 'score_sum': 5000}, {'party_abbreviation': "LP", 'score_sum': 5400}, {'party_abbreviation': "PDP", 'score_sum': 5700}]
            result = {res['party_abbreviation']: res['score_sum'] for res in result}

    return render(request, 'local_govt_result.html', {'local_govts': local_govts, 'result': result, 'selected_lga': selected_lga})

def store_polling_unit_result(request):
    if request.method == 'POST':
        polling_unit_id = request.POST.get('polling_unit_id')
        ward_id = request.POST.get('ward_id')
        lga_id = request.POST.get('lga_id')

        # Save the new polling unit details to the database
        polling_unit = PollingUnit.objects.create(
            polling_unit_id=polling_unit_id,
            ward_id=ward_id,
            lga_id=lga_id
            # Add other fields as per your table structure
        )

        # Save the results for all parties
        parties = Party.objects.all()
        for party in parties:
            party_score = request.POST.get(party.partyid)
            AnnouncedPUResult.objects.create(
                polling_unit=polling_unit,
                party_abbreviation=party.partyid,
                party_score=party_score,
                entered_by_user='admin',  # Set the user who entered the data
                # Add other fields as per your table structure
            )

        return redirect('success')  # Redirect to a success page

    else:
        parties = [{"partyid": 1, "partyname": "PDP"}, {"partyid": 2, "partyname": "DPP"}, {"partyid": 3, "partyname": "ACN"}, {"partyid": 4, "partyname": "PPA"}, {"partyid": 5, "partyname": "CDC"}]
        return render(request, 'new_polling_unit.html', {'parties': parties})
