#coding: utf-8

def person_user(request):
    try:
        return {"user": request.user.person}
    except:
        return {"user": request.user}
