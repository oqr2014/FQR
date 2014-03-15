
#ifndef _QR_EURO_OPTION_HPP_
#define _QR_EURO_OPTION_HPP_

#include "option.hpp"

namespace QR 
{

class EuroOption; 
typedef boost::shared_ptr<EuroOption> EuroOptionPtr; 

class EuroOption : public Option { 
public: 
    EuroOption() : Option() {}  
    EuroOption(const EuroOption& option_); 
    EuroOption& operator=(const EuroOption& option_); 

    EuroOption(
		Type    type_,
		const QuantLib::Date&  valueDate_,
		const QuantLib::Date&  maturityDate_,
		double  S_,
		double  K_,
		double  sigma_,
		double  r_); 
			
    EuroOption(
		Type    type_,
		double  S_,
		double  K_,
		double  T_,
		double  sigma_,
		double  r_);

	double getd1() const { return _d1; }	
	double getd2() const { return _d2; }
	double getN_d1() const { return _N_d1; }
	double getN_d2() const { return _N_d2; }
	double getn_d1() const { return _n_d1; }
	double getn_d2() const { return _n_d2; }
	
	void setd1(double d1_)    { _d1 = d1_; }
	void setd2(double d2_)    { _d2 = d2_; }
	void setN_d1(double N_d1_) { _N_d1 = N_d1_; }
	void setN_d2(double N_d2_) { _N_d2 = N_d2_; }
	void setn_d1(double n_d1_) { _n_d1 = n_d1_; }
	void setn_d2(double n_d2_) { _n_d2 = n_d2_; }
		
	virtual void init(); 
	virtual void calcPrice(); 
	virtual void calcDelta(double pct_ = .005);  //default to shake 0.5% 
	virtual void calcVega(double pct_ = .005);
	virtual void calcGamma(double pct_ = .005);
	virtual void calcGreeksAnalytic(); 
	virtual void calcImplVol(); 
	virtual void calc(); 
private: 
    double  _d1, _d2;  // intermediate results 
	double  _N_d1, _N_d2;  // N(d1), N(d2) 
	double  _n_d1, _n_d2;  // n(d1), n(d2) 
}; 


std::ostream& operator<<( std::ostream& out_, const EuroOption& option_); 

}

#endif 

