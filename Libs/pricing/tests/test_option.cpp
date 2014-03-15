#include <iostream>
#include <oqr/pricing/euro_option.hpp> 


static void read_euro_option_data( )
{
	
}


int main(int argc, const char* argv[])
{
	std::cout << "test european option ..." << std::endl;
	QR::EuroOption option(
		QR::Option::PUT,
		36,
		40,
		1., 
		.2, 
		.06); 
	option.calc(); 
	std::cout << "option: " << option << std::endl; 	
	option.calcDelta(); 
	option.calcVega(); 
	option.calcGamma(); 
	option.calcTheta(); 
	option.calcRho(); 
	std::cout << "Numerical calculations of the greeks: " << std::endl; 
	std::cout << "delta=" << option.getGreeks().getDelta() << std::endl; 
	std::cout << "vega=" << option.getGreeks().getVega() << std::endl; 
	std::cout << "gamma=" << option.getGreeks().getGamma() << std::endl; 
	std::cout << "theta=" << option.getGreeks().getTheta() << std::endl; 
	std::cout << "rho=" << option.getGreeks().getRho() << std::endl; 

	return 0; 
}
