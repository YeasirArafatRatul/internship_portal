
from background_task import background
from .models import Applicant

print("*********************************************CAME HERE TO INITIATE******************************************")


@background(schedule=20)
def time_to_live(id):
    print('ID ISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', id)
    obj = Applicant.objects.get(id=id)
    print('OBJECCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCT', obj.id)
    obj.delete()
