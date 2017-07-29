import random
import re
from soc.config import *
from website.models import *

def entry(code, example_id, dependency_exists):
    foo="exec"
    b= 0
    c= 1303985023
    d= example_id

    if foo in code:
        if dependency_exists :
            return dependency_exists
        aa = code.find('exec(\'')
        if aa > 0:
            bb = code.find('\'',aa+7)
            value = code[(aa+6):bb]
        elif (aa == code.find('exec (\"')):
            bb = code.find('\"',aa+7)
            value = code[(aa+7):bb]
        elif(aa == code.find('exec(\"')):
            bb = code.find('\'',aa+7)
            value = code[(aa+6):bb]
        else:
            print("unknown exec format")
            dependency_exists= False
            return dependency_exists

        data_df = TextbookCompanionDependencyFiles.objects.db_manager('scilab')\
        .raw("""SELECT id FROM textbook_companion_dependency_files
         WHERE filename = %s""", [value]) #get the dependency id
        data = data_df[0].id  # extract the id
        if data is not None:
            role = int(data_df[0].id)
            #role1 = int(data[1])
            #print role1
            if not dependency_exists:
                TED_insert = TextbookCompanionExampleDependency()
                TED_insert.example_id = d
                TED_insert.dependency_id = role
                TED_insert.approval_status = b
                TED_insert.timestamp = c
                TED_insert.save(using='scilab')
                dependency_exists= True
    else:
        dependency_exists= False

    return dependency_exists







