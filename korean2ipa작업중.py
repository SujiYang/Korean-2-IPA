"""Created on Wed Nov 28 02:26:56 2018
@file: korean2ipa.py
@author: Suji Yang

"""

"""This

Notes
-----


References
----------


Examples
--------

"""

import re

# Korean consonants and vowels inventory in IPA

inventory = {".":".", " ":" ",
               "ㄱ":"k","ㄲ":"k͈","ㄴ":"n","ㄷ":"t","ㄸ":"t͈","ㄹ":"l","ㅁ":"m","ㅂ":"p","ㅃ":"p͈͈","ㅅ":"s","ㅆ":"s͈","ㅇ":"ŋ","ㅈ":"tɕ","ㅉ":"t͈ɕ","ㅊ":"tɕʰ","ㅋ":"kʰ","ㅌ":"tʰ","ㅍ":"pʰ","ㅎ":"h",
               "ㅏ":"a","ㅐ":"ɛ","ㅓ":"ʌ","ㅔ":"e","ㅗ":"o","ㅜ":"u","ㅡ":"ɯ","ㅣ":"i",
               "ㅑ":"ja","ㅒ":"jɛ","ㅕ":"jʌ","ㅖ":"je","ㅛ":"jo","ㅠ":"ju"}

# some natural classes

consonants = ["m","n","ŋ","l","p","t","k","p͈͈","t͈","k͈","pʰ","tʰ","kʰ","tɕ","t͈ɕ","tɕʰ","s","h","s͈"]

nasals = ["m","n","ŋ"]
liquids = ["l"]

stops = ["p","t","k","p͈͈","t͈","k͈","pʰ","tʰ","kʰ"]
plainStops = ["p","t","k"]
tenseStops = ["p͈͈","t͈","k͈"]
asprStops = ["pʰ","tʰ","kʰ"]

Affrics = ["tɕ","t͈ɕ","tɕʰ"]
plainAffrics = ["tɕ"]
tenseAffics =["t͈ɕ"]
asprAffics = ["tɕʰ"]

frics = ["s","h","s͈"]
plainFricatives = ["s","h"]
tenseFricatives = ["s͈"]


vowels = "(a|ɛ|ʌ|e|o|u|ɯ|i|ja|jɛ|jʌ|je|jo|ju|wø|wi|wa|wɛ|wʌ|we|ɯi)"

monophthong = ["a","ɛ","ʌ","e","o","u","ɯ","i","wø","wi"]
diphthong = ["ja","jɛ","jʌ","je","jo","ju","wa","wɛ","wʌ","we","ɯi"]


# Unicode Korean starts from: 44032, ends with: 55199
baseCode, initial, mid = 44032, 588, 28

# initial characters [00]-[18]
initials = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

# mid characters [00]-[20]
mids = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]

# final characters [00]-[27] (missing 1)
finals = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

def korOrthoSyllParser(Input):
    syll_list = list(Input)
    
    allParsed = []
    for syll in syll_list:
        # first check if the input is Korean
        if re.match(".*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*", syll) is not None:
            
            parsed = []
            
            code = ord(syll) - baseCode
            
            I = int(code / initial)
            parsed.append(initials[I])
            
            M = int((code - (initial * I)) / mid)
            parsed.append(mids[M])
                        
            F = int((code - (initial * I) - (mid * M)))
            if finals[F] == "":
                parsed
            else:
                parsed.append(finals[F])
                
            # save lst(the result of each iteration) into an empty list, allParsed
            allParsed.append(parsed)
            
        # if it's not a Korean just leave it
        else:
            allParsed.extend(syll)
            
            
    return allParsed

def prep(parsedList):
    
    seg_list = []
    for parsed in parsedList:
        if parsed != " " and parsed != ".": 
            seg_list.append(("").join(parsed)+".")
        else:
            seg_list.append(parsed)
     
    return seg_list


