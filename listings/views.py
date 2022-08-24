import datetime
from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from contacts.models import Contact,Reservation
from django.contrib import messages
# from django.contrib.auth import User
from .models import Listing
cal=[]
import calendar
class myMonthsCal:
  month_id = 0
  days_list = []
  month_name = ""
  prev_d = []

class myCalender:
  day_id = 0
  day_date = date.today()
  day_d = date.today().day
  day_m = date.today().month
  day_name = date.today().strftime('%A')
  is_free = True

from datetime import date, datetime
# month = datetime.now().date().month
# print(listing_id)
# listing = get_object_or_404(Listing, pk=listing_id)

cal=[]
def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  cal.clear()
  months_obj_list = []
  from datetime import datetime
  thisYear = datetime.now().date().year
  thisMonth = datetime.now().date().month

  reserved_days = []
  for itm in Reservation.objects.all():
    res_d = itm.day
    reserved_days.append(res_d)
    print(res_d)
  listing = get_object_or_404(Listing, pk=listing_id)
  allDaysContainer = []



  for m_I in range(thisMonth, 13):
    tempMontDays = []
    previus_d = []
    # from datetime import datetime
    num_days = calendar.monthrange(thisYear, thisMonth)[1]
    allDays = [date(thisYear, thisMonth, day) for day in range(1, num_days+1)]
    # print(days1_0)
    # break
    for day_ in allDays:
      allDaysContainer.append(day_)
      cal.append(day_)
    #   # print(date_)
    # # for i4 in days1_0:
    #   # print(i4.strftime('%A')[0:3], i4)
      day_temp = myCalender()
      day_temp.day_name = day_.strftime('%A')[0:3]
      day_temp.day_id = allDaysContainer.index(day_)
      day_temp.day_date = day_
      day_temp.day_d = day_.day
      day_temp.day_m = day_.month
      if day_ in reserved_days:
        day_temp.is_free = False
      tempMontDays.append(day_temp)
    week_days = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    f1_d = tempMontDays[0].day_name
    for dnm_ in week_days:
      if dnm_ == f1_d:
        day_index = week_days.index(dnm_)
        break
      else:
        previus_d.append(dnm_)
  # print(previus_d)
    tempMonthcal = myMonthsCal()
    import datetime
    month_num = str(thisMonth)
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    full_month_name = datetime_object.strftime("%B")
    tempMonthcal.month_name = full_month_name
    tempMonthcal.days_list = tempMontDays
    tempMonthcal.prev_d = previus_d
    tempMonthcal.month_id = thisMonth
    months_obj_list.append(tempMonthcal)
    thisMonth += 1
  # for  itm in months_obj_list:
  #   print(itm.month_name)
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing0 = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']
    days_to_reserv= request.POST.getlist('arr')
    # print(days_to_reserv,"0000000000")


    #  Check if user has made inquiry already
    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
      if has_contacted:
        messages.error(request, 'You have already made an inquiry for this listing')
        return redirect('/listings/'+listing_id)

    for i in days_to_reserv:
      dayToRes=allDaysContainer[int(i)]
      Reservation.objects.create(
        farms=listing,
        day=dayToRes,
        customer=request.user
      )
    contact = Contact(listing=listing0, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id )

    contact.save()

    # Send email
    # send_mail(
    #   'Property Listing Inquiry',
    #   'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
    #   'iprabhatdev@gmail.com',
    #   [realtor_email, 'random@gmail.com'],
    #   fail_silently=False
    # )

    messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
    return redirect('/listings/'+listing_id)

  context = {
    'listing': listing,
    'my_cal':months_obj_list
  }


  return render(request, 'listings/listing.html', context)

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)