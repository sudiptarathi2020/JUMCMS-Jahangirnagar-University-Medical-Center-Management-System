from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from certifications.models import FundraisingRequest, FundraisingCertificate

# Create your views here.
@login_required
def fundraising_request_list(request):
    """
    Display a list of all fundraising requests.

    Retrieves all instances of FundraisingRequest from the database 
    and renders them in the 'admin/show_requests.html' template.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered page displaying the list of fundraising requests.
    """
    fundraising_requests = FundraisingRequest.objects.all()
    
    return render(request, 'admin/show_requests.html', {'fundraising_requests': fundraising_requests})

@login_required
def approve(request, request_id):
    """
    Toggle the approval status of a specified fundraising request.

    Fetches the FundraisingRequest by the provided ID. If approved, assigns a unique 
    serial number. If unapproved, removes the serial number. Displays a success 
    message indicating the update and redirects to the list of fundraising requests.

    Parameters:
        request (HttpRequest): The HTTP request object.
        request_id (int): The ID of the fundraising request to approve/unapprove.

    Returns:
        HttpResponseRedirect: Redirects to the fundraising request list view.
    """
    # Fetch the fundraising request by ID
    user = request.user
    fundraising_request = get_object_or_404(FundraisingRequest, id=request_id)
    
    
    fundraising_request.is_approved = not fundraising_request.is_approved
    
    if fundraising_request.is_approved == True:
        fundraising_request.serial_number = get_random_string(length=20, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        fundraising_request.save()
    elif fundraising_request.is_approved == False:
        fundraising_request.serial_number = None
        fundraising_request.save()

    
    # Add a success message
    messages.success(request, f"Approval status for {fundraising_request.patient.user.name} updated successfully.")
    
    # Redirect to the same page (or to the admin page showing the list)
    return redirect('certifications:fundraising-request-list', )