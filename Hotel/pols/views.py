from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView
from datetime import datetime, timedelta
from django.db.models import Count, Min
from .forms import *
from .models import *
from django import forms

def index(request, title='/'):
    arrival = datetime.now().strftime("%Y-%m-%d")
    departure = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")
    people = '1 взрослый'
    try:
        if request.method == 'POST':
            print(request.POST['arrival'])
            print(request.POST['departure'])
            if request.POST['arrival'] != '':
                arrival = request.POST['arrival']
            if request.POST['departure'] != '':
                departure = request.POST['departure']
            if request.POST['people'] != '':
                people = f"{request.POST['people']} взрослый"
    except:
        print('123')
    supet_title = '/'
    log_in_people = 3
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/index.html', {'log_in_people': log_in_people, 'arrival': arrival, 'departure': departure, 'people': people})
        else:
            return render(request, 'pols/index.html',{'arrival': arrival, 'departure': departure, 'people': people})

    if request.method == 'POST':
        if 'register' in request.POST:
            user_form = SignUpForm
            if user_form.is_valid:
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    User = get_user_model()
                    user = User.objects.create_user(email=email, password=password)
                # profile = Profile.objects.create(user=user, email=email)
                else:
                    return redirect('index')
            return redirect('index')

        # else:
        #     return render(request, 'pols/filter.html')

        elif 'login' in request.POST:
            user_form = SignInForm(data=request.POST)
            if user_form.is_valid:
                print('lol')
                user = authenticate(email=request.POST.get('email_aut'), password=request.POST.get('password_aut'))
                if user is not None:
                    login(request, user)
                    return redirect('index')
                    # return redirect('index')
        elif 'search' in request.POST:
            print('123')
            print(request.POST['city'])
            if request.POST['city'] != '':
                return redirect('offers_city', city=request.POST['city'], arrival=arrival,
                                departure=departure, people=people)
            else:
                return redirect('offers_city', city='Москва', arrival=arrival, departure=departure, people=people)
            return redirect('offers_city', city=request.POST['city'], arrival=request.POST['arrival'], departure=request.POST['departure'], people=f"{request.POST['people']} взрослый")

    else:
        return render(request, 'pols/index.html', {'arrival': arrival, 'departure': departure, 'people': people})

def offers(request, city, arrival, departure, people, orderby='Сортировка'):
    rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city))
    log_in_people = 3
    if orderby == 'Сначала недорогие':
        rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city)).order_by('price_per_night')
    elif orderby == 'Сначала дорогие':
        rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city)).order_by('-price_per_night')
    print(Hotel.objects.all().filter(city=city))
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/filter.html', {'log_in_people': log_in_people, 'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'people':people, 'orderby': orderby})
        else:
            return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'people':people, 'orderby': orderby})

    if request.method == 'POST':
        if 'register' in request.POST:
            user_form = SignUpForm
            if user_form.is_valid:
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    User = get_user_model()
                    user = User.objects.create_user(email=email, password=password)
                # profile = Profile.objects.create(user=user, email=email)
                else:
                    return redirect('offers')
            return redirect('offers')
        # else:
        #     return render(request, 'pols/filter.html')

        elif 'login' in request.POST:
            user_form = SignInForm(data=request.POST)
            if user_form.is_valid:
                print('lol')
                user = authenticate(email=request.POST.get('email_aut'), password=request.POST.get('password_aut'))
                if user is not None:
                    login(request,user)
                    return redirect('offers_city', city=city, arrival=arrival, departure=departure, people=people)
                    # return redirect('index')
            else:
                return redirect('offers')

        elif 'search' in request.POST:
            return redirect('offers_city', city=request.POST['city'], arrival=request.POST['arrival'], departure=request.POST['departure'], people=request.POST['people'])

        elif 'filter_btn' in request.POST:
            # print(request.POST['min_price'])
            # print(request.POST['max_price'])
            # print(request.POST['star'])
            #print(Hotel.objects.all().filter(stars=request.POST['star']))
            # rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city), price_per_night__range=(request.POST['min_price'], request.POST['max_price']))
            if request.POST['star']:
                if request.POST['min_price'] and request.POST['max_price']:
                    if request.POST['star']:
                        rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city), price_per_night__range=(request.POST['min_price'], request.POST['max_price'])).filter(hotel__in=Hotel.objects.all().filter(stars=request.POST['star']))
                    else:
                        rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city),
                                                           price_per_night__range=(
                                                           request.POST['min_price'], request.POST['max_price']))
                else:
                    rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city)).filter(hotel__in=Hotel.objects.all().filter(stars=request.POST['star']))
            if request.user.is_authenticated:
                return render(request, 'pols/filter.html', {'log_in_people': log_in_people, 'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'people':people, 'orderby': orderby})
            else:
                return render(request, 'pols/filter.html',
                              {'rooms': rooms, 'city': city, 'arrival': arrival, 'departure': departure,
                               'people': people, 'orderby': orderby})

    else:
        return render(request, 'pols/filter.html')

def favorites(request, city=None):
    favorites = Favorites.objects.all().filter(user=request.user)
    cities = Hotel.objects.filter(id__in=favorites.values_list('hotel_id', flat=True)).values('city').annotate(count=Count('id')).values_list('city', flat=True)
    # cities = Hotel.objects.all().values('city').annotate(count=Count('id')).values_list('city', flat=True)
    # print(Hotel.objects.all().values('city').annotate(count=Count('id')).values_list('city', flat=True))
    print(cities)
    if city is not None:
        favorites = Favorites.objects.all().filter(user=request.user, hotel__in=Hotel.objects.all().filter(city=city))
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/favorites.html', {'favorites': favorites, 'cities': cities})
        else:
            return redirect(request.META.get('HTTP_REFERER'))

    if request.POST:
        if 'delite' in request.POST:
            Favorites.objects.filter(id=request.POST['delite']).delete()

    return render(request, 'pols/favorites.html', {'favorites': favorites, 'cities': cities})

def travel_history(request):
    arrival = datetime.now().strftime("%Y-%m-%d")
    departure = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")
    people = '1 взрослый'

    bookings = Booking.objects.all().filter(user=request.user)
    print(bookings)
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/history.html', {'bookings': bookings, 'arrival': arrival, 'departure':departure, 'people':people})
        return redirect(request.META.get('HTTP_REFERER'))


class PostDetailView(DetailView):
    model = Hotel
    context_object_name = 'object'
    fields = '__all__'
    template_name = 'pols/hotel.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['hotels']=[self.get_object()]
        return context

    def get_object(self, queryset=None):
        return Hotel.objects.get(id=self.kwargs['id_hotel_id'])

def hotel(request, id_hotel_id, arrival, departure, people):
    hotels = Hotel.objects.all().filter(id=id_hotel_id)
    rooms = Rooms.objects.all().filter(hotel=id_hotel_id)
    reviews = Reviews.objects.all().filter(hotel=id_hotel_id)
    reviews_count = len(reviews)
    print(hotels)
    # print(Rooms.objects.all()

    log_in_people = 3
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'people':people})
        else:
            return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'people':people})

    if request.method == 'POST':
        if 'register' in request.POST:
            user_form = SignUpForm
            if user_form.is_valid:
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    User = get_user_model()
                    user = User.objects.create_user(email=email, password=password)
                # profile = Profile.objects.create(user=user, email=email)
                else:
                    return redirect('hotel')
            return redirect('hotel_id')

        elif 'login' in request.POST:
            user_form = SignInForm(data=request.POST)
            if user_form.is_valid:
                print('lol')
                user = authenticate(email=request.POST.get('email_aut'), password=request.POST.get('password_aut'))
                if user is not None:
                    login(request,user)
                    return render(request,'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms})
                    # return redirect('index')
            else:
                return redirect('hotel_id')
        elif 'addhotel' in request.POST:
            User = get_user_model()
            print(1)
            print(Hotel.objects.get(id=id_hotel_id))
            print(User.objects.all().filter(email=request.user))
            price = Rooms.objects.all().filter(hotel=Hotel.objects.get(id=id_hotel_id)).order_by("price_per_night")[0].price_per_night
            try:
                print(Favorites.objects.all().filter(hotel = Hotel.objects.get(id=id_hotel_id), user = request.user)[0])
            except:
                try:
                    Favorites(hotel = Hotel.objects.get(id=id_hotel_id), user = request.user, min_price = price).save()
                    return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'arrival':arrival, 'departure':departure, 'people':people})

                except:
                    return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'arrival':arrival, 'departure':departure, 'people':people})

        elif 'search' in request.POST:
            return redirect('hotel_id_hotel', id_hotel_id=id_hotel_id, arrival=request.POST['arrival'], departure=request.POST['departure'], people=request.POST['people'])
    else:
        return render(request, 'pols/hotel.html')

