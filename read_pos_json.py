# -*- coding: cp936 -*-

import json

pos_json='''
{
    "doc id": 1,
    "doc": {
        "paras": [
            {
                "para id":0
            },
            {
                "para id": 1,
                "sentences": [
                    {
                        "sent id": 0,
                        "cont": "国内专家学者40余人参加研讨会。",
                        "words": [
                            {
                                "word id": 0,
                                "wd": "国内",
                                "pos": "NN",
                                "ne": "O"
                            },
                            {
                                "word id": 1,
                                "wd": "专家",
                                "pos": "NN",
                                "ne": "O"
                            },
                            {
                                "word id": 2,
                                "wd": "学者",
                                "pos": "NN",
                                "ne": "O"
                            },
                            {
                                "word id": 3,
                                "wd": "40余",
                                "pos": "CC",
                                "ne": "Number"
                            },
                            {
                                "word id": 4,
                                "wd": "人",
                                "pos": "NN",
                                "ne": "0"
                            },
                            {
                                "word id": 5,
                                "wd": "研讨会",
                                "pos": "NN",
                                "ne": "O"
                            }
                            ,
                            {
                                "word id": 6,
                                "wd": "。",
                                "pos": "PU",
                                "ne": "O"
                            }
                        ]
                    }
                ]
            }
        ]
    }
}'''
def read_pos_json(pjs):
    try:
        pjs=pjs.decode('utf8')
    except:
        try:
            pjs=pjs.decode('gb18030')
        except:
            pass
    js=json.loads(pjs)
    wll=[]
    try:
        doc=js['doc']
        paras=doc['paras']
        for para in paras:
            sens=para.get('sentences',None)
            if sens!=None:
                for sen in sens:
                    wds=sen.get('words',None)
                    if wds!=None:
                        wl=[(x['wd'],x['pos']) for x in wds]
                        if len(wl)!=0:
                            wll.append(wl)
    except:
        wll=[]
    return wll

if __name__=='__main__':
    wll=read_pos_json(pos_json)
    print wll
    print 'done'