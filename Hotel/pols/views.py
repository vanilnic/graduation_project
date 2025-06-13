from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView
from datetime import datetime, timedelta
from django.db.models import Count, Min, Avg
from .forms import *
from .models import *
from django import forms
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse

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
                    try:
                        user = User.objects.create_user(email=email, password=password)
                        return render(request, 'pols/index.html', {'arrival':arrival, 'departure':departure, 'people':people, 'done_register': '1'})
                    except:
                        return render(request, 'pols/index.html', {'arrival':arrival, 'departure':departure, 'people':people, 'error_register': 'Данный пользователь существует!'})
                else:
                    return  render(request, 'pols/index.html', {'arrival':arrival, 'departure':departure, 'people':people, 'error_register': 'Пароли не совпадают!'})
            return redirect('index')

        elif 'login' in request.POST:
            user_form = SignInForm(data=request.POST)
            if user_form.is_valid:
                print('lol')
                user = authenticate(email=request.POST.get('email_aut'), password=request.POST.get('password_aut'))
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'pols/index.html', {'arrival':arrival, 'departure':departure, 'people':people, 'error_login': 'Неверные логин или пароль!'})

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

    arrival_now = datetime.now().strftime("%Y-%m-%d")
    departure_now = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")

    if orderby == 'Сначала недорогие':
        rooms = rooms.order_by('price_per_night')
    elif orderby == 'Сначала дорогие':
        rooms = rooms.order_by('-price_per_night')
    print(Hotel.objects.all().filter(city=city))
    
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/filter.html', {'log_in_people': log_in_people, 'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'orderby': orderby})
        else:
            return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now,'people':people, 'orderby': orderby})

    if request.method == 'POST':
        if 'register' in request.POST:
            user_form = SignUpForm
            if user_form.is_valid:
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    User = get_user_model()
                    try:
                        user = User.objects.create_user(email=email, password=password)
                        return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now,'people':people, 'orderby': orderby, 'done_register': '1'})
                    except:
                        return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now,'people':people, 'orderby': orderby, 'error_register': 'Данный пользователь существует!'})
                # profile = Profile.objects.create(user=user, email=email)
                else:
                    return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now,'people':people, 'orderby': orderby, 'error_register': 'Пароли не совпадают!'})

            return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now,'people':people, 'orderby': orderby})

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
                else:
                    return render(request, 'pols/filter.html', {'rooms': rooms, 'city':city, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now,'people':people, 'orderby': orderby, 'error_login': 'Неверные логин или пароль!'})
            else:
                return redirect('offers')

        elif 'search' in request.POST:
            return redirect('offers_city', city=request.POST['city'], arrival=request.POST['arrival'], departure=request.POST['departure'], people=request.POST['people'])

        elif 'filter_btn' in request.POST:
            min_price = request.POST.get('min_price')
            max_price = request.POST.get('max_price')
            star = request.POST.get('star', '')
            
            min_price = request.POST.get('min_price', '')
            max_price = request.POST.get('max_price', '')

            orderby = request.POST.get('orderby', 'Сортировка')

            try:
                filter_min = int(min_price) if min_price else 0
            except ValueError:
                filter_min = 0

            try:
                filter_max = int(max_price) if max_price else 100000
            except ValueError:
                filter_max = 100000
            #print(Hotel.objects.all().filter(stars=request.POST['star']))
            # rooms = Rooms.objects.all().filter(hotel__in=Hotel.objects.all().filter(city=city), price_per_night__range=(request.POST['min_price'], request.POST['max_price']))
            rooms = Rooms.objects.filter(
                hotel__city=city,
                price_per_night__gte=filter_min,
                price_per_night__lte=filter_max
            )

            if star is not None and star != '':
                rooms = rooms.filter(hotel__stars=star)

            if orderby == 'Сначала недорогие':
                rooms = rooms.order_by('price_per_night')
            elif orderby == 'Сначала дорогие':
                rooms = rooms.order_by('-price_per_night')

            context = {
                'rooms': rooms,
                'city': city,
                'arrival': arrival,
                'departure': departure,
                'people': people,
                'orderby': orderby,
                'min_price': min_price, 
                'max_price': max_price,
                'star': star,
                'arrival_now':arrival_now, 
                'departure_now':departure_now
            }

            if request.user.is_authenticated:
                context['log_in_people'] = log_in_people

            return render(request, 'pols/filter.html', context)
    else:
        return render(request, 'pols/filter.html')

