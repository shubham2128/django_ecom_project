from django.shortcuts import render
import pickle
from .forms import UserIDForm
from .utils import get_recommendations
from .utils import settings
# Load the trained model from pickle file
with open(settings.MODEL_FILE, 'rb') as f:
    algo_knn_user = pickle.load(f)

def home(request):
    form = UserIDForm()
    return render(request,'home.html', {'form': form})

def recommendations(request):
    form = UserIDForm(request.POST or None)  # Create form instance whether the request is POST or not

    if request.method == 'POST':
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            print("User ID from form:", user_id)  # Debug print to check user_id
            recommendations = get_recommendations(user_id)
            return render(request, 'recommendations.html', {'recommendations': recommendations})
    
    # If request method is not POST or form is not valid, render home page with form
    return render(request, 'home.html', {'form': form})


