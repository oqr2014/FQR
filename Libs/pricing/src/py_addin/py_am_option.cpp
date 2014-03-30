/***********************************************
 * boost python wrapper for greeks.hpp 
 ***********************************************/
#include "py_addin.hpp"

using namespace boost::python; 
using namespace QR; 

void export_QR_AmOption()
{
    class_<AmOption, bases<Option> >("AmOption", init<>())
    .def(init<const AmOption&>()) 
    .def(init<Option::Type, const QuantLib::Date&, const QuantLib::Date&, 
		double, double, double, double, double>()) 
    .def(init<Option::Type, double, double, double, double, double, double>()) 
	.def("clone", &AmOption::clone, return_value_policy<manage_new_object>())
	.def("calcPrice", &AmOption::calcPrice)
	.def("calcGreeksAnalytic", &AmOption::calcGreeksAnalytic)
	.def("calc", &AmOption::calc)
	;
}

