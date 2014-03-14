
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
        double  r_);
 
    Option(
        Type    type_, 
        double  S_, 
        double  K_,
	    double  T_, 
        double  sigma_, 
        double  r_);

    virtual ~Option() {} 
    
    virtual void init() {} 
	virtual void calc() {} 

    std::string getTypeName() const; 
    Type getType() const { return _type; }  
    QuantLib::Date getValueDate() const { return _valueDate; }
    QuantLib::Date getMaturityDate() const { return _maturityDate; }
    double getSpot() const { return _S; }
    double getStrike() const { return _K; }
    double getTime2Maturity() const { return _T; }
    double getVol() const { return _sigma; }
    double getRate() const { return _r; }
    QuantLib::DayCounter getDCC() const { return _dayCounter; }
    int getInitFlag() const { return _initFlag; }
	double getPrice() const { return _price; }
	Greeks getGreeks() const { return _greeks; }

    void setType(Type type_) { _type = type_; } 
    void setValueDate(const QuantLib::Date& date_) { _valueDate = date_; }
    void setMaturityDate(const QuantLib::Date& date_) { _maturityDate = date_; }
    void setSpot(double S_) { _S = S_; }
    void setStrike(double K_) { _K = K_; }
    void setTime2Maturity(double T_) { _T = T_; }
    void setVol(double sigma_) { _sigma = sigma_; }
    void setRate(double r_) { _r = r_; }
    void setDCC(const QuantLib::DayCounter& dcc_) { _dayCounter = dcc_; }
    void setInitFlag(int flag_) { _initFlag = flag_; }
	void setPrice(double price_) { _price = price_; }
	void setGreeks(const Greeks& greeks_) { _greeks = greeks_; }

protected: 
    Type  _type; 
    QuantLib::Date  _valueDate; 
    QuantLib::Date  _maturityDate;     
    double  _S;        // Underlying price 
    double  _K;        // Strike 
    double  _T;        // year fraction to maturity 
    double  _sigma;    // Volatility 
    double  _r;        // Risk free rate 
    QuantLib::DayCounter _dayCounter; 
    int     _initFlag;
	double  _price;
    Greeks  _greeks; 
}; 

std::ostream& operator<<(std::ostream& out_, const Option& option_); 


}

#endif 

