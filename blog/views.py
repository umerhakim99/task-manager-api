from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .forms import ContactForm
from .models import Contact
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.core.paginator import Paginator
# from django.db.models import Q


from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactSerializer


# Class base 
from rest_framework.views import APIView













def home(request):
    return render(request, 'blog/home.html')



# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)

#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']

#             print(name)
#             print(email)
#             print(message)

#             return render(request, 'blog/success.html')

#     else:
#         form = ContactForm()

#     return render(request, 'blog/contact.html', {'form': form})






@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            # return render(request, 'blog/success.html')
            messages.success(request, "Contact Created Successfully.")
            return redirect('messages')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})







@login_required
def contact_list(request):

    search_query = request.GET.get('q')
    sort = request.GET.get('sort')

    contacts = Contact.objects.filter(user=request.user)

    # SEARCH
    if search_query:
        contacts = contacts.filter(name__icontains=search_query)

    # SORTING
    if sort == "name":
        contacts = contacts.order_by('name')

    elif sort == "email":
        contacts = contacts.order_by('email')

    # elif sort =="message":
    #     contacts = contacts.order_by('message')

    else:
        contacts = contacts.order_by('-id')   # newest first

    paginator = Paginator(contacts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/messages.html', {
        # 'contacts': contacts,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort': sort
    })


#------------------------------------------------------





@login_required
def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Updated Successfully.')
            return redirect('messages')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'edit_contact.html', {'form': form})




@login_required
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)

    if request.method == "POST":
        contact.delete()
        messages.success(request, "Contact Deleted Successfully.")
        return redirect('messages')

    return render(request, 'blog/delete_contact.html', {'contact': contact})







# @api_view(['GET'])
# def contact_api(request):
#     contacts = Contact.objects.all()
    
#     serializer = ContactSerializer(contacts, many=True)


#     return Response(serializer.data)


@api_view(['GET', 'POST']) 
def contact_api(request):

    if request.method == 'GET':
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(serializer.errors)






@api_view([ 'GET','PUT', 'DELETE'])  
def contact_detail_api(request, id):

    try:
        contact = Contact.objects.get(id=id, user=request.user)
    except Contact.DoesNotExist:
        return Response({"error": "Contact not found"}, status=404)


    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)


    if request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    if request.method == 'DELETE':
        contact.delete()
        return Response({"message": "Contact deleted"})
    






class ContactListAPI(APIView):

    def get(self, request):
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(serializer.errors)
    





class ContactDetailAPI(APIView):

    def get(self, request, id):

        try:
            contact = Contact.objects.get(id=id, user=request.user)
        except Contact.DoesNotExist:
            return Response({"error": "Contact not found"}, status=404)

        serializer = ContactSerializer(contact)
        return Response(serializer.data)



    def put(self, request, id):

        try:
            contact = Contact.objects.get(id=id, user=request.user)
        except Contact.DoesNotExist:
            return Response({"error": "Contact not found"}, status=404)

        serializer = ContactSerializer(contact, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)



    def delete(self, request, id):

        try:
            contact = Contact.objects.get(id=id, user=request.user)
        except Contact.DoesNotExist:
            return Response({"error": "Contact not found"}, status=404)
        contact.delete()
        return Response({"message": "Contact deleted"})




#----------------------------------------


from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import filters

from .permissions import IsOwner



class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    serializer_class = ContactSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'message']
    ordering_fields = ['name', 'email', 'created_at']

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)










