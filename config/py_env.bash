#!/bin/bash

export LD_LIBRARY_PATH=/usr/lib:/usr/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/oqr/Svr/Quote/py:/oqr/Libs/pricing/src/python:/oqr/MD/FIX/python:$LD_LIBRARY_PATH:$PYTHONPATH
export PYTHONPATH=/oqr/Libs/utils/src/py:$PYTHONPATH
export XML_CONF_DIR=/oqr/config/ 