def noo_onset(output):
    """Convert the syllable initial ŋ that has no phonetic value into empty string.
    
    Parameters
    ----------
    output : str
        A returned value from the main function: primary.
    
    Returns
    -------
    str
       Phonological processes: no ŋ onset applied to the result of the main function primary.
        
    """

    # find syllable initial ŋ and substitute with empty string.
    
    # Case 1: (regular) sequence of syllable marker and ŋ
    noo_onset = re.sub("\.ŋ",".",output)
    # Case 2: (white space) sequence of white space and ŋ
    noo_onset = re.sub(" ŋ"," ",noo_onset)[1:]
    
    return noo_onset


def vv2diphthong(Noo_onset):
    """Convert the sequence of two vowels into a diphthong.
    
    Parameters
    ----------
    output : str
        A returned value from the previous function: noo_onset
    
    Returns
    -------
    str
       Now diphthongs are represented into the result of the previous function noo_onset.
        
    """

    # find the sequence of VV and substitute with a diphthong 'wV'
    
    vv2diphthong = re.sub("oi","wø",Noo_onset)
    vv2diphthong = re.sub("ui","wi",vv2diphthong)
    vv2diphthong = re.sub("oa","wa",vv2diphthong)
    vv2diphthong = re.sub("oɛ","wɛ",vv2diphthong)
    vv2diphthong = re.sub("uʌ","wʌ",vv2diphthong)
    vv2diphthong = re.sub("ue","we",vv2diphthong)
    
    return vv2diphthong
    
    
#def korCVname(VV2diphthong):
#   
#    korCVname = re.sub("ti\.kɯt\.(i|ɯl|e)","ti.kɯ.s"r"\1",Noo_onset)
#    korCVname = re.sub("tɕi\.ɯtɕ\.(i|ɯl|e)","tɕi.ɯ.s"r"\1",korCVname)
#    korCVname = re.sub("tɕʰi\.ɯtɕʰ\.(i|ɯl|e)","tɕʰi.ɯ.s"r"\1",korCVname)
#    korCVname = re.sub("kʰi\.ɯkʰ\.(i|ɯl|e)","kʰi.ɯ.k"r"\1",korCVname)
#    korCVname = re.sub("tʰi\.ɯtʰ\.(i|ɯl|e)","tʰi.ɯ.s"r"\1",korCVname)
#    korCVname = re.sub("pʰi\.ɯpʰ\.(i|ɯl|e)","pʰi.ɯ.p"r"\1",korCVname)
#    korCVname = re.sub("hi\.ɯh\.(i|ɯl|e)","hi.ɯ.s"r"\1",korCVname)
#    
#    return korCVname


def palatalization(VV2diphthong) :
    """Convert the syllable coda t,tʰ(ltʰ) into the palatalized tɕ,tɕʰ when followed by the nucleus, vowel 'i'.
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: vv2diphthong.
    
    Returns
    -------
    str
       Phonological processes: palatalization applied to the result of the previous function vv2diphthong.
        
    """    
    
    # find the sequence of 't/tʰ/ltʰ.i' and substitute with '.tɕ/tɕʰi' 
    
    # t,tʰ -> tɕ,tɕʰ / ___.i
    # ㄷ,ㅌ(ㄹㅌ) -> ㅈ,ㅊ / ___.ㅣ
    palatalization = re.sub("t\.i",".tɕi",VV2diphthong)
    palatalization = re.sub("tʰ\.i",".tɕʰi",palatalization) # 벼훑이[벼훌치]
    
    ### exception: ㄷ,ㅌ + ㅣ 합성어의 경우 구개음화 일어나지 않음, 밭이랑[반니랑(받니랑)]
    ### !합성어 구분 어떻게 구현
    
    return palatalization

### ㅣ,ㅑ,ㅕ,ㅛ,ㅠ -> 니,냐,녀,뇨,뉴 / (합성어/파생어) C.___
### !합성어,파생어 구분 어떻게 구현


