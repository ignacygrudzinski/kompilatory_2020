import sys,os
import pathlib
from os.path import exists

def p(name):
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),name)

def run_from(name, input_file, output_file):
    parser_path = os.path.join(str(pathlib.Path(__file__).parent.absolute()),'..','parser2.py')
    with open(p(name)) as python_cmd_file:
            python_cmd = python_cmd_file.read()
            cmd = python_cmd + " " + parser_path + " < "  + input_file + " > " + output_file
            os.system(cmd)

def test(input, output):
    
    # prepare files
    input_file = p('input')
    output_file = p('output')

    # write
    f = open(input_file, "w")
    f.write(input)
    f.close()
    
    # execute   
    if exists(p('python_cmd')):        
        run_from('python_cmd', input_file, output_file)
    else:
        msg =  '''
                create python_cmd file in repository root folder with python interpreter command
                i.e. for linux: /usr/bin/python3
                for Windows: python3

                using default
                '''
        print(msg)
        run_from('python_cmd_default', input_file, output_file)

    # get output
    with open(output_file) as f:
        result = f.read()[:-1]
        
        if(result == output):
            print("OK")
        else:
            print("*****ERROR*******\n"+input+'\n*********WAS**********\n'+result + "\n**********SHOULD*BE*********\n" + output + "\n************************\n")
            
  
