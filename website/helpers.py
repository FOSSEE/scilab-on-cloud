import os
import re
import time
import subprocess

from soc.settings import PROJECT_DIR
 
def scilab_run(code, token):
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

    # Create a file for the current request
    canvas_off = """
    function turnCanvasOff()
       m = getscilabmode();
       if (m=="STD"|m=="NW") then
           previousDisp = disp;
           prot = funcprot();
           funcprot(0);
           deff("disp(str)", "");
           usecanvas(%f);
           disp = previousDisp;
           funcprot(prot);
       end
    endfunction
    turnCanvasOff();
    clear turnCanvasOff;
    """

    file_path = PROJECT_DIR + '/static/tmp/' + token + '.sci'

    f = open(file_path, "w")
    f.write("mode(-1);\nlines(0);\nmode(-1);\ntry\nmode(2);\n")
    f.write('lines(0)\n')
    f.write(canvas_off)
    f.write(code)
    f.write('\nexit')
    f.write("\nmode(-1);\nexit();\ncatch\nmode(-1);\ndisp(lasterror());\nexit();")
    f.close()
    
    if plot_exists:
        cmd = 'export DISPLAY=:99 && '
        cmd +=  'xvfb-run -a cat {0}'.format(file_path) + ' | scilab-adv-cli -nw -nb'
        print "############################"
        print cmd
    else:
        cmd = 'cat {0}'.format(file_path) + ' | scilab-adv-cli -nw'

    output = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    ).communicate()[0]
    #os.remove(file_path)
    output = trim(output)
    return output

def trim(output):
    atoms_banner = """
    Start Image Processing Tool 2
        Load macros
        Load help

    SIVP - Scilab Image and Video Processing Toolbox
        Load macros
        Load gateways
        Load help
        Load demos


     
     Start identification   
     
     Load macros   
     
     Load help   
    """
    output = output.replace(atoms_banner, '')
    return output
