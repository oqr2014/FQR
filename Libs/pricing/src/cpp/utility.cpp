
#include "utility.hpp"

namespace QR
{

void Utility::trimLeft(std::string& str_)
{
	if (0 == str_.size())
		return; 
	size_t i; 
	for(i = 0; i < str_.size(); i++)
	{
		if( ' ' == str_[i] || 
			'\n' == str_[i] ||
			'\r' == str_[i] ||
			'\t' == str_[i])
			continue;
		break; 
	}
	str_ = str_.substr(i);  
} 

void Utility::trimRight(std::string& str_)
{
	if (0 == str_.size())
		return; 
	size_t i; 
	for(i = str_.size()-1; i >= 0; i--)
	{
		if( ' ' == str_[i] || 
			'\n' == str_[i] ||
			'\r' == str_[i] ||
			'\t' == str_[i])
			continue;
		break; 
	}
	str_ = str_.substr(0, i+1);  
}

void Utility::trimBoth(std::string& str_)
{
	trimLeft(str_); 
	trimRight(str_);
}

QuantLib::Date Utility::str2Date(const std::string &str_)
{
// support this format "MM/DD/YYYY" only e.g. 03/17/2014
	QuantLib::Date date;
	std::string str = str_; 
	trimBoth(str); 
	if(0 == str.size())
		return QuantLib::Date(); 
	size_t loc = str.find("/");
	if (loc != std::string::npos) {
		size_t loc2 = str.find("/", loc+1);
		if (loc2 == std::string::npos) 
			return QuantLib::Date(); 
		int month = std::atoi(str.substr(0, loc).c_str()); 
		if (month < 1 || month > 12)
			return QuantLib::Date(); 
		int day = std::atoi(str.substr(loc+1, loc2-loc).c_str());
		int year = std::atoi(str.substr(loc2+1).c_str()); 
		return QuantLib::Date(day, static_cast<QuantLib::Month>(month), year);  
	}
	return QuantLib::Date(); 

}

std::istream& operator>>(std::istream& in_, QuantLib::Date& date_)
{ // format: month/day/year e.g. 03/17/2014
	int day, month, year; 
	std::string str; 
	in_ >> str; 
	date_ = Utility::str2Date(str); 
	return in_; 
}

}
