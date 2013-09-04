from Enviro.models import User, Booth, UserToBooth, UserSimilarities, BoothSimilarities
from Enviro.qrCodeManager import QRCodeManager
import ESAsimilarity
import SpreadingActivation
from django.http import HttpResponse
import json
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

import threading

similarity_thread=None
profile_thread=None

def login(request,username=None,password=None):
    '''
        The authenticator function which permits user into the system
    '''

    response = {}

    # Credentials provider check
    if username is None or password is None:
        response['msg'] = "User.CredentialsNotProvided"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Query the User DB for the corresponding username and password
    try:
        user = User.objects.get(username=username,password=password)

    except User.DoesNotExist:
        # User aws not found, probably wrong username or password
        response['msg'] = "User.DoesNotExist"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    except User.MultipleObjectsReturned:
        # This case cannot happen, still might be a good check
        response['msg'] = "User.MultipleObjectsReturned"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Respond with ok message and user id
    response['msg'] = "User.AccessGranted"
    response['id'] = user.id
    response['username'] = user.username
    response['code'] = 200

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response


@csrf_exempt
def register(request):
    '''
        The function which registers an user into the system
    '''
    global similarity_thread, profile_thread
    response = {}

    # Get user info
    request_data = json.loads(request._get_raw_post_data())

    # Try adding it into User DB
    new_user = User(name=request_data['name'], username=request_data['username'], password=request_data['password'],
                    tag_set=request_data['tagSet'])

    # Perform DB validation of fields
    try:
        new_user.full_clean()

    except ValidationError, e:
        response['msg']='; '.join(e.messages)
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Commit to DB
    new_user.save()

    # Compute similarities and update similarity tables
    #ESAsimilarity.computeUserSimilarities("register", userId=new_user.id, tagSet=request_data['tagSet'])
    similarity_thread = threading.Thread(target=ESAsimilarity.computeUserSimilarities,
                                         args=["register", new_user.id, request_data['tagSet']])
    similarity_thread.start()

    #SpreadingActivation.spreadingActivationAlgo(request_data['tagSet'], new_user.id, 5, "2.1")
    profile_thread = threading.Thread(target=SpreadingActivation.spreadingActivationAlgo,
                                         args=[request_data['tagSet'], new_user.id, 5, "2.1"])
    profile_thread.start()

    # Send back the response
    response['msg'] = "User.RegisterAccepted"
    response['code'] = 200

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response



def get_current_location(request,userId=None):
    '''
        The function sends details about the current location of the user
    '''
    global similarity_thread
    response = {}

    # Check to se if the user is checked in at a booth
    try:
        user2booth = UserToBooth.objects.get(user=userId)
    except UserToBooth.DoesNotExist:
        # If there is no correspondence between a booth and an user
        response['msg'] = "UserToBooth.DoesNotExist"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response


    # Get booth details
    booth = Booth.objects.get(id=user2booth.booth.id)
    user2booth_id_list = UserToBooth.objects.filter(booth=booth.id).values_list('user_id', flat=True)
    user2booth_name_list = User.objects.filter(id__in=user2booth_id_list).values_list('id','name','tag_set')

    # Get similarity
    user_similarities = UserSimilarities.objects.filter(userFrom=userId, userTo__in=user2booth_id_list).values_list('similarity', flat=True)

    # Send details about users checked in at the same booth
    response['users']={}
    # Check if the similarity process is ready
    if similarity_thread is None or not similarity_thread.isAlive() :
        for i in range(len(user2booth_id_list)):
            response['users'][i] = {}
            response['users'][i]['name'] = user2booth_name_list[i][1]
            response['users'][i]['tagSet'] = user2booth_name_list[i][2]
            response['users'][i]['similarity'] = "{0:.2f}".format(float(user_similarities[i])*100)

    # Send details about the booth
    response['msg'] = "UserToBooth.Exists"
    response['code'] = 200
    response['title'] = booth.title
    response['logo'] = booth.logo
    response['description'] = booth.description
    response['tagSet'] = booth.tag_set
    if similarity_thread is not None and similarity_thread.isAlive() :
        response['similarity'] = None
    else:
        booth_similarities = BoothSimilarities.objects.get(userFrom=userId, boothTo=booth.id)
        response['similarity'] = "{0:.2f}".format(float(booth_similarities.similarity)*100)
    response['checkedIn'] = len(user2booth_id_list)

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response

def get_sa_profile(request,userId=None):
    '''
        Sends details about the user profile
    '''
    global profile_thread
    response = {}

    # Check if the similarity process is ready
    if profile_thread is not None and profile_thread.isAlive() :
        response['msg'] = "UserProfile.NotReady"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Find the user in the system
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        response['msg'] = "User.DoesNotExist"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Send details about the user
    response['msg'] = "User.Exists"
    response['code'] = 200
    response['name'] = user.name
    response['username'] = user.username
    response['password'] = user.password
    response['tagSet'] = user.tag_set
    response['tagSetNew'] = user.tag_set_improved

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response


