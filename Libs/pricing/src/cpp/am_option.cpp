#include <cmath>
#include "am_option.hpp"

namespace QR 
{

AmOption::AmOption(const AmOption& option_) 
{
	*this = option_; 
} 

AmOption& AmOption::operator=(const AmOption& option_) 
{
	if (this == &option_)
		return *this; 
	Option::operator=(option_);  
	_euroOption = option_._euroOption; 
	return *this;    
}


AmOption::AmOption(
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
			
AmOption::AmOption(
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

void AmOption::init()
{
	_euroOption = EuroOption(
					_type, 
					_S, 
					_K, 
					_T, 
					_sigma,
					_r,
					_q);
	_euroOption.init(); 
	_initFlag = 1; 
} 

double AmOption::criticalPrice(double tolerance_)
{
	double riskFreeDF = std::exp(-_r * _T); 
	double variance = _sigma * _sigma; 
	double n = 2.0 * _r * _T / variance;
	double m = 2.0 * _r * _T / variance;
	double bT = _r * _T;
	double  qu, Su, h, Si;
	switch (_type) {
	case Option::CALL:
		qu = (-(n-1.0) + std::sqrt(((n-1.0)*(n-1.0)) + 4.0*m))/2.0;
		Su = _K / (1.0 - 1.0/qu);
		h = -(bT + 2.0 * _sigma) * _K / (Su - _K);
		Si = _K + (Su - _K) * (1.0 - std::exp(h));
		break;
	case Option::PUT:
		qu = (-(n-1.0) - std::sqrt(((n-1.0)*(n-1.0)) + 4.0*m))/2.0;
		Su = _K / (1.0 - 1.0/qu);
		h = (bT - 2.0*_sigma) * _K / (_K - Su);
		Si = Su + (_K - Su) * std::exp(h);
		break;
	default:
		QL_FAIL("unknown option type");
	}

// Newton Raphson algorithm for finding critical price Si
	double Q, LHS, RHS, bi;
	double forwardSi = Si / riskFreeDF;
	double d1 = (std::log(forwardSi/_K) + 0.5*variance) / _sigma;
	QuantLib::CumulativeNormalDistribution cumNormalDist;
	double K = (riskFreeDF != 1.0) ?  2.0*_r*_T / (variance * (1.0 - riskFreeDF)) : 0.0;
	QuantLib::Option::Type option_type = (_type==Option::CALL)? QuantLib::Option::Call : QuantLib::Option::Put; 
	double temp = QuantLib::blackFormula(option_type, _K, forwardSi, _sigma) * riskFreeDF;
	switch (_type) {
	case Option::CALL:
		Q = (-(n-1.0) + std::sqrt(((n-1.0)*(n-1.0)) + 4 * K)) / 2;
		LHS = Si - _K;
		RHS = temp + (1 - cumNormalDist(d1)) * Si / Q;
		bi =  cumNormalDist(d1) * (1 - 1/Q) + (1 - cumNormalDist.derivative(d1) / _sigma) / Q;
		while (std::fabs(LHS - RHS)/_K > tolerance_) {
			Si = (_K + RHS - bi * Si) / (1 - bi);
			forwardSi = Si / riskFreeDF;
			d1 = (std::log(forwardSi / _K) + 0.5 * variance) / _sigma;
			LHS = Si - _K;
			double temp2 = blackFormula(option_type, _K, forwardSi, _sigma) * riskFreeDF;
			RHS = temp2 + (1 - cumNormalDist(d1)) * Si / Q;
			bi = cumNormalDist(d1) * (1 - 1 / Q) + (1 - cumNormalDist.derivative(d1) / _sigma) / Q;
		}
		break;
	case Option::PUT:
		Q = (-(n-1.0) - std::sqrt(((n-1.0)*(n-1.0)) + 4 * K)) / 2;
		LHS = _K - Si;
		RHS = temp - (1 - cumNormalDist(-d1)) * Si / Q;
		bi = - cumNormalDist(-d1) * (1 - 1/Q) - (1 + cumNormalDist.derivative(-d1) / _sigma) / Q;
		while (std::fabs(LHS - RHS)/_K > tolerance_) {
			Si = (_K - RHS + bi * Si) / (1 + bi);
			forwardSi = Si / riskFreeDF;
			d1 = (std::log(forwardSi/_K) + 0.5*variance) / _sigma;
			LHS = _K - Si;
			double temp2 = blackFormula(option_type, _K, forwardSi, _sigma) * riskFreeDF;
			RHS = temp2 - (1 - cumNormalDist(-d1)) * Si / Q;
			bi = - cumNormalDist(-d1) * (1 - 1 / Q) - (1 + cumNormalDist.derivative(-d1) / _sigma) / Q;
		}
		break;
	default:
		QL_FAIL("unknown option type");
	}
	return Si;
}

void AmOption::calcPrice() 
{ 
	if ( !_initFlag ) 
		init(); 
	if( Option::CALL == _type ) { 
// assume no dividend, european option call = american option   
		_euroOption.calcPrice(); 
		_price = _euroOption.getPrice(); 
		return; 
	} 
	// early exercise may be optimal for PUT 
	QuantLib::CumulativeNormalDistribution cumNormalDist;
	double tolerance = 1e-6;
	double Sk = criticalPrice(tolerance);
	double riskFreeDF = std::exp(-_r * _T); 
	double forwardSk = Sk / riskFreeDF;
	double variance = _sigma * _sigma; 
	double d1 = (std::log(forwardSk / _K) + 0.5 * variance) / _sigma;
	double n = 2.0 * _r * _T / variance;
	double K = 2.0 * _r *_T / (variance * (1.0 - riskFreeDF));
	double Q, a;
	switch (_type) {
	case Option::CALL:
		Q = (-(n-1.0) + std::sqrt(((n-1.0)*(n-1.0))+4.0*K))/2.0;
		a =  (Sk/Q) * (1.0 - cumNormalDist(d1));
		if (_S < Sk) {
			_euroOption.calcPrice(); 
			_price = _euroOption.getPrice() + a * std::pow((_S/Sk), Q);
		}
		else
			_price = _S - _K;
		break;
	case Option::PUT:
		Q = (-(n-1.0) - std::sqrt(((n-1.0)*(n-1.0))+4.0*K))/2.0;
		a = -(Sk/Q) * (1.0 - cumNormalDist(-d1));
		if (_S > Sk) {
			_euroOption.calcPrice(); 
			_price = _euroOption.getPrice() + a * std::pow((_S/Sk), Q);
		} 
		else 
			_price = _K - _S;
		break;
	default:
		QL_FAIL("unknown option type");
	}
}

void AmOption::calc() 
{
	if ( !_initFlag )
		init(); 
	calcPrice(); 
//	calcGreeksAnalytic(); 
}

std::ostream& operator<<(std::ostream& out_, const AmOption& option_)
{ 
    out_ << (Option)(option_);     
    return out_; 
} 

}

