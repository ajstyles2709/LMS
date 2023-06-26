"""
     Modification Log
     24/07 Created all the required functions with their respective work..
     26/07 wordked on the functionality and the logic
     27/07 worked on functionality enhancement...
     29/07 worked on functionality enhancement...with change in code logic in update and delete item
"""



from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import ItemRegistration, ItemUpdation, ReserveItemForm, ReleaseItemForm, userUpdateForm, PasswordChangeCustomForm
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import Item, ReserveItem
# Create your views here.


def index(request): #index page, user will see this page first..
    if request.method == "POST":
        userReg = UserCreationForm(request.POST) #On the index page, creating user..
        if userReg.is_valid():
            userReg.save()
            userReg = UserCreationForm()
            messages.success(request, "Registered Successfully! you can Log In Now..")
        else:
            userReg = UserCreationForm(request.POST)
    else:
        userReg = UserCreationForm() #on the index page showing userRegistration form for new user..
    return render(request, 'index.html', {'form': userReg})


def adminLogin(request): #function for admin to log in to admin UI..
    admForm = AuthenticationForm()
    if request.method == 'POST':
        admform = AuthenticationForm(request=request, data=request.POST)
        if admform.is_valid():
            uname = admform.cleaned_data['username']
            pw = admform.cleaned_data['password']
            uobj = User.objects.get(username=uname)
            if uobj.is_superuser: #if the user is super user then only he can log in to admin UI...
                user = auth.authenticate(request, username=uname, password=pw)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, "Successfully Logged In")
                    itemBookObj = Item.objects.filter(Quantity__gte=0,Category='Book')
                    itemCDObj = Item.objects.filter(Quantity__gte=0,Category='CD')
                    return render(request, 'Admin/adminIndex.html', {'Bookitem': itemBookObj,'CDitem':itemCDObj})
            else:
                messages.error(request, "You are not a Admin..")
                admform = AuthenticationForm(request=request, data=request.POST)
        else:
            admForm = AuthenticationForm(request=request, data=request.POST)
    else:
        admForm = AuthenticationForm()
    return render(request, 'Admin/adminLogin.html', {'form': admForm})


def AdminIndex(request): #Admin index to relocate to admin index page
    itemBookObj = Item.objects.filter(Quantity__gte=0,Category='Book')
    itemCDObj = Item.objects.filter(Quantity__gte=0,Category='CD')
    return render(request, 'Admin/adminIndex.html', {'Bookitem': itemBookObj,'CDitem':itemCDObj})


def RegisterItem(request): #Adding new item to the database..
    if request.method == 'POST':
        itemReg = ItemRegistration(data=request.POST)
        if itemReg.is_valid():
            itemReg.save()
            messages.success(request, "Item Added Successfully!")
            itemReg = ItemRegistration()
        else:
            itemReg = ItemRegistration(data=request.POST)
    else:
        itemReg = ItemRegistration() #passing initial value to form as 0000 for user understanding..
    return render(request, 'Admin/itemReg.html', {'form': itemReg})


def UpdateItem(request, itemId): #to update the Item in Database by admin only..using dynamic url...
    if request.method == 'POST':
        upitemObj = Item.objects.get(Id=itemId)
        upitemForm = ItemUpdation(request.POST, instance=upitemObj)
        if upitemForm.is_valid():
            upitemObj.save()
            messages.success(request, "Book Updated Successfully!")
            return redirect("/AdminIndex/")
        else:
            print("In Valid Book")
    else:
        upitemObj = Item.objects.get(Id=itemId) #getting the data of item to pass in the form for update..
        upitemForm = ItemUpdation(instance=upitemObj) #admin will get the same item data, to which he wants to update..
    return render(request, 'Admin/itemUpdate.html', {'form': upitemForm})