def liaison(Palatalization):
    """Convert the last consonant of the syllable coda followed by a nucleus into the consonant onset followed by the nucleus.
    
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: palatalization.
    
    Returns
    -------
    str
       Phonological processes: liaison applied to the result of the previous function palatalization.
        
    """
     
    ### exception: 모음(ㅏ,ㅓ,ㅗ,ㅜ,ㅟ)으로 시작하는 실질형태소, syllCodaNeut적용후 옮겨발음
    ### !실질형태소 어떻게 구현
    
    # find the sequence of C.V and substitute with the sequence of .CV
    
    # Case 1: single consonant coda 
    
    # (혿,쌍받침)C.V(조사,어미,접미사) -> .CV
    liaison = re.sub("(m|n|l|p|k|p͈͈|t͈|k͈|pʰ|kʰ|tɕ|t͈ɕ|tɕʰ|s|s͈)\."+ vowels,"."r"\1\2",Palatalization)
    liaison = re.sub("(t|tʰ)\.(a|ɛ|ʌ|e|o|u|ɯ|ja|jɛ|jʌ|je|jo|ju|wø|wi|wa|wɛ|wʌ|we|ɯi)","."r"\1\2",liaison) # i --- palatalization
   
    # Case 2: double consonant coda  
    
    # (겹받침)C1C2.V(조사,아미,접미사) -> C1.C2V
    liaison = re.sub("lk\."+ vowels,"l.k"r"\1",liaison)
    liaison = re.sub("lm\."+ vowels,"l.m"r"\1",liaison)
    liaison = re.sub("lpʰ\."+ vowels,"l.pʰ"r"\1",liaison)
    liaison = re.sub("lp\."+ vowels,"l.p"r"\1",liaison)
    liaison = re.sub("ltʰ\."+ vowels,"l.tʰ"r"\1",liaison)
    liaison = re.sub("ls\."+ vowels,"l.s͈"r"\1",liaison)
    liaison = re.sub("ps\."+ vowels,"p.s͈"r"\1",liaison)
    liaison = re.sub("ks\."+ vowels,"k.s͈"r"\1",liaison)
    liaison = re.sub("ntɕ\."+ vowels,"n.tɕ"r"\1",liaison)
        
    return liaison
    

def wi_ify(Liaison):
    """Convert the vowel 'ɯi' into 'i' when preceded by the consonant that has a phonetic value.
    
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: liaison.
    
    Returns
    -------
    str
       Phonological processes: Cɯi to Ci conversion applied to the result of the previous function palatalization.
        
    """ 
    
    # find the sequence of Cɯi and substitute with the sequence of Ci
    
    # ɯi -> i / C___
    # ㅢ -> ㅣ / C___
    wi_ify = re.sub("(m|n|ŋ|l|p|t|k|p͈͈|t͈|k͈|pʰ|tʰ|kʰ|tɕ|t͈ɕ|tɕʰ|s|h|s͈)ɯi",r"\1""i",Liaison)
    
    return wi_ify


