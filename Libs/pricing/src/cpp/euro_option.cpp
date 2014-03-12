#include <cmath>
#include "euro_option.hpp"

namespace QR {

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
		double  r_) : 
	Option(
		type_,
		valueDate_,
		maturityDate_, 
		S_,
	    K_,
		sigma_,
		r_)
{} 
			
EuroOption::EuroOption(
		Type    type_,
		double  S_,
		double  K_,
		double  T_,
		double  sigma_,
		double  r_) :
	Option(
		type_,
		S_,
	    K_,
		T_,
		sigma_,
		r_)
{}

EuroOption::initialize()
{
	
	QL_REQUIRE(_K >= 0.0, "strike (" << _K << ") must be non-negative");
	QL_REQUIRE(_sigma >= 0.0, "sigma (" << _sigma << ") must be non-negative");

	if (_sigma >= QL_EPSILON) {
		if (close(_K, 0.0)) {
			_d1   = QL_MAX_REAL;
			_d2   = QL_MAX_REAL;
			_N_d1 = 1.0;
			_N_d2 = 1.0;
			_n_d1 = 0.0;
			_n_d2 = 0.0;
		} 
		else {
			_d1 = (std::log(_S / _K) + (_r + 0.5 * _sigma * _sigma) * _T) / (_sigma * std::sqrt(_T));
			_d2 = d1_ - _sigma * std::sqrt(_T);
			QuantLib::CumulativeNormalDistribution cnd;
			_N_d1 = cnd(_d1);
			_N_d2 = cnd(_d2);
			_n_d1 = cnd.derivative(_d1);
			_n_d2 = cnd.derivative(_d2);
		}
	} 
	else {  //vol = 0
		if (close(_S, _K)) {
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

	switch (_type) {
	case Option::Call:
		alpha_     =  cum_d1_;//  N(d1)
		DalphaDd1_ =    n_d1_;//  n(d1)
		beta_      = -cum_d2_;// -N(d2)
		DbetaDd2_  = -  n_d2_;// -n(d2)
		break;
	case Option::Put:
		alpha_     = -1.0+cum_d1_;// -N(-d1)
		DalphaDd1_ =        n_d1_;//  n( d1)
		beta_      =  1.0-cum_d2_;//  N(-d2)
		DbetaDd2_  =     -  n_d2_;// -n( d2)
		break;
	default:
		QL_FAIL("invalid option type!");
	}
}


std::ostream& operator<<(std::ostream& out_, const EuroOption& option_)
{ 
    out_ << (Option)(option_);     
    out_ << "d1=" << option_.getd1() << std::endl; 
    out_ << "d2=" << option_.getd2() << std::endl; 
    return out_; 
} 

}

