from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import user_info
from polls.models import movies
# Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'login.html')
        

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User Created')
                return render(request, 'info.html')
        else:
            messages.info(request, 'Passwords Not Matching..')
            return redirect('register')
    return render(request, 'register.html')

def info(request):
    if request.method == 'POST':
        user = user_info()
        user.user_name = request.POST['user_name']
        user.fav_genre = request.POST['fav_genre']
        user.fav_actor = request.POST['fav_actor']
        user.fav_actress = request.POST['fav_actress']
        user.save()

    return redirect('login')





def logout(request):
    auth.logout(request)
    return redirect('/')

def userprofile(request):
    return render(request, 'userprofile.html')




def recommend(obj):
    print(obj)
    cinemas=movies.objects.all().values()
    for cinema in cinemas:
        cinema['bayes'] = ((cinema['Rating_average'] * cinema['Rating_Count']) + (350)) / (cinema['Rating_Count'] * 100)

    df1 = movies.objects.filter(Genres = obj[0]).values()
    df2 = movies.objects.filter(Actor = obj[1]).values()
    df3 = movies.objects.filter(Actress = obj[2]).values()

    simi_score= [[0] * 3 for i in [1] * 5]
    # simi_score[0][1] = 1
    cnt = 1
    it = iter(cinemas)
    for i in simi_score:
        i[0] = cnt
        x = next(it, None)
        # print(x)
        i[2] = x['bayes']
        cnt+=1

    for df in df1:
        # print(df)
        simi_score[df['id']-1][1]+=4
    for df in df2:
        simi_score[df['id']-1][1]+=3
    for df in df3:
        simi_score[df['id']-1][1]+=3
    
    # print(simi_score)
    # Sorting the list acc to its score

    def Sort(sub_li):
        sub_li.sort(reverse=True, key = lambda x: x[1])
        return sub_li

    simi_score = Sort(simi_score)

    movies_list= [[0] * 3 for i in [1] * 3]
    for i in range(3):
        movies_list[i] = simi_score[i]
    
    def sort_bayes(sub_li):
        sub_li.sort(reverse=True, key = lambda x: x[2])
        return sub_li
    
    movies_list = sort_bayes(movies_list)
    print(movies_list)

    return movies_list
    



