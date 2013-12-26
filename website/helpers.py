import os
import re
import time
import subprocess

from soc.settings import PROJECT_DIR
 
def scilab_run(code, token):
    #Remove all clear;
    code = code.replace('clear','')
    code = code.replace(r'clear.*all','')
    plot_exists = False

    #Finding the plot and appending xs2jpg function
    p = re.compile(r'.*plot.*\(.*,.*,*\).*\n')
    if p.search(code):
        plot_exists = True
        code = code + '\n'
        temp = code
        code = ''
        start, end, count = 0, 0, 0
        current_time = time.time()
        plot_path = []
        for (count, match) in enumerate(p.finditer(temp)):
            print "count==================",count
            plot_path.append(
                PROJECT_DIR + '/static/tmp/{0}.jpg'.format(int(current_time) + count)
            )
            end = match.end()
            code += temp[start:end]
            code += 'xs2jpg(gcf(), "{0}");\n'.format(plot_path[-1])
            start = end
        code += temp[end:]

    #Check whether to load scimax / maxima
    if 'syms' in code or 'Syms' in code:
        code = code.replace('syms', 'Syms')
        code = 'exec(\'/home/cheese/scimax/loader.sce\');\nmaxinit\n' + code

    file_path = PROJECT_DIR + '/static/tmp/' + token + '.sci'

    #thanks @prathamesh920 github
    #traps even syntax errors eg: endfunton
    f = open(file_path, "w")
    f.write('mode(2);\n')
    f.write(code)
    f.write('\nquit();')
    f.close()
    

    #this makes it possible to execute scilab without the problem of \
    #getting stuck in the prompt in case of error
    cmd = 'printf "lines(0)\nexec(\'{0}\',2);\nquit();"'.format(file_path)
    cmd += ' | /home/cheese/scilab-5.4.1/bin/scilab-adv-cli -nw'
    print cmd

    output = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    ).communicate()[0]

    #os.remove(file_path)
    output = trim(output)
    return output

def trim(output):
    #for future use
    return output
