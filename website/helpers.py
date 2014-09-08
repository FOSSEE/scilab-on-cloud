import os, re, sys, time, subprocess

from soc.settings import PROJECT_DIR
from timeout import TimerTask
 
def scilab_run(code, token, book_id, dependency_exists): 
    #Check for system commands
    system_commands = re.compile(
        'unix\(.*\)|unix_g\(.*\)|unix_w\(.*\)|unix_x\(.*\)|unix_s\(.*\)|host|newfun|execstr|ascii|mputl|dir\(\)'
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

    #traps even syntax errors eg: endfunton
    f = open(file_path, "w")
    f.write('mode(2);\n')
    if dependency_exists:
        f.write('getd("/var/www/scilab_in/uploads/{0}/DEPENDENCIES/");'.format(book_id))
    f.write('lines(0);\n')
    f.write(unicode(code))
    f.write('\nquit();')
    f.close()
    
    #this makes it possible to execute scilab without the problem of \
    #getting stuck in the prompt in case of error
    cmd = 'printf "exec(\'{0}\',2);\nquit();"'.format(file_path)
    cmd += ' | /home/cheese/scilab-5.4.1/bin/scilab-adv-cli -nw'

    task = TimerTask(cmd, timeout=10)
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
