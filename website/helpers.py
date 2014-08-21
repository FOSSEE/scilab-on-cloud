import os
import re
import time
import subprocess

from soc.settings import PROJECT_DIR
 
def scilab_run(code, token, example_id): 
    #Check for system commands
    system_commands = re.compile(
        'unix\(.*\)|unix_g\(.*\)|unix_w\(.*\)|unix_x\(.*\)|unix_s\(.*\)'
    )
    if system_commands.search(code):
        return "System Commands not allowed"

    #Remove all clear;
    code = re.sub(r'clear.*all|clear|clc\(\)|clc', '', code)

    plot_exists = False

    #Finding the plot and appending xs2jpg function
    p = re.compile(r'.*plot.*\(.*,.*,*\).*\n')

    plot_path = ''
    if p.search(code):
        plot_exists = True
        code = code + '\n'
        current_time = time.time()
        plot_path = PROJECT_DIR + '/static/tmp/{0}.jpg'.format(str(current_time))
        code += 'xs2jpg(gcf(), "{0}");\n'.format(plot_path)

    #Check whether to load scimax / maxima
    if 'syms' in code or 'Syms' in code:
        code = code.replace('syms', 'Syms')
        code = 'exec(\'/home/cheese/scimax/loader.sce\');\nmaxinit\n' + code

    file_path = PROJECT_DIR + '/static/tmp/' + token + '.sci'

    #thanks @prathamesh920 github
    #traps even syntax errors eg: endfunton
    f = open(file_path, "w")
    f.write('mode(2);\n')
    f.write(unicode(code))
    f.write('\nquit();')
    f.close()
    

    #this makes it possible to execute scilab without the problem of \
    #getting stuck in the prompt in case of error
    cmd = 'printf "lines(0)\nexec(\'{0}\',2);\nquit();"'.format(file_path)
    cmd += ' | /home/cheese/scilab-5.4.1/bin/scilab-adv-cli -nw'

    output = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    ).communicate()[0]

    #os.remove(file_path)
    output = trim(output)
    data = {
        'output': output,
        'plot_path': plot_path.replace(PROJECT_DIR, '')
    }
    return data

def trim(output):
    #for future use
    output = re.sub(r'\n \n \n', '\n', output)
    return output
