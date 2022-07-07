import nltk
from django.shortcuts import render

 
def gender_features(name):
    features = {}
 
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
 
    features["first_three_letter"] = name[:3].lower()
    features["last_three_letter"] = name[-3:].lower()
 
    return features
 
def index(request):
    message = ''
    if request.method == 'POST':
        input_name = request.POST.get("name", "")
 
        if input_name != '':
            
 
            from nltk.corpus import names
 
            # Prepare the label for each name
            labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
 
            import random
            random.shuffle(labeled_names)
 
            # Generate the training set and test set
            feature_set = [(gender_features(n), gender) for (n, gender) in labeled_names]
            train_set = feature_set[:3000]
            test_set = feature_set[3000:]
 
            classifier = nltk.NaiveBayesClassifier.train(train_set)
 
            message = input_name + " is probably " + classifier.classify(gender_features(input_name)) + ". (accuracy : " + str(round(nltk.classify.accuracy(classifier, test_set) * 100, 2)) + "%)"
        else:
            message = "Name cannot be empty!"
 
    context = {'message': message}
    return render(request, 'NameClassification/form.html', context)