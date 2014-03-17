#ifndef _QR_GREEKS_H_
#define _QR_GREEKS_H_
#include <string>
#include <iostream>
#include <boost/shared_ptr.hpp>

namespace QR {
class Greeks;
typedef boost::shared_ptr<Greeks> GreeksPtr; 

class Greeks {
public:
    Greeks(); 
    Greeks(const Greeks& greeks_); 
    Greeks& operator=(const Greeks& greeks_); 

	Greeks(
    	double  delta_,
    	double  vega_, 
    	double  gamma_,
    	double  theta_,
    	double  rho_, 
		double  deltaA_,
		double  vegaA_, 
		double  gammaA_,
		double  thetaA_,
		double  rhoA_); 

    double getDelta() const { return _delta; }
    double getVega() const  { return _vega; }
    double getGamma() const { return _gamma; }
    double getTheta() const { return _theta; }
    double getRho() const   { return _rho; }

    double getDeltaA() const { return _deltaA; }
    double getVegaA() const  { return _vegaA; }
    double getGammaA() const { return _gammaA; }
    double getThetaA() const { return _thetaA; }
    double getRhoA() const   { return _rhoA; }

    void setDelta(double delta_) { _delta = delta_; }
    void setVega(double vega_)   { _vega = vega_; }
    void setGamma(double gamma_) { _gamma = gamma_; }
    void setTheta(double theta_) { _theta = theta_; }
    void setRho(double rho_)     { _rho = rho_; }
    
    void setDeltaA(double deltaA_) { _deltaA = deltaA_; }
    void setVegaA(double vegaA_)   { _vegaA = vegaA_; }
    void setGammaA(double gammaA_) { _gammaA = gammaA_; }
    void setThetaA(double thetaA_) { _thetaA = thetaA_; }
    void setRhoA(double rhoA_)     { _rhoA = rhoA_; }

private: 
    double  _delta; 
    double  _vega; 
    double  _gamma; 
    double  _theta; 
    double  _rho; 
    double  _deltaA; // Analytical  
    double  _vegaA;  // Analytical  
    double  _gammaA; // Analytical 
    double  _thetaA; // Analytical 
    double  _rhoA;   // Analytical 
};

std::ostream& operator<<(std::ostream& out_, const Greeks& greeks_);
 
}

#endif 