def DeleteItem(request, itemId): #to delete the item for admin only..by parameterized url..
    delitemObj = Item.objects.get(Id=itemId) #item obj to delete the asked item...
    if delitemObj not in ReserveItem.objects.all():
        delitemObj.delete()
        itemBookObj = Item.objects.filter(Quantity__gte=0,Category='Book')
        itemCDObj = Item.objects.filter(Quantity__gte=0,Category='CD')
        messages.success(request, "Item Deleted Successfully!")
        return render(request, 'Admin/adminIndex.html', {'Bookitem': itemBookObj,'CDitem':itemCDObj})
    else:
        messages.error(request, "Item is reserved by some user, You can't delete it..")
        itemBookObj = Item.objects.filter(Quantity__gte=0,Category='Book')
        itemCDObj = Item.objects.filter(Quantity__gte=0,Category='CD')
    return render(request, 'Admin/adminIndex.html', {'Bookitem': itemBookObj,'CDitem':itemCDObj})


def AdminLogout(request): #admin logiut function
    messages.success(request, "logout Successfully!")
    auth.logout(request)
    return redirect("/LoginAdm/")


def userLogin(request):  #user login function for user log in to user index...
    if request.method == 'POST':
        userForm = AuthenticationForm(request=request, data=request.POST)
        if userForm.is_valid():
            uname = userForm.cleaned_data['username']
            pw = userForm.cleaned_data['password']
            usr = auth.authenticate(request, username=uname, password=pw)
            if usr is not None:
                auth.login(request, usr)
                itemBookObj = Item.objects.filter(Quantity__gte=1,Category='Book')
                itemCDObj = Item.objects.filter(Quantity__gte=1,Category='CD')
                return render(request, 'User/userIndex.html', {'Bookitem': itemBookObj,'CDitem':itemCDObj})
            else:
                userForm = AuthenticationForm(
                    request=request, data=request.POST)
        else:
            userForm = AuthenticationForm(request=request, data=request.POST)
    else:
        userForm = AuthenticationForm() #authentication form for user login
    return render(request, 'User/userLogin.html', {'form': userForm})


def userIndex(request): #user Index function to relocate to user Index page from user actions..
    Book = 'Book'
    CD = 'CD'
    itemBookObj = Item.objects.filter(Quantity__gte=1,Category=Book)
    itemCDObj = Item.objects.filter(Quantity__gte=1,Category=CD)
    stud = request.user.id
    Check = ReserveItem.objects.filter(UserId=stud) #checking if current user having any reservations or not..
    currDate = date.today()
    passedDate = 0
    for i in Check: #for past due item...if user have some pending item whos dateofReturn is passed...
        returnDate = i.DateOfReturn #fetching date of return
        if returnDate < currDate: #if date of return is less than current date..
            passedDate=returnDate
        if returnDate >= currDate:
            currDate=returnDate
    if passedDate:
        messages.warning(request, "You have a past due Item to Return..")
    if Check:
        messages.info(request, "You have a Current due Item to Return..")
    return render(request, 'User/userIndex.html', {'Bookitem': itemBookObj,'CDitem':itemCDObj})


def reserveItem(request, itemId): #function to reserve the item...
    if request.method == 'POST':
        reserveItem = ReserveItemForm(data=request.POST)
        choice = request.POST['Category']
        Check = ReserveItem.objects.filter(UserId=request.user.id, ItemId=itemId,Category=choice) #checkin User with requested book in ReserveItem or not..If false then it will alow user to reserve the item...
        count = 0
        data = ReserveItem.objects.filter(Category=choice,UserId=request.user.id,)
        for i in data:
            count+=1
        print(count)
        if not Check: #with the help of this...
            if count < 2:
                if reserveItem.is_valid():
                    reserveItem.save()
                    itmObj = Item.objects.get(Id=itemId) #getting the Id of reserved item from item table to deduct one copy..
                    itmObj.Quantity -= 1
                    itmObj.save()
                    messages.success(request, "Item Reserved Successfully!")
                    return redirect("/Usr/userIndex")
            else:
                messages.error(request, "You can not reserve more than 2 items for same category..")
                Itmobj = Item.objects.get(Id=itemId)
                reserveItem = ReserveItemForm(instance=Itmobj, initial={'UserId': request.user.id, 'ItemId': itemId, 'Copies': 1})
        else:
            messages.error(request, "You can not reserve same Item twice..")
            Itmobj = Item.objects.get(Id=itemId)
            reserveItem = ReserveItemForm(instance=Itmobj, initial={'UserId': request.user.id, 'ItemId': itemId, 'Copies': 1})
    else:
        Itmobj = Item.objects.get(Id=itemId)
        reserveItem = ReserveItemForm(instance=Itmobj, initial={'UserId': request.user.id, 'ItemId': itemId, 'Copies': 1}) #passing intial values for the particular user
    return render(request, 'User/itemReserve.html', {'form': reserveItem})


