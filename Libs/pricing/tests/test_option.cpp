#include <iostream>
#include <oqr/pricing/euro_option.hpp> 
#include <oqr/pricing/am_option.hpp> 
#include <oqr/pricing/test_kit.hpp>

namespace QR 
{ 

class TestOption : public TestFunctor {
public: 
	TestOption(const std::string& testName_) : TestFunctor(testName_) {}
	virtual int readInput(); 
	virtual void operator()(void); 
private: 
	EuroOption::Style   _style;
	EuroOption::Type	_type; 
	QuantLib::Date      _valueDate; 
	QuantLib::Date      _maturityDate; 
	double				_S; 
	double				_K; 
	double				_T; 
	double				_sigma; 
	double				_r; 
	double				_q;		
}; 

int TestOption::readInput() 
{
	while ( !_ifs.eof() ) { 
		std::string style; 
		_ifs >> style;  
		if ('#' != style[0]) {
			if ( style == "EUROPEAN" || style == "EURO")
				_style = Option::EUROPEAN; 
			else
				_style = Option::AMERICAN; 
			break; 
		}
		// skip comment line starting with '#'
		_ifs.ignore(1024, '\n');
	}
	if (_ifs.eof()) 
		return -1; 
	std::string type; 
	_ifs >> type; 
	_type = (type == "CALL") ? Option::CALL : Option::PUT;
	_ifs >> _S; 
	_ifs >> _K; 
	_ifs >> _T; 
	_ifs >> _sigma; 
	_ifs >> _r; 
	_ifs >> _q; 
	_ifs.ignore(1024, '\n'); 
	return 0; 
}

void TestOption::operator()(void)
{
	std::cout << "test european option ..." << std::endl;
	OptionPtr optionPtr; 
	if (_style == Option::EUROPEAN) {
		optionPtr = OptionPtr( new EuroOption(
					_type,
					_S,
					_K,
					_T,
					_sigma,
					_r,
					_q) );
	} 
	else {
		optionPtr = OptionPtr( new AmOption( 
					_type,
					_S,
					_K,
					_T,
					_sigma,
					_r,
					_q) );
	}

	optionPtr->calc(); 
	_ofs << "European option: " << *optionPtr << std::endl; 	
	optionPtr->calcDelta(); 
	optionPtr->calcVega(); 
	optionPtr->calcGamma(); 
	optionPtr->calcTheta(); 
	optionPtr->calcRho(); 
	_ofs << "Numerical calculations of the greeks: " << std::endl; 
	_ofs << "delta=" << optionPtr->getGreeks().getDelta() << std::endl; 
	_ofs << "vega="  << optionPtr->getGreeks().getVega()  << std::endl; 
	_ofs << "gamma=" << optionPtr->getGreeks().getGamma() << std::endl; 
	_ofs << "theta=" << optionPtr->getGreeks().getTheta() << std::endl; 
	_ofs << "rho="   << optionPtr->getGreeks().getRho()   << std::endl;
	double price = 5.277;  
	_ofs << "Implied Vol for price(" << price << ")=" << optionPtr->calcImplVol(price) << std::endl; 	
}

} 
int main(int argc, const char* argv[])
{
	QR::TestOption test_option("TestOption");
	test_option.test();  	
	return 0; 
}

 
