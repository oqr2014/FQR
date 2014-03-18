#include "test_kit.hpp"

namespace QR 
{

TestFunctor::TestFunctor(const std::string& testName_) : 
	_testName(testName_), 
	_inPath("./inputs"), 
	_outPath("./outputs")
{
	_inFile = _inPath + "/" + testName_ + ".txt"; 
	_outFile = _outPath + "/" + testName_ + ".out"; 
} 

TestFunctor::TestFunctor(
	const std::string& testName_,
	const std::string& inPath_, 
	const std::string& inFile_, 
	const std::string& outPath_,  
	const std::string& outFile_) : 
	_testName(testName_), 
	_inPath(inPath_), 
	_inFile(inFile_), 
	_outPath(outPath_), 
	_outFile(outFile_)
{}


void TestFunctor::test() 
{
	_ifs.open(_inFile.c_str()); 
	if (!_ifs.is_open()) {
		std::string errMsg = "Open input file [" + _inFile + "] failed!"; 
		std::cout << errMsg << std::endl; 
		throw QRException(errMsg); 
	}
	_ofs.open(_outFile.c_str()); 
	if (!_ofs.is_open()) {
		std::string errMsg = "Open output file [" + _outFile + "] failed!"; 
		std::cout << errMsg << std::endl; 
		throw QRException(errMsg); 
	}

	writeOutHeader(); 	
//test in a loop 
	while(!_ifs.eof()) {
		try {
			if ( readInput() != 0 ) 
				break; 
			operator()();
 		}
		catch (std::exception &e) {
			std::cout << "std::exception caught: " << e.what() << std::endl; 
		} 
		catch (...) { 
			std::cout << "Unkown exception caught !" << std::endl; 
		} 
	}
	
	_ifs.close(); 
	_ofs.close(); 
}

}