def doubleCCoda(Wi_ify):
    """Convert double consonant coda into a single consonant coda.
    
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: wi_ify.
    
    Returns
    -------
    str
       Phonological processes: non-geminate consonant coda applied to the result of the previous function wi_ify.
        
    """ 

    
    ##############################################################################
    # aspiration >> doubleCCoda
    
    # lp.h -> l.pʰ / ntɕ.h -> n.tɕʰ / (verb/adj)lk.h -> l.kʰ
    # ㄹㅂ.ㅎ -> ㄹ.ㅍ / ㄴㅈ.ㅎ -> ㄴ.ㅊ / (용언)ㄹㄱ.ㅎ -> ㄹ.ㅋ  
    
    doubleCCoda = re.sub("lp\.h","l.pʰ",Wi_ify)
    doubleCCoda = re.sub("ntɕ\.h","n.tɕʰ",doubleCCoda)
    ### !용언 doubleCCoda = re.sub("lk\.h","l.kʰ",Wi_ify)
    #############################################################################
    
    
    # exception : 'palp-' [pap]
    # exception: 밟- [밥]
    doubleCCoda = re.sub("palp","pap",doubleCCoda)
    
    ### exception: 'nʌlp-' derivative/compound [nʌp]
    ### exception: 넓- 파생어/합성어 넓적,넓죽,넓둥[넙] <-> 넓다[널따]
    ### !무한한 파생어/합성어 어떻게 구현
    doubleCCoda = re.sub("nʌlp\.(tɕ|t͈ɕ)uk","nʌp.tɕuk",doubleCCoda)
    doubleCCoda = re.sub("nʌlp\.(tɕ|t͈ɕ)ʌk","nʌp.tɕʌk",doubleCCoda)
    doubleCCoda = re.sub("nʌlp\.(t|t͈)uŋ","nʌp.tuŋ",doubleCCoda)

    
    ######################################################################
    ### !용언/체언 구분
    # tensification >> doubleCCoda
    
    # k,t,s,tɕ -> k͈,t͈,s͈,t͈ɕ / verb/adj stem coda ltʰ,lp.___
    # ㄱㄷㅅㅈ -> ㄲㄸㅆㅉ / 어간받침 ㄹㅌ,ㄹㅂ.___
    
    ### presupposition: words that contain doubleC coda 'lt'ʰ and 'lp' fall under the class of verbs/adjectives.
    ### presupposition: the only exception to 'lp': 'jʌ.tʌlp' which is a numeral that contains doubleC coda lp.
    ### !ㄹㅌ받침 용언밖에 없다는 가정(ㄹㅌ받침 체언 없다는 가정) --- 체언 있다면 일일이 넣어야
    ### !ㄹㅂ받침 체언 '여덟' 밖에 없다는 가정 --- 더 있다면 일일이 넣어야
    doubleCCoda = re.sub("jʌ.tʌlp\.(k|t|s|tɕ)","jʌ.tʌlp."r"\1",doubleCCoda)
    
    doubleCCoda = re.sub("(ltʰ|lp)\.k",r"\1"".k͈",doubleCCoda)
    doubleCCoda = re.sub("(ltʰ|lp)\.t",r"\1"".t͈",doubleCCoda)
    doubleCCoda = re.sub("(ltʰ|lp)\.s",r"\1"".s͈",doubleCCoda)
    doubleCCoda = re.sub("(ltʰ|lp)\.tɕ",r"\1"".t͈ɕ",doubleCCoda)
    ######################################################################
    
    # find doubleC coda and substitute with a single consonant coda
    
    # lp,ls,ltʰ -> l / ntɕ -> n / lm -> m / lpʰ,ps -> p / ks,lk -> k
    # ㄹㅂ,ㄹㅅ,ㄹㅌ -> ㄹ / ㄴㅈ -> ㄴ / ㄹㅁ -> ㅁ / ㄹㅍ,ㅂㅅ -> ㅂ / ㄱㅅ,ㄹㄱ -> ㄱ
    doubleCCoda = re.sub("(lp|ls|ltʰ)","l",doubleCCoda)
    doubleCCoda = re.sub("ntɕ","n",doubleCCoda)
    doubleCCoda = re.sub("lm","m",doubleCCoda)
    doubleCCoda = re.sub("(lpʰ|ps)","p",doubleCCoda)
    doubleCCoda = re.sub("(ks|lk)","k",doubleCCoda)
    
    ### exception: 용언 ㄹㄱ(ㄷ,ㅈ,ㅅ) -> ㄱ, ㄹㄱ(ㄱ) -> ㄹ
    ### !용언(체언) 구분 어떻게 구현
    
    return doubleCCoda   
    

def syllCodaNeut(doubleCCoda):
    """Convert the syllable coda affricates and fricatives into stop 't' and tensed/aspirated stops into plain stops.
    
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: doubleCCoda.
    
    Returns
    -------
    str
       Phonological processes: syllable coda neutralization applied to the result of the previous function doubleCCoda.
        
    """     
    
    # Case 1: affricates into t
    syllCodaNeut = re.sub("(tɕ|t͈ɕ|tɕʰ)\.","t.",doubleCCoda)
    
    # Case 2: fricatives into t
    syllCodaNeut = re.sub("(s|s͈)\.","t.",syllCodaNeut)
    
    # Case 3: tensed/aspirated stops into plain stops
    syllCodaNeut = re.sub("(p͈͈|pʰ)\.","p.",syllCodaNeut)
    syllCodaNeut = re.sub("(t͈|tʰ)\.","t.",syllCodaNeut)
    syllCodaNeut = re.sub("(k͈|kʰ)\.","k.",syllCodaNeut)
    
    return syllCodaNeut  