def order(request, id_room, arrival, departure, people):
    log_in_people = 3
    room = Rooms.objects.get(id=id_room)
    days = int(departure[8:]) - int(arrival[8:])
    total_price = room.price_per_night * days
    hotel = room.hotel.id
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/making_an_order.html', {'log_in_people': log_in_people, 'room': room, 'arrival': arrival, 'departure': departure, 'people': people, 'days': days, 'total_price': total_price, 'hotel': hotel})

    if request.method == 'POST':
        if 'register' in request.POST:
            user_form = SignUpForm
            if user_form.is_valid:
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    User = get_user_model()
                    user = User.objects.create_user(email=email, password=password)
                # profile = Profile.objects.create(user=user, email=email)
                else:
                    return redirect('order')
            return redirect('order')
        # else:
        #     return render(request, 'pols/filter.html')

        elif 'login' in request.POST:
            user_form = SignInForm(data=request.POST)
            if user_form.is_valid:
                print('lol')
                user = authenticate(email=request.POST.get('email_aut'), password=request.POST.get('password_aut'))
                if user is not None:
                    login(request, user)
                    return render(request, 'pols/making_an_order.html', {'log_in_people': log_in_people})
                    # return redirect('index')
            else:
                return redirect('order')
    else:
        return render(request, 'pols/making_an_order.html')

def payments(request, id_room, arrival, departure, people):
    room = Rooms.objects.get(id=id_room)
    days = int(departure[8:]) - int(arrival[8:])
    total_price = room.price_per_night * days
    people = people[:10]
    people_f = int(''.join(filter(str.isdigit, people)))
    print(''.join(filter(str.isdigit, people)))
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/payments.html', {'room': room, 'arrival': arrival, 'departure': departure, 'people': people, 'total_price': total_price})
    if request.method == 'POST':
        if len(request.POST['number_card']) == 19 and len(request.POST['cvv_card']) == 3:
            Booking.objects.create(quantity_people=people_f, arrival=arrival, departure=departure, price_per_room=total_price, user=request.user, room=room)
            return redirect('index')
        else:
            print('lox')
            return render(request, 'pols/payments.html',
                          {'room': room, 'arrival': arrival, 'departure': departure, 'people': people,
                           'total_price': total_price})

        print(len(request.POST['number_card']))
        print(request.POST['date_card'])
        print(request.POST['cvv_card'])

def successful_payment(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/successfully.html')

# def registrarion(request):
    # if request.method == 'POST':
    #     user_form = SignUpForm
    #     if user_form.is_valid():
    #         user_form.save()
    #     return redirect('index')