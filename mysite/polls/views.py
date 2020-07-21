
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice
from django.http import HttpResponse
import json
from .models import Question
from .models import TestModel

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be
        published in the future)."""
        
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]
    

    
def demoform(request):
    if request.method == "POST":
        list_key = []
        list_value = []
        for key, value in request.POST.items():
                list_key.append(key)
                list_value.append(value)
    #            print('Key: %s' % (key) ) 
    # print(f'Key: {key}') in Python >= 3.7
    #            print('Value %s' % (value) )
    # print(f'Value: {value}') in Python >= 3.7
    #    html = "<html><body>It is Key %s and Value </body></html>" % (key)
    #    return HttpResponse(html)
    
    for key, value in request.POST.items():
        TestModel(field_1=key, field_2=value).save()
    #       batch_colc=t[2], batch_cold=t[3],
    #       batch_cole=t[4]).save()
    #aList = [(headline=val) for val in list_key]
    #Entry.objects.bulk_create(aList)

    #orm_bulk_create(list_key)    
    #html="<html> <body> <ul> <li> Questions %s</li>  <li> Answers %s </li> </ul> </body>  </html>"  %(list_key,list_value)   
    html="<html><body> Thank you for taking the time to complete this survey. </body></html>"
    #json_stuff = json.dumps({"list_of_jsonstuffs" : list_key}) 
    #json_output = json.dumps({ {'question': country, 'answer': wins} for country, wins in zip(list_key, list_value)})   
    #return HttpResponse(json_output, content_type ="application/json")
    return HttpResponse(html)                

class DetailView(generic.DetailView):
    model = Question
    #question_list = Question.objects
    template_name = 'polls/detail.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """Return all published questions (not including those set to be
        published in the future)."""
        
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


#from app import models


def orm_bulk_create(n_records):
    instances = [
        models.TestModel(
            field_1=i,
            field_2=str(i),
            field_3=timezone.now(),
        )
        for i in xrange(0, n_records)
    ]

    models.TestModel.objects.bulk_create(instances)


if __name__ == '__main__':
    utils.timed(orm_bulk_create)

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    #output = ', '.join([q.question_text for q in latest_question_list])
#    #return HttpResponse(output)
#    context = {'latest_question_list': latest_question_list}
#    return render(request, 'polls/index.html', context)


#def index(request):
#    return HttpResponse("You are at a survey website")

#def detail(request, question_id):
    
#    return HttpResponse(" You are looking at the question %s." % question_id)

#def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question': question})    

#def results(request, question_id):
#    #response="You are lookign at the result of the question %s. "
#    #return HttpResponse(response % question_id)
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.vote += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
# Create your views here.