def aspiration(SyllCodaNeut):
    """Convert the syllable onset k,t,p,tɕ into aspirated kʰ,tʰ,pʰ,tɕʰ when preceded by consonant 'h'/'nh'/'lh' syllable coda and
    convert syllable coda k,t,p,tɕ into aspirated kʰ,tʰ,pʰ,tɕʰ when followed by consonant 'h' syllable onset.

    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: syllCodaNeut.
    
    Returns
    -------
    str
       Phonological processes: aspiration applied to the result of the previous function syllCodaNeut.
        
    """     
        
    # Case 1: find the sequence of 'h.k/t/p/tɕ' and substitute with '.kʰ','.tʰ','.pʰ','.tɕʰ'
   
    # k,t,p,tɕ -> kʰ,tʰ,pʰ,tɕʰ / h.___
    # ㄱ,ㄷ,ㅂ,ㅈ -> ㅋ,ㅌ,ㅍ,ㅊ / ㅎ,ㄴㅎ,ㄹㅎ.___
    aspiration = re.sub("h\.k",".kʰ",SyllCodaNeut)
    aspiration = re.sub("h\.t",".tʰ",aspiration)
    aspiration = re.sub("h\.p",".pʰ",aspiration)
    aspiration = re.sub("h\.tɕ",".tɕʰ",aspiration)
   
    # find the sequence of 'h.s' and substitute with '.s͈'
    
    # s -> s͈ / h.___
    # ㅅ -> ㅆ / ㅎ/ㄴㅎ/ㄹㅎ.___ 
    aspiration = re.sub("h\.s",".s͈",aspiration)
        
    #################################################
    # palatalization  >> aspiration
    
    # h -> tɕʰ / t.___i
    # ㅎ -> ㅊ / ㄷ.___/
    
    aspiration = re.sub("t\.hi",".tɕʰi",aspiration)
    #################################################
    
    # Case 2: find the sequence of 'k.h','t.h','p.h','tɕ.h' and substitute with '.kʰ','.tʰ','.pʰ','.tɕʰ'
    
    # k,t,p,tɕ -> kʰ,tʰ,pʰ,tɕʰ / ___.h
    # ㄱ,ㄷ,ㅂ,ㅈ -> ㅋ,ㅌ,ㅍ,ㅊ / ___.ㅎ
    aspiration = re.sub("k\.h",".kʰ",aspiration)
    aspiration = re.sub("t\.h",".tʰ",aspiration)
    aspiration = re.sub("p\.h",".pʰ",aspiration)
    aspiration = re.sub("tɕ\.h",".tɕʰ",aspiration)
    
    return aspiration
 
    
def h(Aspiration):
    """Convert the sequence of 'h.n' into 'n.n', the sequence of h.V into .V and the sequence of 'nh','nl' into 'n','l'.

    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: aspiration.
    
    Returns
    -------
    str
       Phonological processes regarding the segment 'h' applied to the result of the previous function aspiration.
        
    """      
    
    # Case 1: find the sequence of 'h.n' and substitute with 'n.n'
    
    # h -> n / ___.n
    # ㅎ -> ㄴ / ___.ㄴ
    h = re.sub("h\.n","n.n",Aspiration)
    
    # Case 2: find the sequence of h.V and substitue with the sequence of .V
    
    # h -> "" / ___.V
    # ㅎ -> "" / ___. V
    h = re.sub("h\."+ vowels,"."r"\1",h)
    
    # Case 3: find the sequence of 'nh','nl' and substitute with 'n','l'
    
    # nh -> n, lh -> l
    # ㄴㅎ -> ㄴ, ㄹㅎ -> ㄹ
    h = re.sub("nh","n",h)
    h = re.sub("lh","l",h)
    
    return h


