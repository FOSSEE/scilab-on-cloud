import random
import re
import os
from soc.config import *
from website.models import *
from shutil import *
from soc.config import UPLOADS_PATH
import mimetypes
import time


def entry(code, example_id, dependency_exists, book_id):
    foo = "exec"
    b = 0
    c = 1303985023
    d = example_id
    #QUOTED_STRING_RE = re.compile(r'exec\(".*"\)')

    index = 0
    while index < len(code):
        index = code.find('exec\(', index)
        if index == -1:
            break
        if index > 0:
            bb = code.find('\'', index + 7)
            value = code[(index + 6):bb]
        elif (index == code.find('exec (\"')):
            bb = code.find('\"', index + 7)
            value = code[(index + 7):bb]
        elif(index == code.find('exec(\"')):
            bb = code.find('\'', index + 7)
            value = code[(index + 6):bb]
        else:
            print("unknown exec format")
            dependency_exists = False
            return dependency_exists
        print ("file name: " + value)
        data_df = TextbookCompanionDependencyFiles.objects.using('scilab')\
            .filter(filename=value)  # get the dependency id

        if not data_df.count():
            filepath = UPLOADS_PATH
            print ("file path: " + UPLOADS_PATH + "/" + str(book_id))

            def find_all(name, path):
                result = []
                for root, dirs, files in os.walk(path):
                    if name in files:
                        result.append(os.path.join(root, name))
                return result
            result_files = find_all(value, UPLOADS_PATH + "/" + str(book_id))
            print (result_files[0])
            check_file_exist = os.path.exists(
                UPLOADS_PATH + "/" + str(book_id) + "/DEPENDENCIES/" + value)
            if check_file_exist == False:
                copy(result_files[0], UPLOADS_PATH +
                     "/" + str(book_id) + "/DEPENDENCIES")
                filepath = UPLOADS_PATH + "/" + \
                    str(book_id) + "/DEPENDENCIES/" + value
                filesize = os.path.getsize(filepath)
                filemime = mimetypes.guess_type(filepath)

                TED_insert = TextbookCompanionDependencyFiles()
                TED_insert.preference_id = book_id
                TED_insert.filename = value
                TED_insert.filepath = str(book_id) + "/DEPENDENCIES/" + value
                TED_insert.filemime = filemime
                TED_insert.filesize = filesize
                TED_insert.caption = value
                TED_insert.description = value
                TED_insert.timestamp = int(time.time())
                TED_insert.save(using='scilab')
                dep_file_id = TextbookCompanionDependencyFiles.objects.using('scilab')\
                    .get(filename=value)
                print (dep_file_id.id)
                TED_insert = TextbookCompanionExampleDependency()
                TED_insert.example_id = d
                TED_insert.dependency_id = dep_file_id.id
                TED_insert.approval_status = b
                TED_insert.timestamp = int(time.time())
                TED_insert.save(using='scilab')

                role = TextbookCompanionDependencyFiles.objects.using('scilab')\
                    .get(filename=value)
                if not dependency_exists:
                    TED_insert = TextbookCompanionExampleDependency()
                    TED_insert.example_id = d
                    TED_insert.dependency_id = role.id
                    TED_insert.approval_status = b
                    TED_insert.timestamp = c
                    TED_insert.save(using='scilab')
                    dependency_exists = True

        else:
            dependency_exists = TextbookCompanionExampleDependency.objects.using('scilab')\
                .filter(example_id=example_id).exists()
            if not dependency_exists:
                role = TextbookCompanionDependencyFiles.objects.using('scilab')\
                    .get(filename=value)
                TED_insert = TextbookCompanionExampleDependency()
                TED_insert.example_id = d
                TED_insert.dependency_id = role.id
                TED_insert.approval_status = b
                TED_insert.timestamp = c
                TED_insert.save(using='scilab')
                dependency_exists = True

        # end
        index += 2  # +2 because len('ll') == 2

    return dependency_exists
