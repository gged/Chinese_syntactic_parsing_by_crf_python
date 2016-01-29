//���һ��dict.txt�Ƿ�ȫ�ǣ�pos�Ƿ�ϸ�
#ifndef CTBPARSER_H
#define CTBPARSER_H
#include "crf.h"
#include "normalstr.h"
#include "trie.h"
#include "crfparser.h"
typedef struct word{
	int left;
	int right;
	int parent;
	double weight;
	string pos;
	string dep;
}word;



class ctbparser{
public:
	ctbparser();
	~ctbparser();
	
	//APIs
	bool load_config(char *fn);//ѵ�������ԵĲ����ļ�
	void decode_string(char *in, char *out);
	void decode_file(char *fn_in, char *fn_out);
	//void decode_file2(char *fn_in, char *fn_out);
private:
	bool check_dict();
	normalstr *_ns;
	bool _full;//���ȫ�ǣ�
	bool _segsen;//��Ҫ�־䣿
	int _task;//seg,pos,parse
	int _nbest;
	CRF *_ner;
	char _ner_model_file[100];
	CRF *_seg;
	char _seg_model_file[100];
	CRF *_pos;
	char _pos_model_file[100];
	crfparser *_par;
	char _parser_model_file[100];
	Trie *_dict;
	char _dict_file[100];
	vector<vector<word> > _words;//�м�����
	vector<double> _probs;
	vector<string> _fulls;
	vector<string> _halfs;
	void process_sub();
	//void process_sub2();
	void output(char *out);
	void output(FILE *&fout);
	bool get_char(char *&p, char *c);
	bool get_char(FILE *&fp, char *c);
	void get_constraint(vector<word> &cw);
	int _version;
};
#endif
