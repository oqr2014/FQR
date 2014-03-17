
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
	_type         = option_._type; 
    _valueDate    = option_._valueDate; 
    _maturityDate = option_._maturityDate;  
    _S            = option_._S; 
    _K            = option_._K; 
    _T            = option_._T; 
    _sigma        = option_._sigma; 
    _r            = option_._r; 
    _q            = option_._q; 
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
    double  r_,
	double  q_) :   
    _type(type_),  
    _valueDate(valueDate_),  
    _maturityDate(maturityDate_),  
    _S (S_),  
    _K(K_),  
    _sigma(sigma_),  
    _r(r_),
    _q(q_),
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
    double  r_,
	double  q_) :
    _type(type_),  
    _S(S_),  
    _K(K_),  
    _T(T_),  
    _sigma(sigma_),  
    _r(r_),      
    _q(q_),
    _dayCounter(QuantLib::Actual365Fixed()), 
    _initFlag(0) {}
    
std::string Option::getTypeName() const 
{
    if (_type == PUT) 
        return std::string("PUT");
    else
        return std::string("CALL");  
}

void Option::calcDelta(double pct_) 
{
	OptionPtr option1(this->clone());
	OptionPtr option2(this->clone());
	option1->setSpot( (1 - pct_) * _S );
	option2->setSpot( (1 + pct_) * _S );
	option1->calcPrice(); 
	option2->calcPrice();
	double delta = ( option2->getPrice() - option1->getPrice() ) / ( 2 * pct_ * _S ); 
	_greeks.setDelta(delta); 
}

void Option::calcVega(double pct_) 
{
	OptionPtr option1(this->clone());
	OptionPtr option2(this->clone());
	option1->setVol( (1 - pct_) * _sigma );
	option2->setVol( (1 + pct_) * _sigma );
	option1->calcPrice(); 
	option2->calcPrice();
	double vega = ( option2->getPrice() - option1->getPrice() ) / ( 2 * pct_ * _sigma ); 
	_greeks.setVega(vega); 
}

void Option::calcGamma(double pct_) 
{
	OptionPtr option1(this->clone());
	OptionPtr option2(this->clone());
	option1->setSpot( (1 - pct_) * _S );
	option2->setSpot( (1 + pct_) * _S );
	option1->calcPrice(); 
	option2->calcPrice();
	calcPrice(); 
	double gamma = ( option1->getPrice() + option2->getPrice() - 2 * _price ) / ( pct_ * _S * pct_ * _S ); 
	_greeks.setGamma(gamma); 
}

void Option::calcTheta(double pct_)
{
	OptionPtr option1(this->clone());
	OptionPtr option2(this->clone());
	option1->setT2M( (1 - pct_) * _T );
	option2->setT2M( (1 + pct_) * _T );
	option1->calcPrice(); 
	option2->calcPrice();
	double theta = ( option1->getPrice() - option2->getPrice() ) / ( 2 * pct_ * _T ); 
	_greeks.setTheta(theta); 
}

void Option::calcRho(double pct_)
{
	OptionPtr option1(this->clone());
	OptionPtr option2(this->clone());
	option1->setRate( (1 - pct_) * _r );
	option2->setRate( (1 + pct_) * _r );
	option1->calcPrice(); 
	option2->calcPrice();
	double rho = ( option2->getPrice() - option1->getPrice() ) / ( 2 * pct_ * _r ); 
	_greeks.setRho(rho); 
}

double Option::calcImplVol(double price_) 
{
	QuantLib::Bisection bisection; 
	double accuracy = 1.e-6;
	double guess = 0.15; 
	double xmin = 1.e-5; 
	double xmax = 5.; 
	double impl_vol = bisection.solve(
					FunctorImplVol(this, price_), 
					accuracy, 
					guess, 
					xmin, 
					xmax); 
	return impl_vol; 
}

std::ostream& operator<<(std::ostream& out_, const Option& option_) 
{
    out_ << "Type=" << option_.getTypeName() << std::endl; 
    out_ << "ValueDate=" << option_.getValueDate() << std::endl; 
    out_ << "MaturityDate=" << option_.getMaturityDate() << std::endl; 
    out_ << "Spot=" << option_.getSpot() << std::endl; 
    out_ << "Strike=" << option_.getStrike() << std::endl; 
    out_ << "T2M=" << option_.getT2M() << std::endl; 
    out_ << "Volatility=" << option_.getVol() << std::endl; 
    out_ << "Risk free rate=" << option_.getRate() << std::endl; 
    out_ << "Dividend yield=" << option_.getDivYield() << std::endl; 
    out_ << "DayCounter=" << option_.getDCC().name() << std::endl; 
    out_ << "InitFlag=" << option_.getInitFlag() << std::endl; 
    out_ << "Price=" << option_.getPrice() << std::endl; 
    out_ << "Greeks=" << option_.getGreeks() << std::endl; 
    return out_; 
}

double FunctorImplVol::operator() (double vol_) const 
{
	OptionPtr optPtr(_optionPtr->clone());
	optPtr->setVol(vol_);
	optPtr->calcPrice();
	double f = optPtr->getPrice() - _price;
	return f;
}

}

