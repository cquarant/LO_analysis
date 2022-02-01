#!/bin/sh

#Prod1
python launch_analyze_run_array_opt.py --firstRun 6084 --arrayCode 416 -i data/ --output data/
python launch_analyze_run_array_opt.py --firstRun 6090 --arrayCode 809 -i data/ --output data/

#Prod3
python launch_analyze_run_array_opt.py --firstRun 6096 --arrayCode 586 -i data/ --output data/
python launch_analyze_run_array_opt.py --firstRun 6102 --arrayCode 805 -i data/ --output data/

#Prod4
python launch_analyze_run_array_opt.py --firstRun 6108 --arrayCode 708 -i data/ --output data/
python launch_analyze_run_array_opt.py --firstRun 6114 --arrayCode 799  -i data/ --output data/

#Prod5
python launch_analyze_run_array_opt.py --firstRun 6120 --arrayCode 531 -i data/ --output data/
python launch_analyze_run_array_opt.py --firstRun 6126 --arrayCode 800  -i data/ --output data/

#Prod9

#Prod10
