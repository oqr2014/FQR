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
	virtual void writeOutHeader(); 
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
	double				_price_implVol; 
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
	_ifs >> _price_implVol; 
	_ifs.ignore(1024, '\n'); 
	return 0; 
}

void TestOption::writeOutHeader() 
{
	_ofs << "#Style\tType\tPrice\tDelta\tVega\tGamma\tTheta\tRho\tImplVol(price)" << std::endl; 
}

void TestOption::operator()(void)
{
	std::cout << "test option ..." << std::endl;
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

	optionPtr->calcPrice(); 
	optionPtr->calcDelta(); 
	optionPtr->calcVega(); 
	optionPtr->calcGamma(); 
	optionPtr->calcTheta(); 
	optionPtr->calcRho(); 
	double implVol = optionPtr->calcImplVol(_price_implVol); 
	_ofs << optionPtr->getStyleName() 
		<< "\t" << optionPtr->getTypeName()  
		<< "\t" << optionPtr->getPrice()  
		<< "\t" << optionPtr->getGreeks().getDelta() 
		<< "\t" << optionPtr->getGreeks().getVega() 
		<< "\t" << optionPtr->getGreeks().getGamma()
		<< "\t" << optionPtr->getGreeks().getTheta()
		<< "\t" << optionPtr->getGreeks().getRho() 
		<< "\t" << implVol << std::endl; 	
}

} 


int main(int argc, const char* argv[])
{
	QR::TestOption test_option("TestOption");
	test_option.test();  	
	return 0; 
}

 