def nasalization(H):
    """Convert the syllable coda 'l' into the homorganic nasal 'n' when preceded by the nasalC 'm','ŋ' or the non-nasalC 'k','p' and
    convert the syllable coda 'k','t','p' into the homorganic nasal when followed by the nasal 'n','m'.
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: h.
    
    Returns
    -------
    str
       Phonological processes: nasalization applied to the result of the previous function h.
        
    """           
    
    # Case 1: find the sequence of ''m/ŋ.l' and substitute with 'm/ŋ.n'
    
    # ㄹ -> ㄴ / ㅁ,ㅇ.___
    nasalization = re.sub("(m|ŋ)\.l",r"\1"".n",H)
    
    # Case 2: find the sequence of ''k/p/.l' and substitute with 'k/p.n'
    
    # ㄹ -> ㄴ / ㄱ,ㅂ.___
    nasalization = re.sub("(k|p)\.l",r"\1"".n",nasalization)
    
    # Case 3: find the sequence of 'k/t/p.n/m' and substitute with 'ŋ/n/m.n/m'
    
    # ㄱ,ㄷ,ㅂ -> ㅇ,ㄴ,ㅁ / ___.ㄴ,ㅁ
    nasalization = re.sub("k\.(n|m)","ŋ."r"\1",nasalization)
    nasalization = re.sub("t\.(n|m)","n."r"\1",nasalization)
    nasalization = re.sub("p\.(n|m)","m."r"\1",nasalization)
    
    return nasalization        
 
    
def lateralization(Nasalization):
    """Convert the syllable coda 'n' into the lateral 'l' when followed  by the syllable onset 'l' and 
    convert the syllavle onset 'n' into the lateral 'l' when preceded by the syllable coda 'l'.
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: nasalization.
    
    Returns
    -------
    str
       Phonological processes: lateralization applied to the result of the previous function nasalization.
        
    """ 
    
    # find the sequence of 'n.l' and substitute with 'l.l'
    
    # ㄴ -> ㄹ / ___.ㄹ
    lateralization = re.sub("n\.l","l.l",Nasalization)
    
    # find the sequence of 'l.n' and substitute with 'l.l'
    
    # ㄴ -> ㄹ / ㄹ.___
    lateralization = re.sub("l\.n","l.l",lateralization)
    
    ### 한자어 중 ㄴ+ㄹ이지만 [ㄹㄹ] 아닌[ㄴㄴ]으로 발음되는 경우 있음, 공권력[공꿘녁]
    ### (실제발음고려한것, 사전에 [ㄴㄴ]로 발음 단어 개별 표기)
    ### !무한한 ㄴ+ㄹ[ㄴㄴ] 한자어 어떻게 구현
    
    return lateralization