def ReleaseItem(request, itemId): #for releasing the item with parameterized url...it helps to fetch the data for which we are asking..
    relitmObj = ReserveItem.objects.get(Id=itemId)
    if request.method == 'POST':
        itId = request.POST['ItemId']
        releaseItem = ReleaseItemForm(request.POST, instance=relitmObj)
        if releaseItem.is_valid():
            relitmObj.delete() #deleteing the resrved item from resrved table...
            itmObj = Item.objects.get(Id=itId) #getting the Id of reserved item from item table to add one copy..
            itmObj.Quantity += 1
            itmObj.save()
            messages.success(request, "Item Returned Successfully!")
            return redirect('/Usr/Reservations/')
    else:
        relitemObj = ReserveItem.objects.get(Id=itemId)
        releaseItem = ReserveItemForm(instance=relitemObj, initial={'UserId': request.user.id, 'Copies': 1, 'DateOfReturn':date.today().strftime("%Y-%m-%d")}) #passing intial values for the particular user
    return render(request, 'User/itemRelease.html', {'form': releaseItem})


def ChangePassword(request): #change Password to change user passord
    if request.method == 'POST':
        cForm = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if cForm.is_valid():
            cForm.save()
            uname = request.user.username
            pw = cForm.cleaned_data['new_password1']
            usr = auth.authenticate(request, username=uname, password=pw)
            if usr is not None:
                auth.login(request, usr)
                messages.success(request, "Password Changed Successfully!")
                return redirect("/Usr/userIndex/")
            else:
                cForm = PasswordChangeCustomForm(user=request.user, data=request.POST)
        else:
            cForm = PasswordChangeCustomForm(user=request.user, data=request.POST)
    else:
        cForm = PasswordChangeCustomForm(user=request.user) #to get the user who is requesting the change password..
    return render(request, 'User/ChangePassword.html', {'form': cForm})


def UpdateUser(request): #to update the data of the user...
    if request.method == 'POST':
        userForm = userUpdateForm(request.POST, instance=request.user)
        if userForm.is_valid():
            userForm.save()
            messages.success(request, "Profile updated Successfully!")
            return redirect("/Usr/userIndex/")
        else:
            print("Invalid Student")
            userForm = userUpdateForm(instance=request.user) #it provide the data eith the requested user...
    else:
        userForm = userUpdateForm(instance=request.user)
        return render(request, 'User/userUpdate.html', {'form': userForm})


def CheckReservation(request): #to view the reserved Item....
    currDate = date.today()
    expItemObj = ReserveItem.objects.filter(UserId=request.user,DateOfReturn__lt=currDate)
    currItemObj = ReserveItem.objects.filter(UserId=request.user,DateOfReturn__gte=currDate)
    return render(request, 'User/CheckReservations.html',{'expitem': expItemObj, 'curritem':currItemObj})  
          

def userLogout(request): #user logout function.....
    messages.success(request, "logout Successfully!")
    auth.logout(request)
    return redirect("/LoginUsr/")
