
#ifndef _QR_OPTION_HPP_
#define _QR_OPTION_HPP_

#include <iostream>
#include <string>
#include <vector>
#include <boost/shared_ptr.hpp>
#include <ql/quantlib.hpp>
#include "greeks.hpp"

namespace QR 
{

const double PCT_CHANGE_GREEKS = 0.001; 
class Option; 
typedef boost::shared_ptr<Option> OptionPtr; 

class Option { 
public: 
    enum Type {
        PUT = -1, 
        CALL = 1 
    }; 

    Option(); 
    Option(const Option& option_); 
    Option& operator=(const Option& option_); 

    Option(
        Type    type_, 
        const QuantLib::Date&  valueDate_,               
        const QuantLib::Date&  maturityDate_,               
        double  S_, 
        double  K_,
        double  sigma_, 
        double  r_, 
		double  q_);
 
    Option(
        Type    type_, 
        double  S_, 
        double  K_,
	    double  T_, 
        double  sigma_, 
        double  r_,
		double  q_);

    virtual ~Option() {} 
    virtual Option* clone() const { return new Option(*this); } 

    virtual void init() {} 
	virtual void calcPrice() {} 
	virtual void calcDelta(double pct_ = PCT_CHANGE_GREEKS);  
	virtual void calcVega(double pct_ = PCT_CHANGE_GREEKS);   
	virtual void calcGamma(double pct_ = PCT_CHANGE_GREEKS); 
	virtual void calcTheta(double pct_ = PCT_CHANGE_GREEKS);  
	virtual void calcRho(double pct_ = PCT_CHANGE_GREEKS); 
	virtual void calcGreeksAnalytic() {}  
	virtual void calc() {} 
	virtual double calcImplVol(double price_); 

    std::string getTypeName() const; 
    Type getType() const { return _type; }  
    QuantLib::Date getValueDate() const { return _valueDate; }
    QuantLib::Date getMaturityDate() const { return _maturityDate; }
    double getSpot() const { return _S; }
    double getStrike() const { return _K; }
    double getT2M() const { return _T; }
    double getVol() const { return _sigma; }
    double getRate() const { return _r; }
    double getDivYield() const { return _q; }
    QuantLib::DayCounter getDCC() const { return _dayCounter; }
    int getInitFlag() const { return _initFlag; }
	double getPrice() const { return _price; }
	Greeks getGreeks() const { return _greeks; }

    void setType(Type type_) { _type = type_; _initFlag = 0; } 
    void setValueDate(const QuantLib::Date& date_) { _valueDate = date_; _initFlag = 0; }
    void setMaturityDate(const QuantLib::Date& date_) { _maturityDate = date_; _initFlag = 0; }
    void setSpot(double S_) { _S = S_; _initFlag = 0; }
    void setStrike(double K_) { _K = K_; _initFlag = 0; }
    void setT2M(double T_) { _T = T_; _initFlag = 0; }
    void setVol(double sigma_) { _sigma = sigma_; _initFlag = 0; }
    void setRate(double r_) { _r = r_; _initFlag = 0; }
    void setDivYield(double q_) { _q = q_; _initFlag = 0; }
    void setDCC(const QuantLib::DayCounter& dcc_) { _dayCounter = dcc_; _initFlag = 0; }
    void setInitFlag(int flag_) { _initFlag = flag_; _initFlag = 0; }
	void setPrice(double price_) { _price = price_; _initFlag = 0; }
	void setGreeks(const Greeks& greeks_) { _greeks = greeks_; _initFlag = 0; }

protected: 
    Type  _type; 
    QuantLib::Date  _valueDate; 
    QuantLib::Date  _maturityDate;     
    double  _S;        // Underlying price 
    double  _K;        // Strike 
    double  _T;        // year fraction of time to maturity 
    double  _sigma;    // Volatility 
    double  _r;        // Risk free rate 
    double  _q;        // Dividend yield, not used so far 
    QuantLib::DayCounter _dayCounter; 
    int     _initFlag;
	double  _price;
    Greeks  _greeks; 
}; 

std::ostream& operator<<(std::ostream& out_, const Option& option_); 

class FunctorImplVol {
public:
	explicit FunctorImplVol(const Option* optionPtr_, double price_) :
	_optionPtr(optionPtr_), _price(price_)
	{}

	double operator() (double vol_) const; 

private:
	const Option*	_optionPtr;
	double			_price;
};


}

#endif 

