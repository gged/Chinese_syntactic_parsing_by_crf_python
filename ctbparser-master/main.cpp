#include <fstream>
#include <iostream>
#include <ctime>
#include "ctbparser.h"
using namespace std;
int main(int args, char *argv[])
{
	ctbparser *c=new ctbparser();
	if(!c->load_config("/home/hdz/Desktop/QA/ctbparser-master/config.txt")){//full path
		delete c;
		c=0;
		return 1;
	}
	char src[100];
	char res[100];
	/*
	cout<<"请输入一句话：(输入'Q'退出)"<<endl;
	do{
		cin>>s;
		if(!strcmp(s,"Q"))
			break;
		c->decode_string(s,t);
		cout<<t<<endl;
	}while(1);
	c->decode_file("in.txt","out.txt");
	cout<<"ctbparser test success!"<<endl;
	if (args>=2){
		//cout<<argv[1]<<endl;
		sscanf(argv[1],"%s",&s);
		c->decode_string(s,t);
		cout<<t<<endl;
	}
	*/
	sscanf(argv[1],"%s",&src);
	sscanf(argv[2],"%s",&res);
	c->decode_file(src,res);
	delete c;
	c=0;
	return 0;
}
