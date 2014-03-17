#include "greeks.hpp"

namespace QR {

Greeks::Greeks() {}

Greeks::Greeks(const Greeks& greeks_) {
    *this = greeks_; 
} 
    
Greeks& Greeks::operator=(const Greeks& greeks_) {
    if (this == &greeks_)
        return *this; 
    _delta  = greeks_._delta;
    _vega   = greeks_._vega; 
    _gamma  = greeks_._gamma;
    _theta  = greeks_._theta;
    _rho    = greeks_._rho; 
    _deltaA = greeks_._deltaA;
    _vegaA  = greeks_._vegaA; 
    _gammaA = greeks_._gammaA;
    _thetaA = greeks_._thetaA;
    _rhoA   = greeks_._rhoA; 
    return *this; 
}    
    
Greeks::Greeks(
    double  delta_,
    double  vega_, 
    double  gamma_,
    double  theta_,
    double  rho_, 
    double  deltaA_,
    double  vegaA_, 
    double  gammaA_,
    double  thetaA_,
    double  rhoA_) : 
    _delta(delta_),
    _vega(vega_),
    _gamma(gamma_),
    _theta(theta_),
    _rho(rho_), 
    _deltaA(deltaA_),
    _vegaA(vegaA_),
    _gammaA(gammaA_),
    _thetaA(thetaA_),
    _rhoA(rhoA_) 
{}

std::ostream& operator<<(std::ostream& out_, const Greeks& greeks_)
{
	out_ << "delta="  << greeks_.getDelta() << std::endl; 
	out_ << "vega="   << greeks_.getVega()  << std::endl; 
	out_ << "gamma="  << greeks_.getGamma() << std::endl; 
	out_ << "theta="  << greeks_.getTheta() << std::endl; 
	out_ << "rho="    << greeks_.getRho()   << std::endl; 
	out_ << "deltaA=" << greeks_.getDeltaA() << std::endl; 
	out_ << "vegaA="  << greeks_.getVegaA()  << std::endl; 
	out_ << "gammaA=" << greeks_.getGammaA() << std::endl; 
	out_ << "thetaA=" << greeks_.getThetaA() << std::endl; 
	out_ << "rhoA="   << greeks_.getRhoA()   << std::endl; 
	return out_; 	
}

}
