from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

@login_required
def feedback_submission(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback-thanks')
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})

@login_required
def feedback_thanks(request):
    return render(request, 'feedback_thanks.html')