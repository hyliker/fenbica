#coding: utf-8
from django.db import models
from django.template import Library, Node
from person.models import Person
register = Library()

#@register.inclusion_tag('person/templatetags/person_statistics.html', takes_context=True)
#def person_statistics(context, obj):
    #return {"staff": 283}

class PersonStatisticsNode(Node):
    def render(self, context):
        from staff.models import Staff
        from student.models import Student
        staff_list = Staff.objects.filter(is_leaved=False)
        student_list = Student.objects.filter(is_leaved=False)

        context['person_statistics'] = {
            "staff": {
                "count": staff_list.count(),
                "male_count": staff_list.filter(gender__name=u"男").count(),
                "female_count": staff_list.filter(gender__name=u"女").count(),
            },
            "student": {
                "count": student_list.count(),
                "male_count": student_list.filter(gender__name=u"男").count(),
                "female_count": student_list.filter(gender__name=u"女").count(),
            },
        }
        return ''

@register.tag
def get_person_statistics(parser, token):
    return PersonStatisticsNode()
