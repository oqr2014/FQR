#include "py_addin.hpp"

using namespace boost::python; 
using namespace QR; 

void export_QR_Greeks(); 
void export_QR_Option(); 
void export_QR_EuroOption(); 
void export_QR_AmOption(); 
void export_QuantLib_Date(); 
void export_QR_Utility(); 

BOOST_PYTHON_MODULE(liboqr_py)
{
	export_QR_Greeks(); 
	export_QR_Option(); 
	export_QR_EuroOption(); 
	export_QR_AmOption(); 
	export_QuantLib_Date(); 
	export_QR_Utility(); 
}

