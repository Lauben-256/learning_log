from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

# Custom Functions
""" Check if user associated with a topic matches the currently logged-in user """
def check_topic_owner(request, id):
    topic = Topic.objects.get(pk = id)
    if topic.owner != request.user:
        raise Http404

def index(request):
    """ The homepage for Learning  Log """
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """ Show all topics """ 
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {
        'topics' : topics
    }
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, id):
    """ Show a single topic and all its entries. """
    topic = Topic.objects.get(pk = id)
    # Make sure the topic belongs to the current user.
    """
    if topic.owner != request.user:
        raise Http404
    """
    check_topic_owner(request, id)

    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic' : topic,
        'entries' : entries,
    }
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """ Add a new topic """
    if request.method == 'GET':
        # No data submitted; create a blank form. 
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """ Add a new entry for a particular topic """
    topic = Topic.objects.get(pk = topic_id)
    
    # Check if the topic to add an entry belongs to the currently logged in user. 
    check_topic_owner(request, topic_id)

    if request.method != 'POST':
        # No data submitted, create a blank form. 
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    # Edit an existing entry
    entry = Entry.objects.get(pk = entry_id)
    topic = entry.topic
    """
    if topic.owner != request.user:
        raise Http404
    """
    check_topic_owner(request, entry_id)

    if request.method != 'POST':
        # Initital request; pre-fill form with the current entry.
        form = EntryForm(instance = entry)
    else:
        # POST data submitted, process data.
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)