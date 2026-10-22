"""Map bounded definite-length BER tag/length/value boundaries without interpreting values."""
import argparse,json,sys

def analyze(data):
    if not isinstance(data,bytes) or len(data)>131072:raise ValueError('bytes input must be <=128KiB')
    nodes=[]
    def error(p,s):raise ValueError('offset '+str(p)+': '+s)
    def walk(at,end,parent,depth):
        if depth>32:error(at,'depth exceeds32')
        while at<end:
            start=at
            if len(nodes)>=5000:error(at,'more than5000 nodes')
            first=data[at];at+=1;number=first&31
            if number==31:
                number=0;count=0
                while True:
                    if at>=end:error(at,'truncated high tag')
                    b=data[at];at+=1;count+=1
                    if count>4:error(at-1,'high tag longer than4 octets')
                    if count==1 and b&127==0:error(at-1,'nonminimal high tag')
                    number=number*128+(b&127)
                    if not b&128:break
                if number<31:error(start,'high tag number below31 (EMV deviations unsupported)')
            tag_end=at
            if first>>6==0 and number==0:error(start,'end-of-contents tag unsupported in definite data')
            if at>=end:error(at,'missing length')
            b=data[at];at+=1;minimal=True
            if b==128:error(at-1,'indefinite length unsupported')
            if b<128:length=b
            else:
                n=b&127
                if n>4:error(at-1,'length uses more than4 octets')
                if at+n>end:error(at,'truncated length')
                length=int.from_bytes(data[at:at+n],'big');minimal=length>=128 and data[at]!=0;at+=n
            stop=at+length
            if stop>end:error(start,'value crosses parent boundary')
            index=len(nodes);constructed=bool(first&32)
            nodes.append({'index':index,'parent':parent,'depth':depth,'offset':start,'tag_hex':data[start:tag_end].hex(),
                          'class':['universal','application','context','private'][first>>6],'tag_number':number,
                          'constructed':constructed,'header_length':at-start,'value_offset':at,'length':length,'end':stop,
                          'minimal_length':minimal,'preview_hex':None if constructed else data[at:min(stop,at+32)].hex()})
            if constructed:walk(at,stop,index,depth+1)
            at=stop
    walk(0,len(data),None,0)
    return {'bytes':len(data),'nodes':nodes,'all_lengths_minimal':all(n['minimal_length']for n in nodes),
            'limitation':'Structural definite BER only; no schema, ASN.1 value semantics, DER validation, EMV tag deviations, decryption or certificate verification.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('hex_file');a=p.parse_args()
    try:
        with open(a.hex_file,'rb')as f:s=f.read(1048577)
        if len(s)>1048576:raise ValueError('hex file exceeds1MiB')
        data=bytes.fromhex(s.decode('ascii'));print(json.dumps(analyze(data),indent=2));return 0
    except (ValueError,OSError,UnicodeError)as e:print(json.dumps({'error':str(e)}),file=sys.stderr);return 2

if __name__=="__main__": raise SystemExit(main())
