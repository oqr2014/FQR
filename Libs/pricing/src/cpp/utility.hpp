
#ifndef _QR_UTILITY_HPP_
#define _QR_UTILITY_HPP_

#include <iostream>
#include <string>
#include <boost/shared_ptr.hpp>
#include <ql/quantlib.hpp>

namespace QR 
{

class QRException : public std::exception 
{
public: 
	explicit QRException(const std::string& msg_): 
	std::exception(), 
	_msg(msg_) {}
	 
	virtual ~QRException() throw() {}

	virtual const char* what() const throw() 
	{
		return _msg.c_str(); 
	}
private: 
	std::string _msg; 
}; 

class Utility {
public: 
	static void trimLeft(std::string& str_); 
	static void trimRight(std::string& str_); 
	static void trimBoth(std::string& str_); 
	static QuantLib::Date string2Date(const std::string &str_);       

private: 
	Utility(); 
	Utility(const Utility &util_); 
	~Utility(); 
};  

std::istream& operator>>(std::istream& in_, QuantLib::Date& date_); 	

}

#endif

