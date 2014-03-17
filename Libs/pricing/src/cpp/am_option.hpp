// American option pricing 

#ifndef _QR_AM_OPTION_HPP_
#define _QR_AM_OPTION_HPP_

#include "option.hpp"
#include "euro_option.hpp"

namespace QR 
{

class AmOption; 
typedef boost::shared_ptr<AmOption> AmOptionPtr; 

class AmOption : public Option { 
public: 
    AmOption() : Option() {}  
    AmOption(const AmOption& option_); 
    AmOption& operator=(const AmOption& option_); 

    AmOption(
		Type    type_,
		const QuantLib::Date&  valueDate_,
		const QuantLib::Date&  maturityDate_,
		double  S_,
		double  K_,
		double  sigma_,
		double  r_, 
		double  q_); 
			
    AmOption(
		Type    type_,
		double  S_,
		double  K_,
		double  T_,
		double  sigma_,
		double  r_, 
		double  q_);

	virtual ~AmOption() {} 
//	virtual AmOptionPtr clone() const { return AmOptionPtr(new AmOption(*this)); }
	virtual AmOption* clone() const { return new AmOption(*this); }
	 
	virtual void init(); 
	virtual void calcPrice(); 
	virtual void calcGreeksAnalytic() {}
	virtual void calc(); 

private: 
	virtual double criticalPrice(double tolerance_); 
	EuroOption _euroOption;  //without dividend, American option call = European option call 
}; 


std::ostream& operator<<( std::ostream& out_, const AmOption& option_); 

}

#endif 