def favorites(request, city=None):
    arrival = datetime.now().strftime("%Y-%m-%d")
    departure = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")
    people = '1 взрослый'

    referer = request.META.get('HTTP_REFERER', '')
    if 'favorites' not in referer:
        request.session['favorites_back_url'] = referer

    if not request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    favorites = Favorites.objects.filter(user=request.user)

    cities = Hotel.objects.filter(id__in=favorites.values_list('hotel_id', flat=True)) \
        .values_list('city', flat=True).distinct()

    if city:
        favorites = favorites.filter(hotel__city=city)

    if request.method == 'POST' and 'delite' in request.POST:
        Favorites.objects.filter(id=request.POST['delite']).delete()
        return redirect(request.path_info) 

    return render(request, 'pols/favorites.html', {
        'favorites': favorites,
        'cities': cities,
        'arrival': arrival,
        'departure': departure,
        'people': people,
        'selected_city': city,
        # 'formatted': formatted,
        'back_url': request.session.get('favorites_back_url', '/') 
    })

def travel_history(request):
    arrival = datetime.now().strftime("%Y-%m-%d")
    departure = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")
    people = '1 взрослый'

    bookings = Booking.objects.all().filter(user=request.user).order_by('-arrival')
    bookings_new = []
    for booking in bookings:
        arrival_cancel = datetime.strftime(booking.arrival, "%Y-%m-%d")
        if arrival_cancel < arrival:
            disable_btn_cancel = "true"
        else:
            disable_btn_cancel = "false"
        bookings_new.append({
            'id': booking.id,
            'room_img1': booking.room.img1,
            'room_img2': booking.room.img2,
            'room_img3': booking.room.img3,
            'room_id': booking.room.id,
            'room_hotel_name': booking.room.hotel.name,
            'room_hotel_stars': booking.room.hotel.stars,
            'room_hotel_id': booking.room.hotel.id,
            'room_hotel_CSI': booking.room.hotel.CSI,
            'room_hotel_address': booking.room.hotel.address,
            'arrival': booking.arrival,
            'departure': booking.departure,
            'room_title': booking.room.title,
            'price_per_room': booking.price_per_room,
            'disable_btn_cancel': disable_btn_cancel
        })

    reviewed_booking_ids = Reviews.objects.filter(booking__in=bookings).values_list('booking_id', flat=True)

    if request.method == 'POST':
        if 'delete' in request.GET:
            Booking.objects.filter(id=request.GET.get("delete")).delete()
            return redirect("travel_history")
        if request.user.is_authenticated:
            booking_id = request.POST.get('booking_id')

            booking = get_object_or_404(Booking, id=booking_id, user=request.user)
            existing_review = Reviews.objects.filter(booking=booking).first()
            
            if existing_review:
                return redirect("index")
            else:
                Reviews.objects.create(
                    booking=booking,
                    hotel=booking.room.hotel,
                    stars=int(request.POST.get("rating")),
                    location=int(request.POST.get("location")),
                    сleanliness=int(request.POST.get("cleanliness")),
                    price_quality=int(request.POST.get("comfort")),
                    service=int(request.POST.get("staff")),
                    wifi=int(request.POST.get("value")),
                    comments=request.POST.get("comment")
                )
                hotel_id = booking.room.hotel

                averages = Reviews.objects.filter(hotel_id=hotel_id).aggregate(stars_avg=Avg('stars'))
                formatted = round(averages['stars_avg'], 1)

                print(formatted)

                try:
                    hotel_id.CSI = formatted
                    hotel_id.save()
                    print('Сохранилось')
                except Exception as e:
                    print('Ошибка при сохранении CSI:', e)


                return redirect('travel_history')
        return render(request, 'pols/history.html', {'bookings': bookings_new, 'arrival': arrival, 'departure':departure, 'people':people, 'reviewed_booking_ids':reviewed_booking_ids})

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/history.html', {'bookings': bookings_new, 'arrival': arrival, 'departure':departure, 'people':people, 'reviewed_booking_ids':reviewed_booking_ids})
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
    reviews = Reviews.objects.all().filter(hotel=id_hotel_id).order_by('-id')
    reviews_count = len(reviews)\

    arrival_now = datetime.now().strftime("%Y-%m-%d")
    departure_now = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")

    averages = Reviews.objects.filter(hotel_id=id_hotel_id).aggregate(
    stars_avg=Avg('stars'),
    location_avg=Avg('location'),
    cleanliness_avg=Avg('сleanliness'),
    price_quality_avg=Avg('price_quality'),
    service_avg=Avg('service'),
    wifi_avg=Avg('wifi')
    )
    print(averages)

    formatted = {
    'stars': round(averages['stars_avg'], 1) if averages['stars_avg'] else 0,
    'location': int(round(averages['location_avg'] * 10)) if averages['location_avg'] else 0, 
    'cleanliness': int(round(averages['cleanliness_avg'] * 10)) if averages['cleanliness_avg'] else 0,
    'price_quality': int(round(averages['price_quality_avg'] * 10)) if averages['price_quality_avg'] else 0,
    'service': int(round(averages['service_avg'] * 10)) if averages['service_avg'] else 0,
    'wifi': int(round(averages['wifi_avg'] * 10)) if averages['wifi_avg'] else 0,
    }

    print(formatted)

    favorite_id = None
    if request.user.is_authenticated:
        fav = Favorites.objects.filter(hotel_id=id_hotel_id, user=request.user).first()
        if fav:
            favorite_id = fav.id
        is_favorite = fav is not None
    else:
        is_favorite = False

    log_in_people = 3
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted})
        else:
            return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted})

    if request.method == 'POST':
        if 'register' in request.POST:
            user_form = SignUpForm
            if user_form.is_valid:
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if password == password2:
                    User = get_user_model()
                    try:
                        user = User.objects.create_user(email=email, password=password)
                        return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted, 'done_register': '1'})
                    except:
                        return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted, 'error_register': 'Данный пользователь существует!'})
                else:
                    return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted, 'error_register': 'Пароли не совпадают!'})

            return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted})

        elif 'login' in request.POST:
            user_form = SignInForm(data=request.POST)
            if user_form.is_valid:
                print('lol')
                user = authenticate(email=request.POST.get('email_aut'), password=request.POST.get('password_aut'))
                if user is not None:
                    login(request,user)
                    return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted})
                else:
                    return render(request, 'pols/hotel.html', {'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'reviews': reviews, 'reviews_count': reviews_count, 'arrival':arrival, 'departure':departure, 'arrival_now':arrival_now, 'departure_now':departure_now, 'people':people, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted, 'error_login': 'Неверные логин или пароль!'})
            else:
                return redirect('hotel_id')
        elif 'addhotel' in request.POST:
            User = get_user_model()
            # print(1)
            # print(Hotel.objects.get(id=id_hotel_id))
            # print(User.objects.all().filter(email=request.user))
            price = Rooms.objects.all().filter(hotel=Hotel.objects.get(id=id_hotel_id)).order_by("price_per_night")[0].price_per_night
            try:
                print(Favorites.objects.all().filter(hotel = Hotel.objects.get(id=id_hotel_id), user = request.user)[0])
                return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'arrival':arrival, 'departure':departure, 'people':people, 'reviews': reviews, 'reviews_count': reviews_count, 'ratings': formatted})
            except:
                try:
                    Favorites(hotel = Hotel.objects.get(id=id_hotel_id), user = request.user, min_price = price).save()

                    fav = Favorites.objects.filter(hotel_id=id_hotel_id, user=request.user).first()
                    is_favorite = fav is not None
                    favorite_id = fav.id if fav else None

                    return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'arrival':arrival, 'departure':departure, 'people':people, 'reviews': reviews, 'reviews_count': reviews_count, 'is_favorite': is_favorite, 'favorite_id': favorite_id, 'ratings': formatted})
                except:
                    return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'arrival':arrival, 'departure':departure, 'people':people, 'reviews': reviews, 'reviews_count': reviews_count, 'ratings': formatted})

        elif 'delite' in request.POST:
            favorite_id_to_delete = request.POST.get('delite')
            if favorite_id_to_delete:
                Favorites.objects.filter(id=favorite_id_to_delete, user=request.user).delete()
            return render(request, 'pols/hotel.html', {'log_in_people': log_in_people, 'hotels': hotels, 'id_hotel_id': id_hotel_id, 'rooms': rooms, 'arrival':arrival, 'departure':departure, 'people':people, 'reviews': reviews, 'reviews_count': reviews_count, 'ratings': formatted})

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
            return redirect(reverse('index') + '?booking_success=1')
        else:
            return render(request, 'pols/payments.html',
                          {'room': room, 'arrival': arrival, 'departure': departure, 'people': people,
                           'total_price': total_price})