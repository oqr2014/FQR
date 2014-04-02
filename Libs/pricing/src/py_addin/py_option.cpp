/***********************************************
 * boost python wrapper for greeks.hpp 
 ***********************************************/
#include "py_addin.hpp"

using namespace boost::python; 
using namespace QR; 

void export_QR_Option()
{
scope Option_scope
  = class_<Option>("Option", init<>())
    .def(init<const Option&>()) 
    .def(init<Option::Style, Option::Type, const QuantLib::Date&, const QuantLib::Date&, 
		double, double, double, double, double>()) 
    .def(init<Option::Style, Option::Type, double, 
		double, double, double, double, double>()) 
	.def("clone", &Option::clone, return_value_policy<manage_new_object>())
	.def("calcPrice", &Option::calcPrice)
	.def("calcDelta", &Option::calcDelta)
	.def("calcGamma", &Option::calcGamma)
	.def("calcVega", &Option::calcVega)
	.def("calcTheta", &Option::calcTheta)
	.def("calcRho", &Option::calcRho)
	.def("calcImplVol", &Option::calcImplVol)
	.def("getTypeName", &Option::getTypeName)
	.def("getStyleName", &Option::getStyleName)
    .add_property("ex_style", &Option::getStyle, &Option::setStyle) 
    .add_property("cp_type", &Option::getType, &Option::setType) 
    .add_property("S", &Option::getSpot, &Option::setSpot) 
    .add_property("K", &Option::getStrike, &Option::setStrike) 
    .add_property("T", &Option::getT2M, &Option::setT2M) 
    .add_property("sigma", &Option::getVol, &Option::setVol) 
    .add_property("r", &Option::getRate, &Option::setRate) 
    .add_property("q", &Option::getDivYield, &Option::setDivYield) 
    .add_property("initFlag", &Option::getInitFlag, &Option::setInitFlag) 
    .add_property("greeks", &Option::getGreeks, &Option::setGreeks) 
    .add_property("price", &Option::getPrice, &Option::setPrice) 
	;

	enum_<Option::Type>("Type")
	.value("PUT", Option::PUT)
	.value("CALL", Option::CALL)
	; 

	enum_<Option::Style>("Style")
	.value("EURO", Option::EURO)
	.value("AM", Option::AM)
	.value("EUROPEAN", Option::EUROPEAN)
	.value("AMERICAN", Option::AMERICAN)
	; 
}

