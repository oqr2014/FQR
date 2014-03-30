/***********************************************
 * boost python wrapper for greeks.hpp 
 ***********************************************/
#include "py_addin.hpp"

using namespace boost::python; 
using namespace QR; 

void export_QuantLib_Date()
{
	using QuantLib::Date; 
	class_<Date>("Date", init<>())
	.def(init<int, QuantLib::Month, int>())
	.def("dayOfMonth", &Date::dayOfMonth)
	.def("month", &Date::month)
	.def("year", &Date::year)
	;

	enum_<QuantLib::Month>("Month")
	.value("Jan", QuantLib::Jan)
	.value("Feb", QuantLib::Feb)
	.value("Mar", QuantLib::Mar)
	.value("Apr", QuantLib::Apr)
	.value("May", QuantLib::May)
	.value("Jun", QuantLib::Jun)
	.value("Jul", QuantLib::Jul)
	.value("Aug", QuantLib::Aug)
	.value("Sep", QuantLib::Sep)
	.value("Oct", QuantLib::Oct)
	.value("Nov", QuantLib::Nov)
	.value("Dec", QuantLib::Dec)
	;	
}

void export_QR_Utility()
{
    class_<Utility>("Utility", init<>())
//	.staticmethod("string2Date")
	;
}

