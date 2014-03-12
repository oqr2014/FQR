#include "greeks.hpp"

namespace QR {

Greeks::Greeks() {}

Greeks::Greeks(const Greeks& greeks_) {
    *this = greeks_; 
} 
    
Greeks& Greeks::operator=(const Greeks& greeks_) {
    if (this == &greeks_)
        return *this; 
    _delta = greeks_._delta;
    _vega  = greeks_._vega; 
    _gamma = greeks_._gamma;
    _theta = greeks_._theta;
    _rho   = greeks_._rho; 
    return *this; 
}    
    
Greeks::Greeks(
    double  delta_,
    double  vega_, 
    double  gamma_,
    double  theta_,
    double  rho_) : 
    _delta(delta_),
    _vega(vega_),
    _gamma(gamma_),
    _theta(theta_),
    _rho(rho_) 
{}

std::ostream& operator<<(std::ostream& out_, const Greeks& greeks_)
{
	out_ << "delta=" << greeks_.getDelta() << std::endl; 
	out_ << "vega="  << greeks_.getVega()  << std::endl; 
	out_ << "gamma=" << greeks_.getGamma() << std::endl; 
	out_ << "theta=" << greeks_.getTheta() << std::endl; 
	out_ << "rho="   << greeks_.getRho()   << std::endl; 
	return out_; 	
}

}
