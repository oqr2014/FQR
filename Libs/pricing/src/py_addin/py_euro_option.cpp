/***********************************************
 * boost python wrapper for greeks.hpp 
 ***********************************************/
#include "py_addin.hpp"

using namespace boost::python; 
using namespace QR; 

void export_QR_EuroOption()
{
    class_<EuroOption, bases<Option> >("EuroOption", init<>())
    .def(init<const EuroOption&>()) 
    .def(init<Option::Type, const QuantLib::Date&, const QuantLib::Date&, 
		double, double, double, double, double>()) 
    .def(init<Option::Type, double, double, double, double, double, double>()) 
	.def("clone", &EuroOption::clone, return_value_policy<manage_new_object>())
	.def("calcPrice", &EuroOption::calcPrice)
	.def("calcGreeksAnalytic", &EuroOption::calcGreeksAnalytic)
	.def("calc", &EuroOption::calc)
	;
}

