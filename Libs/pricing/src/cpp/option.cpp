
#include "option.hpp"

namespace QR 
{

Option::Option() :
_dayCounter(QuantLib::Actual365Fixed()), 
_initFlag(0) {} 


Option::Option(const Option& option_) 
{
    *this = option_; 
} 


Option& Option::operator=(const Option& option_) 
{
    if (this == &option_) 
        return *this;  
    _valueDate    = option_._valueDate; 
    _maturityDate = option_._maturityDate;  
    _S            = option_._S; 
    _K            = option_._K; 
    _T            = option_._T; 
    _sigma        = option_._sigma; 
    _r            = option_._r; 
    _dayCounter   = option_._dayCounter; 
    _initFlag     = option_._initFlag;    
	_price        = option_._price; 
	_greeks       = option_._greeks; 
    return *this; 
} 


Option::Option(
    Type type_, 
    const QuantLib::Date&  valueDate_,               
    const QuantLib::Date&  maturityDate_,               
    double  S_, 
    double  K_,
    double  sigma_, 
    double  r_) :   
    _type(type_),  
    _valueDate(valueDate_),  
    _maturityDate(maturityDate_),  
    _S (S_),  
    _K(K_),  
    _sigma(sigma_),  
    _r(r_),
    _dayCounter(QuantLib::Actual365Fixed()), 
    _initFlag(0) 
{
	_T = _dayCounter.yearFraction(_valueDate, _maturityDate);
}  

 
Option::Option(
    Type    type_, 
    double  S_, 
    double  K_,
    double  T_, 
    double  sigma_, 
    double  r_) :
    _type(type_),  
    _S(S_),  
    _K(K_),  
    _T(T_),  
    _sigma(sigma_),  
    _r(r_),      
    _dayCounter(QuantLib::Actual365Fixed()), 
    _initFlag(0) {}
    

std::string Option::getTypeName() const 
{
    if (_type == PUT) 
        return std::string("PUT");
    else
        return std::string("CALL");  
}

   
std::ostream& operator<<(std::ostream& out_, const Option& option_) 
{
    out_ << "Type=" << option_.getTypeName() << std::endl; 
    out_ << "ValueDate=" << option_.getValueDate() << std::endl; 
    out_ << "MaturityDate=" << option_.getMaturityDate() << std::endl; 
    out_ << "Spot=" << option_.getSpot() << std::endl; 
    out_ << "Time2Maturity=" << option_.getTime2Maturity() << std::endl; 
    out_ << "Volatility=" << option_.getVol() << std::endl; 
    out_ << "Rate=" << option_.getRate() << std::endl; 
    out_ << "DayCounter=" << option_.getDCC().name() << std::endl; 
    out_ << "IniFlag=" << option_.getInitFlag() << std::endl; 
    out_ << "Price=" << option_.getPrice() << std::endl; 
    out_ << "Greeks=" << option_.getGreeks() << std::endl; 
    return out_; 
}

}