def tensification(Lateralization):
    """Convert the syllable coda k,t,p,s,tɕ into the tensed k͈,t͈,p͈͈,s͈t͈ɕ when preceded by the syllable coda k,t,p and
    convert the syllavle onset t,s,tɕ into the tensed t͈,s͈,t͈ɕ when preceded by the syllable coda 'l'.
    
    Parameters
    ----------
    Noo_onset : str
        A returned value from the previous function: lateralization.
    
    Returns
    -------
    str
       Phonological processes: lateralization applied to the result of the previous function lateralization.
        
    """ 
    
    # Case 1: find the sequence of 'k/t/p.k/t/p/s/tɕ' and substitute into 'k/t/p/.k͈/t͈/p͈͈/s͈/t͈ɕ'
    
    # k,t,p,s,tɕ -> k͈,t͈,p͈͈,s͈t͈ɕ / k,t,p.___
    # ㄱ,ㄷ,ㅂ,ㅅ,ㅈ -> ㄲ,ㄸ,ㅃ,ㅆ,ㅉ / ㄱ,ㄷ,ㅂ.___
    tensification = re.sub("(k|t|p)\.k",r"\1"".k͈",Lateralization)
    tensification = re.sub("(k|t|p)\.t",r"\1"".t͈",tensification)
    tensification = re.sub("(k|t|p)\.p",r"\1"".p͈͈",tensification)
    tensification = re.sub("(k|t|p)\.s",r"\1"".s͈",tensification)
    tensification = re.sub("(k|t|p)\.tɕ",r"\1"".t͈ɕ",tensification)

    ### (용언)어간받침 ㄱㄷㅅㅈ -> ㄲㄸㅆㅉ / ㄴ,ㅁ.___ (피동,사동 접미사 -기 제외)
    ### 용언: 신고[신꼬] 껴안다[껴안따] 체언: 신도[신도] 신과[신과] 바람도[바람도]
    ### !용언/체언 구분 어떻게 구현
    
    # Case 2: find the sequence of 'l.t/s/tɕ' and substitute into 'l.t͈/s͈/t͈ɕ'
    
    ### (Hanja)  t,s,tɕ -> t͈,s͈,t͈ɕ / l.___
    ### (!한자어) ㄷ,ㅅ,ㅈ -> ㄸ,ㅆ,ㅉ / ㄹ.___
    tensification = re.sub("l\.t","l.t͈",tensification)
    tensification = re.sub("l\.s","l.s͈",tensification)
    tensification = re.sub("l\.tɕ","l.t͈ɕ",tensification)
    
    ### -(으)ㄹ 관형사형, 어미 + 관형격 기능 지닌 사이시옷이 있어야할(휴지가 성립되는) 합성어 VS. 된소리 적용X 한자어 
    ### ㄱ,ㅂ,(ㄷ,ㅅ,ㅈ) -> ㄲ,ㅃ,(ㄸ,ㅆ,ㅉ) / 관형사형 -(으)ㄹ, ___로 시작되는 어미.___ --- 갈곳[갈꼳],만날사람[만날싸람]/할밖에[할빠께]
    ### 문-고리[문꼬리],아침-밥[아침빱],눈-동자[눈똥자],산-새[산쌔],잠-자리[잠짜리]
    ### 된소리 적용X 한자어: 결과,물건...불복,활보...
    ### ! -(으)ㄹ이 관형사형/___시작 어미임을 어떻게 구현
    ### ! 관형격기능지니는 휴지가 성립되는 합성어, 된소리적용X 한자어 구분 어떻게 구현
    
    return tensification


### ! 사이시옷 붙은 단어 구분 어떻게 구현


def primary():
    """Main function, Korean to IPA converter that applies all phonological processes over a given Korean.
    
    1) convert Korean into IPA
    2) apply phonological processes (go through all subfunctions in sequence)
    3) return a modified string
    
    Parameters
    ----------
    Input from user
    
    Returns
    -------
    str
        IPA transcription of a given Korean.
        
    """
    
    # take str input from user
    Input = input("Enter Korean: ") 
    
    parsedList = korOrthoSyllParser(Input)
    print(parsedList)
    Prep = prep(parsedList)
    lPrep = list(Prep)
    print(lPrep)
    
    Prep = ().join(lPrep)
    output = list(Prep)
    
    
    # match each characters(key) with IPA(value) from the dictionary 'inventory.'
    for seg in output:
        output.append(inventory[seg])
    # convert list of IPA characters into a single string, add syllable marker to the BOS and EOS.
    output = "."+("").join(output)
    print(output)
    
    
    # assign variable name for the function call of all the defined functions above.
        # assigned variable name becomes a parameter of the following function
    Noo_onset = noo_onset(output)
    VV2diphthong = vv2diphthong(Noo_onset)
#   KorCVname = korCVname(VV2diphthong)
    Palatalization = palatalization(VV2diphthong)
    Liaison = liaison(Palatalization)
    Wi_ify = wi_ify(Liaison) 
    DoubleCCoda = doubleCCoda(Wi_ify)
    SyllCodaNeut = syllCodaNeut(DoubleCCoda)
    Aspiration = aspiration(SyllCodaNeut)
    H = h(Aspiration)
    Nasalization = nasalization(H)
    Lateralization = lateralization(Nasalization)
    Tensification = tensification(Lateralization)
    
    # remove the syllable marker of the EOS
    output = Tensification[:len(Tensification)-1]
    
    
    # print the result: IPA, Korean transcription
    print(output)

primary()
