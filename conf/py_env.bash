#!/bin/bash

export LD_LIBRARY_PATH=/usr/lib:/usr/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/oqr/Svr/Quote/py:/oqr/Libs/pricing/src/py:/oqr/MD/FIX/py:$LD_LIBRARY_PATH:$PYTHONPATH
export PYTHONPATH=/oqr/Libs/utils/src/py:$PYTHONPATH
export XML_CONF_DIR=/oqr/conf/ 
