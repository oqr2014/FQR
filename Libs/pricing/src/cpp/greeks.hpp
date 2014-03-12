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
    	double  rho_); 

    double getDelta() const { return _delta; }
    double getVega() const  { return _vega; }
    double getGamma() const { return _gamma; }
    double getTheta() const { return _theta; }
    double getRho() const   { return _rho; }

    void setDelta(double delta_) { _delta = delta_; }
    void setVega(double vega_)   { _vega = vega_; }
    void setGamma(double gamma_) { _gamma = gamma_; }
    void setTheta(double theta_) { _theta = theta_; }
    void setRho(double rho_)     { _rho = rho_; }
    
private: 
    double  _delta; 
    double  _vega; 
    double  _gamma; 
    double  _theta; 
    double  _rho; 
};

std::ostream& operator<<(std::ostream& out_, const Greeks& greeks_);
 
}

#endif 
