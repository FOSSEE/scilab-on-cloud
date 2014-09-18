import os, re, sys, time, subprocess

from soc.settings import PROJECT_DIR
from timeout import TimerTask
from soc.config import SCILAB_BIN, SCILAB_FLAGS, SCIMAX_LOADER, UPLOADS_PATH
 
def scilab_run(code, token, book_id, dependency_exists): 
    #Check for system commands
    system_commands = re.compile(
        'unix\(.*\)|unix_g\(.*\)|unix_w\(.*\)|unix_x\(.*\)|unix_s\(.*\)|host|newfun|execstr|ascii|mputl|dir\(\)'
    )
    if system_commands.search(code):
        return { 
            'output': 'System Commands not allowed',
        }

    #Remove all clear;
    code = re.sub(r'clear.*all|clear|clc\(\)|clc', '', code)

    plot_exists = False

    #Finding the plot and appending xs2jpg function
    p = re.compile(r'.*plot.*\(.*\).*\n|bode\(.*\)|evans\(.*\)')

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
        code = 'exec(\'{0}\');\nmaxinit\n'.format(SCIMAX_LOADER) + code

    file_path = PROJECT_DIR + '/static/tmp/' + token + '.sci'

    #traps even syntax errors eg: endfunton
    f = open(file_path, "w")
    f.write('mode(2);\n')
    if dependency_exists:
        f.write(
            'getd("{0}/{1}/DEPENDENCIES/");'.format(UPLOADS_PATH, book_id)
        )
    f.write('lines(0);\n')
    f.write(unicode(code))
    f.write('\nquit();')
    f.close()
    
    #this makes it possible to execute scilab without the problem of \
    #getting stuck in the prompt in case of error
    cmd = 'printf "exec(\'{0}\',2);\nquit();"'.format(file_path)
    cmd += ' | {0} {1}'.format(SCILAB_BIN, SCILAB_FLAGS)

    task = TimerTask(cmd, timeout=15)
    output = task.run().communicate()[0]
    e = task.wait()

    output = trim(output)
    data = {
        'output': output,
        'plot_path': plot_path.replace(PROJECT_DIR, '')
    }
    return data

def trim(output):
    output = [line for line in output.split('\n') if line.strip() != '']
    output = '\n'.join(output)
    return output
