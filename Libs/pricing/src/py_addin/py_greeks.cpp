/***********************************************
 * boost python wrapper for greeks.hpp 
 ***********************************************/
#include "py_addin.hpp"

using namespace boost::python; 
using namespace QR; 

void export_QR_Greeks()
{
    class_<Greeks>("Greeks", init<>())
    .def(init<const Greeks&>()) 
    .def(init<double,double,double,double,double,double,double,double,double,double>())
    .add_property("delta", &Greeks::getDelta, &Greeks::setDelta) 
    .add_property("vega", &Greeks::getVega, &Greeks::setVega) 
    .add_property("gamma", &Greeks::getGamma, &Greeks::setGamma) 
    .add_property("theta", &Greeks::getTheta, &Greeks::setTheta) 
    .add_property("rho", &Greeks::getRho, &Greeks::setRho) 
    .add_property("deltaA", &Greeks::getDeltaA, &Greeks::setDeltaA) 
    .add_property("vegaA", &Greeks::getVegaA, &Greeks::setVegaA) 
    .add_property("gammaA", &Greeks::getGammaA, &Greeks::setGammaA) 
    .add_property("thetaA", &Greeks::getThetaA, &Greeks::setThetaA) 
    .add_property("rhoA", &Greeks::getRhoA, &Greeks::setRhoA); 
}

