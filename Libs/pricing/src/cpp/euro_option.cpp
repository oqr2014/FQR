#include <cmath>
#include "euro_option.hpp"

namespace QR 
{

EuroOption::EuroOption(const EuroOption& option_) 
{
    *this = option_; 
} 

EuroOption& EuroOption::operator=(const EuroOption& option_) 
{
    if (this == &option_)
        return *this; 
    Option::operator=(option_);  
    _d1   = option_._d1; 
    _d2   = option_._d2; 
	_N_d1 = option_._N_d1; 
	_N_d2 = option_._N_d2; 
	_n_d1 = option_._n_d1; 
	_n_d2 = option_._n_d2; 
    return *this;    
}


EuroOption::EuroOption(
		Type    type_,
		const QuantLib::Date&  valueDate_,
		const QuantLib::Date&  maturityDate_,
		double  S_,
		double  K_,
		double  sigma_,
		double  r_,
		double  q_) : 
	Option(
		type_,
		valueDate_,
		maturityDate_, 
		S_,
	    K_,
		sigma_,
		r_, 
		q_)
{} 
			
EuroOption::EuroOption(
		Type    type_,
		double  S_,
		double  K_,
		double  T_,
		double  sigma_,
		double  r_,
		double  q_) :
	Option(
		type_,
		S_,
	    K_,
		T_,
		sigma_,
		r_, 
		q_)
{}

void EuroOption::init()
{
	
	QL_REQUIRE(_K >= 0.0, "strike (" << _K << ") must be non-negative");
	QL_REQUIRE(_sigma >= 0.0, "sigma (" << _sigma << ") must be non-negative");

	if (_sigma >= QL_EPSILON) {
		if (QuantLib::close(_K, 0.0)) {
			_d1   = QL_MAX_REAL;
			_d2   = QL_MAX_REAL;
			_N_d1 = 1.0;
			_N_d2 = 1.0;
			_n_d1 = 0.0;
			_n_d2 = 0.0;
		} 
		else {
			_d1 = (std::log(_S / _K) + (_r + 0.5 * _sigma * _sigma) * _T) / (_sigma * std::sqrt(_T));
			_d2 = _d1 - _sigma * std::sqrt(_T);
			QuantLib::CumulativeNormalDistribution cnd;
			_N_d1 = cnd(_d1);
			_N_d2 = cnd(_d2);
			_n_d1 = cnd.derivative(_d1);
			_n_d2 = cnd.derivative(_d2);
		}
	} 
	else {  //vol = 0
		if (QuantLib::close(_S, _K)) {
			_d1   = 0;
			_d2   = 0;
			_N_d1 = 0.5;
			_N_d2 = 0.5;
			_n_d1 = M_SQRT_2 * M_1_SQRTPI;
			_n_d2 = M_SQRT_2 * M_1_SQRTPI;
		} 
		else if (_S > _K) {
			_d1   = QL_MAX_REAL;
			_d2   = QL_MAX_REAL;
			_N_d1 = 1.0;
			_N_d2 = 1.0;
			_n_d1 = 0.0;
			_n_d2 = 0.0;
		} 
		else { //_S < _K
			_d1   = QL_MIN_REAL;
			_d2   = QL_MIN_REAL;
			_N_d1 = 0.0;
			_N_d2 = 0.0;
			_n_d1 = 0.0;
			_n_d2 = 0.0;
		}
	}
	_initFlag = 1; 
} 

void EuroOption::calcPrice() 
{ 
	if ( !_initFlag ) 
		init(); 
    double call = _S * _N_d1 - _K * std::exp(-_r * _T) * _N_d2;   
	switch (_type) {
	case Option::CALL :
		_price = call; 
		break;
	case Option::PUT :
		_price = _K * std::exp(-_r*_T) - _S + call; 
		break;
	default:
		QL_FAIL("invalid option type!");
	}
}

void EuroOption::calcDelta(double pct_) 
{
	EuroOption option1 = *this; 
	EuroOption option2 = *this; 
	option1.setSpot( (1 - pct_) * _S );
	option2.setSpot( (1 + pct_) * _S );
	option1.calcPrice(); 
	option2.calcPrice();
	double delta = ( option2.getPrice() - option1.getPrice() ) / ( 2 * pct_ * _S ); 
	_greeks.setDelta(delta); 
}

void EuroOption::calcVega(double pct_) 
{
	EuroOption option1 = *this; 
	EuroOption option2 = *this; 
	option1.setVol( (1 - pct_) * _sigma );
	option2.setVol( (1 + pct_) * _sigma );
	option1.calcPrice(); 
	option2.calcPrice();
	double vega = ( option2.getPrice() - option1.getPrice() ) / ( 2 * pct_ * _sigma ); 
	_greeks.setVega(vega); 
}

void EuroOption::calcGamma(double pct_) 
{
	EuroOption option1 = *this; 
	EuroOption option2 = *this; 
	option1.setSpot( (1 - pct_) * _S );
	option2.setSpot( (1 + pct_) * _S );
	option1.calcPrice(); 
	option2.calcPrice();
	calcPrice(); 
	double gamma = ( option1.getPrice() + option2.getPrice() - 2 * _price ) / ( pct_ * _S * pct_ * _S ); 
	_greeks.setGamma(gamma); 
}

void EuroOption::calcTheta(double pct_)
{
	EuroOption option1 = *this; 
	EuroOption option2 = *this; 
	option1.setT2M( (1 - pct_) * _T );
	option2.setT2M( (1 + pct_) * _T );
	option1.calcPrice(); 
	option2.calcPrice();
	double theta = ( option1.getPrice() - option2.getPrice() ) / ( 2 * pct_ * _T ); 
	_greeks.setTheta(theta); 
}

void EuroOption::calcRho(double pct_)
{
	EuroOption option1 = *this; 
	EuroOption option2 = *this; 
	option1.setRate( (1 - pct_) * _r );
	option2.setRate( (1 + pct_) * _r );
	option1.calcPrice(); 
	option2.calcPrice();
	double rho = ( option2.getPrice() - option1.getPrice() ) / ( 2 * pct_ * _r ); 
	_greeks.setRho(rho); 
}

void EuroOption::calcGreeksAnalytic()
{
	if ( !_initFlag ) 
		init(); 

	_greeks.setVega( _S * _n_d1 * std::sqrt(_T) );
	_greeks.setGamma( _n_d1 / (_S * _sigma * std::sqrt(_T)) ); 
	switch (_type) {
	case Option::CALL :
		_greeks.setDelta( _N_d1 );
		_greeks.setTheta( -_S * _n_d1 * _sigma / ( 2*std::sqrt(_T) ) - _r * _K * std::exp(-_r*_T) * _N_d2 ); 
		_greeks.setRho( _K * _T * std::exp(-_r*_T) * _N_d2 );  
		break;
	case Option::PUT :
		_greeks.setDelta( _N_d1 - 1 );
		_greeks.setTheta( -_S * _n_d1 * _sigma / ( 2*std::sqrt(_T) ) + _r * _K * std::exp(-_r*_T) * (1-_N_d2) ); 
		_greeks.setRho( -_K * _T * std::exp(-_r*_T) * (1-_N_d2) );  
		break;
	default:
		QL_FAIL("invalid option type!");
	}
}

void EuroOption::calcImplVol()
{
	
}

void EuroOption::calc() 
{
	if ( !_initFlag )
		init(); 
	calcPrice(); 
	calcGreeksAnalytic(); 
}

std::ostream& operator<<(std::ostream& out_, const EuroOption& option_)
{ 
    out_ << (Option)(option_);     
    out_ << "d1=" << option_.getd1() << std::endl; 
    out_ << "d2=" << option_.getd2() << std::endl; 
    out_ << "N_d1=" << option_.getN_d1() << std::endl; 
    out_ << "N_d2=" << option_.getN_d2() << std::endl; 
    out_ << "n_d1=" << option_.getn_d1() << std::endl; 
    out_ << "n_d2=" << option_.getn_d2() << std::endl; 
    return out_; 
} 

}

