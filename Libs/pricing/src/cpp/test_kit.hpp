
#ifndef _QR_TEST_KIT_HPP_
#define _QR_TEST_KIT_HPP_

#include <iostream>
#include <fstream>
#include <string>
#include <boost/shared_ptr.hpp>
#include "utility.hpp"

namespace QR 
{
class TestFunctor {
public: 
	TestFunctor(const std::string& testName_); 
	TestFunctor(const std::string& testName_, 
				const std::string& inPath_, 
				const std::string& inFile_, 
				const std::string& outPath_, 
				const std::string& outFile_);  
	virtual ~TestFunctor() {}
	virtual int readInput() = 0; 
	virtual void operator() (void) = 0; 
	virtual void test();  
		
	const std::string& getTestName() const { return _testName; }  
	const std::string & getInPath() const {return _inPath; }  
	const std::string & getInFile() const {return _inFile; }  
	const std::string & getOutPath() const {return _outPath; }  
	const std::string & getOutFile() const {return _outFile; }  

	void setInPath(const std::string& str_) { _inPath = str_; }
	void setInFile(const std::string& str_) { _inFile = str_; }
	void setOutPath(const std::string& str_) { _outPath = str_; }
	void setOutFile(const std::string& str_) { _outFile = str_; }

protected:
	TestFunctor();  
	std::string		_testName; 
	std::string		_inPath; 
	std::string		_inFile; 
	std::string		_outPath;
	std::string		_outFile;   
	std::ifstream   _ifs; 
	std::ofstream   _ofs; 

};  

}

#endif

