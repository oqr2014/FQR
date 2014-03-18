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
	bool				_bT2M; 
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
		char c = _ifs.peek(); 
		if ('#' == c) {
			// skip comment line starting with '#'
			_ifs.ignore(1024, '\n');
		}
		else
			break; 
	}
	if (_ifs.eof()) 
		return -1; 
// peek a line 
	std::streampos sp = _ifs.tellg(); 
	std::string line; 
	std::getline(_ifs, line); 
	_ifs.seekg(sp); 
	std::size_t found = line.find("/");
	_bT2M = true; 
	if (found != std::string::npos)
		_bT2M = false; 

	std::string style; 
	_ifs >> style; 
	_style = ( style=="EUROPEAN" || style=="EURO") ? Option::EUROPEAN : Option::AMERICAN; 
	std::string type; 
	_ifs >> type; 
	_type = (type == "CALL") ? Option::CALL : Option::PUT;
	if( !_bT2M ) {
		_ifs >> _valueDate; 
		_ifs >> _maturityDate; 
	}
	_ifs >> _S; 
	_ifs >> _K; 
	if ( _bT2M ) 
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
		if ( _bT2M )
			optionPtr = OptionPtr( new EuroOption( _type, _S, _K, _T, _sigma, _r, _q) );
		else
			optionPtr = OptionPtr( new EuroOption( _type, _valueDate, _maturityDate, _S, _K, _sigma, _r, _q) );
	} 
	else {
		if ( _bT2M )
			optionPtr = OptionPtr( new AmOption( _type, _S, _K, _T, _sigma, _r, _q) );
		else
			optionPtr = OptionPtr( new AmOption( _type, _valueDate, _maturityDate, _S, _K, _sigma, _r, _q) );
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

