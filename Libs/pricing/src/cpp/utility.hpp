
#ifndef _QR_UTILITY_HPP_
#define _QR_UTILITY_HPP_

#include <iostream>
#include <string>
#include <boost/shared_ptr.hpp>
#include <ql/quantlib.hpp>

namespace QR 
{

std::istream& operator>>(std::istream& in_, QuantLib::Date& date_); 	
	
}

#endif

