from django.shortcuts import render
from .models import movies
from accounts.models import user_info
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
import requests, json





# def convert(obj):
#     L = []
#     L = obj.split(" | ")
#     return L

# def convert3(obj):
#     L = []
#     L = obj.split(" | ")
#     n = len(L)
#     del L[4:n-1]
#     return L

# def stem(text):
#     y = []
#     for i in text.split():
#         y.append(ps.stem(i))
    
#     return " ".join(y)


def recommend_movie(obj):
    print(obj)
    # cinemas=pd.DataFrame(list(movies.objects.all().values()))
    cinemas=movies.objects.all().values()
    for cinema in cinemas:
        cinema['bayes'] = ((cinema['Rating_average'] * cinema['Rating_Count']) + (350)) / (cinema['Rating_Count'] * 100)
        
    for cinema in cinemas:
        if(cinema['Title'] == obj):
            movie = cinema
            break
    # cinemas['bayes'] = ((cinemas['Rating_average'] * cinemas['Rating_Count']) + (350)) / (cinemas['Rating_Count'] * 100)
    # movie_index = cinemas[cinemas['Title'] == obj].index[0]
    # movie_genre = cinemas[cinemas['Title'] == obj].index[1]
    # movie_actor = cinemas[cinemas['Title'] == obj].index[7]
    # movie_actress = cinemas[cinemas['Title'] == obj].index[8]
    # movie_pc = cinemas[cinemas['Title'] == obj].index[5]
    print(movie['Genres'])
    df1 = movies.objects.filter(Genres = movie['Genres']).values()
    df2 = movies.objects.filter(Actor = movie['Actor']).values()
    df3 = movies.objects.filter(Actress = movie['Actress']).values()
    df4 = movies.objects.filter(Production_companies = movie['Production_companies']).values()

    # it = iter(s)
	# while True:
	# 	x = next(it, None)
	# 	if not x:
	# 		break
	# 	print(x, end=' ')
    # print(df2)
    simi_score= [[0] * 3 for i in [1] * 47]
    # simi_score[0][1] = 1
    cnt = 1
    it = iter(cinemas)
    for i in simi_score:
        i[0] = cnt
        x = next(it, None)
        i[1] = 1
        # print(x)
        i[2] = x['bayes']
        cnt+=1

    for df in df1:
        simi_score[df['id']-1][1]*=4
    for df in df2:
        simi_score[df['id']-1][1]*=3
    for df in df3:
        simi_score[df['id']-1][1]*=3
    for df in df4:
        simi_score[df['id']-1][1]*=2
    
    print(simi_score)
    
    # [[1,0,bayes], [2,0,0], [3,0,0], [4,0,0]]
    # Sorting the list acc to its score

    def Sort(sub_li):
        sub_li.sort(reverse=True, key = lambda x: x[1])
        return sub_li

    simi_score = Sort(simi_score)

    movies_list= [[0] * 3 for i in [1] * 5]
    for i in range(5):
        movies_list[i] = simi_score[i]
    

    def sort_bayes(sub_li):
        sub_li.sort(reverse=True, key = lambda x: x[2])
        return sub_li
    
    movies_list = sort_bayes(movies_list)
    print(movies_list)




    # Ranking acc to its rating
    # final_list = sorted(list(enumerate(movies_list)),reverse=True,key=lambda x:x[2])[1:2]

    # print(final_list)

    return movies_list




    # # cinemas['Genres'] = cinemas['Genres'].apply(convert)
    # # cinemas['Cast'] = cinemas['Cast'].apply(convert)
    # # cinemas['Production_companies'] = cinemas['Production_companies'].apply(convert3)
    # cinemas['tags'] = cinemas['Cast'] + cinemas['Genres'] + cinemas['Production_companies']
    # cinemas['bayes'] = ((cinemas['Rating_average'] * cinemas['Rating_Count']) + (350)) / (cinemas['Rating_Count'] * 100)
    # cinemas['tags'] = cinemas['tags'].apply(stem)
    # print(cinemas['tags'])
    # cv = CountVectorizer(max_features=1000)
    # vectors = cv.fit_transform(cinemas['tags']).toarray()
    # print(vectors)
    # similarity = cosine_similarity(vectors)
    # print(similarity)
    # movie_index = cinemas[cinemas['Title'] == obj].index[0]
    # print (movie_index)
    # distances = similarity[movie_index]
    # movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:3]
    # print(movies_list)
    # return movies_list

def recommend(request):
    select_value = request.POST.get('name_of_select')
    print(select_value)
    outputs = recommend_movie(select_value)
    cinemas = movies.objects.all().values()
    movie_set = []
    for output in outputs:
        print(output[0])
        movie_set.append(cinemas[output[0]-1])
        # cnt = 0
        # for cinema in cinemas:
        #     if(output[0] == cnt):
        #         movie_set.append(cinema)
        #         break
        #     cnt+=1
    # print(cinemas)
    return render(request, 'movie.html', {'cinemas':movie_set, 'all_cinemas':cinemas} )




    




        

def index(request):
    if request.user.is_authenticated:
        cinema_list = recommend_on_choice(request.user.username)

    response=requests.get('https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=24fc270a42a445a6aaaf7522af806c61').json()
    articles = response['articles']
    for article in articles:
        first = article
        break
    
    left_articles = []
    right_articles = []
    cnt = 0
    for article in articles:
        cnt+=1
        if cnt>6:
            break
        if cnt>3:
            right_articles.append(article)
        else:
            left_articles.append(article)
        
    
    if request.user.is_authenticated:
        return render(request, 'index.html', {'left_articles':left_articles, 'first':first, 'right_articles':right_articles, 'cinema_lists':cinema_list})
    
    return render(request, 'index.html', {'left_articles':left_articles, 'first':first, 'right_articles':right_articles})

def movie(request):
    cinemas = movies.objects.all()
    print (cinemas)

    
    return render(request,'movie.html',{'cinemas':cinemas, 'all_cinemas':cinemas})

    # interns = InternCorner.objects.all()
        # return render(request,'experiences.html',{'interns':interns})


def recommend_on_choice(obj):
    users = user_info.objects.all().values()

    for user in users:
        if(user['user_name'] == obj):
            choices = user
            break
    
    print (choices)
    df1 = movies.objects.filter(Genres = choices['fav_genre']).values()
    df2 = movies.objects.filter(Actor = choices['fav_actor']).values()
    df3 = movies.objects.filter(Actress = choices['fav_actress']).values()

    cinemas=movies.objects.all().values()
    for cinema in cinemas:
        cinema['bayes'] = ((cinema['Rating_average'] * cinema['Rating_Count']) + (350)) / (cinema['Rating_Count'] * 100)

    simi_score= [[0] * 3 for i in [1] * 47]
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

    def Sort(sub_li):
        sub_li.sort(reverse=True, key = lambda x: x[1])
        return sub_li

    simi_score = Sort(simi_score)

    movies_list= [[0] * 3 for i in [1] * 5]
    for i in range(5):
        movies_list[i] = simi_score[i]
    

    def sort_bayes(sub_li):
        sub_li.sort(reverse=True, key = lambda x: x[2])
        return sub_li
    
    movies_list = sort_bayes(movies_list)

    movie_set = []
    for output in movies_list:
        print(output[0])
        movie_set.append(cinemas[output[0]-1])

    return movie_set



