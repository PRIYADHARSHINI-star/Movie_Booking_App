from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from authentication.models import Register,Movie3
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import hashlib
import datetime

def home(request):
    movies = Movie3.objects.all()
    movie_data = [{'ID':movie.id, 'Movie_Name': movie.Movie_Name, 'URL': movie.URL,'Theatre_Name':movie.Theatre_Name,'Theatre_Location':movie.Theatre_Location,'Release_Date':movie.Release_Date} for movie in movies]  # Extract movie names
    return render(request, 'authentication/home.html', {'movie_data': movie_data})

# Create your views here.
def login(request,movie_name):
    if request.method == "POST":
        Email_id = request.POST['mail']
        pswrd = request.POST['pswrd']
        salt="5gz"
        pass1 = pswrd+salt
        hashed1 = hashlib.md5(pass1.encode())
        decrypt_pass = hashed1.hexdigest()
        register_user = Register.objects.filter(Email=Email_id, Password=decrypt_pass)
        if register_user:
            print(movie_name)
            return render(request,'authentication/Seats.html', {'selected_movie_name': movie_name})
        else:
            return render(request,'authentication/login.html',{'selected_movie_name': movie_name})
    return render(request,'authentication/login.html',{'selected_movie_name': movie_name})

def register(request,movie_name):
    if request.method=="POST":
        username = request.POST['username']
        mail = request.POST['mail_id']
        pswrd = request.POST['password']
        confirm = request.POST['confirm']
        if pswrd==confirm:
            salt = "5gz"
            dataBase_password = pswrd+salt
            hashed = hashlib.md5(dataBase_password.encode())
            crypted_pass = hashed.hexdigest()
            ins1 = Register(Username=username, Email = mail, Password = crypted_pass, Confirm_Password = crypted_pass)
            ins1.save()
            print("Data saved to db")
        else:
            print("Enter password properly")
    return render(request,'authentication/register.html',{'selected_movie_name': movie_name})

def Seats(request,movie_name):
    print(movie_name)
    return render(request,'authentication/Seats.html', {'selected_movie_name': movie_name})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie3, id=movie_id)
    selected_movie_name = movie.Movie_Name
    request.session['selected_movie_name'] = selected_movie_name
    return render(request, 'authentication/movie_detail.html', {'movie': movie})

def set_session_data(request):
    if request.method == "POST":
        movie_name = request.POST.get('movieName')
        total_amount = request.POST.get('totalAmount')
        total_seats = request.POST.get('selectedSeatsCount')

        print(f"Movie Name: {movie_name}")
        print(f"Total Amount: {total_amount}")
        print(f"Total Seats: {total_seats}")

        request.session['movie_name'] = movie_name  # Store movie_name in the session
        request.session['total_amount'] = total_amount
        request.session['selectedSeatsCount'] = total_seats
        return JsonResponse({'message': 'Session data set successfully'})

def report(request):
    # Retrieve the values from Local Storage or session
    #selectedSeatsCount = request.session.get('selectedSeatsCount')
    movie_name = request.session.get('movie_name')
    #totalAmount = request.session.get('totalAmount')
    
    # print(movie_name)
    # # Check if the values exist in the session
    # if not (selectedSeatsCount and movie_name and totalAmount):
    #     # Handle the case where the values are missing
    #     return HttpResponse("Booking details are missing")

    # # Send the email
    # subject = 'Booking Details'
    # message = f'Thank you for booking {selectedSeatsCount} seats for the movie {movie_name}. Your total amount is ${totalAmount}.'
    # from_email = settings.EMAIL_HOST_USER  # Your email address
    # recipient_list = ['recipient@example.com']  # The recipient's email address

    # send_mail(subject, message, from_email, recipient_list)

    return render(request, 'authentication/report.html', {'selected_movie_name': movie_name})
def send_email(request):
    if request.method == 'POST':
        selected_movie_name = request.POST.get('selected_movie_name')
        selected_seats_count = request.POST.get('selected_seats_count')
        total_amount = request.POST.get('total_amount')

        # Customize your email subject and message here
        subject = 'Booking Confirmation - Cinemax Cinema'
        message = f'Dear User,\n We are delighted to confirm your booking for an exciting movie experience at Cinemax Cinema. Your booking details are as follows:\n\t Movie: {selected_movie_name}, \n\tNumber of Tickets: {selected_seats_count},\n\tTotal Amount: ${total_amount},\n Please arrive at the cinema at least 30 minutes before the showtime to ensure a smooth and enjoyable experience. You can pick up your tickets at the box office by presenting your booking ID or the email confirmation.\nWe look forward to welcoming you to Cinemax Cinema. If you have any questions or need further assistance, please do not hesitate to contact our customer support team at [Cinemax@cine.com] or [+91 9293920129].\nThank you for choosing Cinemax Cinema for your entertainment needs. Enjoy the show!\nBest regards,\nThe Cinemax Cinema Team'
        #message = f'Thank you for booking {selected_seats_count} seats for the movie {selected_movie_name}. Your total amount is ${total_amount}.'

        # Customize sender, recipient, and other email settings as needed
        from_email = 'sender@example.com'
        recipient_list = ['harryragav008@gmail.com']

        try:
            # Send the email
            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return JsonResponse({'success': False, 'error_message': 'Invalid request'})