def get_profile(request,userId=None):
    '''
        Sends details about the user profile
    '''
    response = {}

    # Find the user in the system
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        response['msg'] = "User.DoesNotExist"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Send details about the user
    response['msg'] = "User.Exists"
    response['code'] = 200
    response['name'] = user.name
    response['username'] = user.username
    response['password'] = user.password
    response['tagSet'] = user.tag_set

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response


@csrf_exempt
def update_profile(request):
    '''
        Gets the user details and update the database with the changes
    '''
    global similarity_thread, profile_thread
    response = {}

    # Get data from client via post
    request_data = json.loads(request._get_raw_post_data())

    # Finds the user in the system
    try:
        user = User.objects.get(id=request_data['userId'])

    except User.DoesNotExist:
        response['msg'] = "User.DoesNotExist"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    user.name = request_data['name']
    user.username = request_data['username']
    user.password = request_data['password']
    tags = request_data['tagSet']
    if tags != '':
        user.tag_set = tags

    # Check validation of fields for DB commit
    try:
        user.full_clean()

    except ValidationError, e:
        response['msg'] = "User.ProfileErrors"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Commit changes to database
    user.save(force_update=True)

    # Compute similarities and update similarity tables
    similarity_thread = threading.Thread(target=ESAsimilarity.computeUserSimilarities,
                                         args=["update_profile", request_data['userId'], request_data['tagSet']])
    similarity_thread.start()

    # Compute profile and update user profile table
    profile_thread = threading.Thread(target=SpreadingActivation.spreadingActivationAlgo,
                                      args=[request_data['tagSet'], request_data['userId'], 5, "2.1"])
    profile_thread.start()

    response['msg'] = "User.ProfileUpdated"
    response['code'] = 200

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response


def get_booths(request,userId=None):
    '''
        Send details about the booths registered into the system
    '''
    global similarity_thread
    response = {}

    # Check if the similarity process is ready
    if similarity_thread is not None and similarity_thread.isAlive() :
        response['msg'] = "Booth.SimilaritiesNotReady"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Get the booths from the system
    count = 0
    for booth in Booth.objects.all():
        count += 1
        response[count] = {}
        response[count]['title'] = booth.title
        response[count]['logo'] = booth.logo
        response[count]['description'] = booth.description
        response[count]['tagSet'] = booth.tag_set
        booth_similarities = BoothSimilarities.objects.get(userFrom=userId, boothTo=booth.id)
        response[count]['similarity'] = "{0:.2f}".format(float(booth_similarities.similarity)*100)
        response[count]['checkedIn'] = UserToBooth.objects.filter(booth=booth.id).count()


    response['msg'] = "Booth.Exists"
    response['code'] = 200
    response['noBooths'] = count

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response


def checkin(request, boothId=None, userId=None):
    '''
        Function that performs a check in of a user at a booth
    '''
    response = {}

    # It has to receive a booth id
    if boothId is None:
        response['msg'] = "User.CheckInFailed"
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Get the user and the booth from DB
    user = User.objects.get(id=userId)
    booth = Booth.objects.get(id=boothId)

    # CheckOut user from old booth, if exists. Delete from UserToBooth
    UserToBooth.objects.filter(user=user.id).delete()
    # CheckIn user to
    new_user2booth = UserToBooth(user=user,booth=booth)

    # Perform validation for DB fields
    try:
        new_user2booth.full_clean()

    except ValidationError, e:
        response['msg']='; '.join(e.messages)
        response['code'] = 200

        http_response = HttpResponse(json.dumps(response), content_type='application/json')
        http_response.status_code = response['code']
        return http_response

    # Commit changes to DB
    new_user2booth.save()

    response['msg'] = "User.CheckInAccepted"
    response['code'] = 200

    http_response = HttpResponse(json.dumps(response), content_type='application/json')
    http_response.status_code = response['code']
    return http_response

def checkout(request,userId):
     '''
        Function that performs a checkout of a user from the event
     '''
     response = {}

     # CheckOut user from old booth, if exists. Delete from UserToBooth
     UserToBooth.objects.filter(user=User.objects.get(id=userId)).delete()

     response['msg'] = "User.CheckOutAccepted"
     response['code'] = 200

     http_response = HttpResponse(json.dumps(response), content_type='application/json')
     http_response.status_code = response['code']
     return http_response


# ----------------------------------------------------------------------------------------------------------------------
# Private ADMIN methods

def generate_qr(request):
    '''
        Generate the QR codes files
    '''

    # Get the booth list from DB
    booths_list = Booth.objects.all()

    print "-->Start generating QR codes:"
    # For every booth found, call QR Manager to generate the corresponding qr code
    for booth in booths_list:
        print QRCodeManager.generate_qr_code(booth)

    #Create checkout QR code
    print QRCodeManager.generate_qr_code()

    # Send successful message
    http_response = HttpResponse(json.dumps({"msg" : "QR Codes Successfully Generated"}), content_type='application/json')
    http_response.status_code = 200
    return http_response