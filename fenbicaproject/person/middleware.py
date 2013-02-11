#coding: utf-8

class PersonMiddelware(object):
    def process_request(self, request):
        try:
            request.person = request.user.person
        except:
            request.person = None
        return None
