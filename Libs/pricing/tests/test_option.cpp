#include <iostream>
#include <oqr/pricing/euro_option.hpp> 
#include <oqr/pricing/am_option.hpp> 


static void read_euro_option_data( )
{
	
}


int main(int argc, const char* argv[])
{
	std::cout << "test european option ..." << std::endl;
	QR::EuroOption euro_option(
		QR::Option::PUT,
		36,  //spot
		40,  //strike 
		1.,  //T2M
		.2,  //vol
		.06, //r 
		.06); //q 
	euro_option.calc(); 
	std::cout << "option: " << euro_option << std::endl; 	
	euro_option.calcDelta(); 
	euro_option.calcVega(); 
	euro_option.calcGamma(); 
	euro_option.calcTheta(); 
	euro_option.calcRho(); 
	std::cout << "Numerical calculations of the greeks: " << std::endl; 
	std::cout << "delta=" << euro_option.getGreeks().getDelta() << std::endl; 
	std::cout << "vega=" << euro_option.getGreeks().getVega() << std::endl; 
	std::cout << "gamma=" << euro_option.getGreeks().getGamma() << std::endl; 
	std::cout << "theta=" << euro_option.getGreeks().getTheta() << std::endl; 
	std::cout << "rho=" << euro_option.getGreeks().getRho() << std::endl;
	double price = 5.277;  
	std::cout << "Implied Vol for price(" << price << ")=" << euro_option.calcImplVol(price) << std::endl; 

	QR::AmOption am_option(
		QR::Option::PUT,
		36,  //spot
		40,  //strike 
		1.,  //T2M
		.2,  //vol
		.06, //r 
		.06); //q 
	am_option.calcPrice(); 
	std::cout << "American option price="<< am_option.getPrice() << std::endl; 
	return 0; 
}
