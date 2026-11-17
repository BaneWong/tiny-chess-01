import json,os,sys,urllib.request,urllib.error
E=os.environ["MAKEFUN_ENV_URL"]
V={"p":100,"n":320,"b":330,"r":500,"q":900}
def post(p,b={}):
 r=urllib.request.Request(E+p,json.dumps(b).encode(),{"content-type":"application/json"})
 try:
  with urllib.request.urlopen(r) as s:return json.load(s)
 except urllib.error.HTTPError:sys.exit()
def bd(f):
 b=[None]*64
 for i,rt in enumerate(f.split()[0].split("/")):
  c=0
  for ch in rt:
   if ch.isdigit():c+=int(ch)
   else:b[i*8+c]=ch;c+=1
 return b
def s2i(s):return(8-int(s[1]))*8+"abcdefgh".index(s[0])
def gm(b,co):
 ms=[];ow="w"==co
 for sq in range(64):
  x=b[sq]
  if x is None:continue
  if ow==x.islower():continue
  pt=x.lower()
  if pt=="p":
   d=-8 if ow else 8;pr=0 if ow else 7;sr=6 if ow else 1
   fw=sq+d
   if 0<=fw<64 and b[fw] is None:
    if fw//8==pr:
     for p in"qnrb":ms.append((sq,fw,p))
    else:ms.append((sq,fw,None))
    if sq//8==sr:
     f2=sq+d*2
     if 0<=f2<64 and b[f2] is None:ms.append((sq,f2,None))
   for o in(-1,1):
    cp=sq+d+o
    if 0<=cp<64 and abs(cp%8-sq%8)==1:
     t=b[cp]
     if t and ow!=t.islower():
      if cp//8==pr:
       for p in"qnrb":ms.append((sq,cp,p))
      else:ms.append((sq,cp,None))
  elif pt=="n":
   for dd in(-17,-15,-10,-6,6,10,15,17):
    nb=sq+dd
    if 0<=nb<64 and abs(nb%8-sq%8)<=2 and abs(nb//8-sq//8)<=2:
     t=b[nb]
     if t is None or ow!=t.islower():ms.append((sq,nb,None))
  elif pt=="b":
   for dd in(-9,-7,7,9):
    nb=sq+dd
    while 0<=nb<64 and abs(nb%8-(nb-dd)%8)<=1:
     t=b[nb]
     if t:
      if ow!=t.islower():ms.append((sq,nb,None))
      break
     ms.append((sq,nb,None));nb+=dd
  if pt=="r":
   for dd in(-8,-1,1,8):
    nb=sq+dd
    while 0<=nb<64 and(dd in(-8,8) or nb%8==sq%8):
     t=b[nb]
     if t:
      if ow!=t.islower():ms.append((sq,nb,None))
      break
     ms.append((sq,nb,None));nb+=dd
  if pt=="q":
   for dd in(-9,-8,-7,-1,1,7,8,9):
    nb=sq+dd
    while 0<=nb<64 and(abs(dd) in(1,8) or abs(nb%8-(nb-dd)%8)<=1):
     t=b[nb]
     if t:
      if ow!=t.islower():ms.append((sq,nb,None))
      break
     ms.append((sq,nb,None));nb+=dd
  if pt=="k":
   for dd in(-9,-8,-7,-1,1,7,8,9):
    nb=sq+dd
    if 0<=nb<64 and abs(nb%8-sq%8)<=2 and abs(nb//8-sq//8)<=2:
     t=b[nb]
     if t is None or ow!=t.islower():ms.append((sq,nb,None))
 return ms
def ap(b,m):
 b=list(b);b[m[1]]=m[2] or b[m[0]];b[m[0]]=None;return b
def pst(pt,sq,w):
 dc=min(sq%8,7-sq%8);dr=min(sq//8,7-sq//8)
 if pt=="p":return(7-(sq//8 if w else 7-sq//8))*5
 if pt=="n":return max(0,3-max(dc,dr))*10
 if pt=="b":return max(0,2-max(dc,dr))*8
 if pt=="r":return max(0,2-max(dc,dr))*6
 if pt=="q":return max(0,3-max(dc,dr))*8
 if pt=="k":return max(0,3-max(dc,dr))*15+max(0,2-dr)*10
 return 0
def ev(bd):
 s=0
 for sq,x in enumerate(bd):
  if x is None:continue
  pt=x.lower();w=x.isupper();v=V.get(pt,0)
  s+=v*(1 if w else -1)+pst(pt,sq,w)*(1 if w else -1)
 return s
def ab(bd,d,a,bx,mx,nt):
 if d<=0 or nt[0]>50000:return ev(bd)
 wc=sum(p.isupper() for p in bd if p)
 co="w" if wc>16 else "b"
 ms=gm(bd,co)
 if not ms:return-99999
 ms.sort(key=lambda m:-V.get(bd[m[1]] or"x",0)*10+V.get(bd[m[0]] or"x",0))
 if mx:
  best=-999999
  for m in ms:
   nt[0]+=1
   sc=-ab(ap(bd,m),d-1,-bx,-a,not mx,nt)
   if sc>best:best=sc
   a=max(a,sc)
   if bx<=a:break
  return best
 best=999999
 for m in ms:
  nt[0]+=1
  sc=-ab(ap(bd,m),d-1,-bx,-a,not mx,nt)
  if sc<best:best=sc
  bx=min(bx,sc)
  if bx<=a:break
 return best
def ch(fen,lg):
 brd=bd(fen);b=None;bs=-999999;nt=[0]
 for u in lg:
  f,t,p=s2i(u[:2]),s2i(u[2:4]),u[4] if len(u)>4 else None
  nt[0]=0;sc=-ab(ap(brd,(f,t,p)),2,-999999,999999,False,nt)
  if sc>bs:bs=sc;b=u
 return b
while True:
 g=post("/game")
 if g["status"]=="done":break
 while g["status"]=="your_move":
  m=ch(g["fen"],g["legal_moves"])
  if not m:post("/resign",{"game":g["game"]});break
  g=post("/move",{"game":g["game"],"move":m})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')}W {g.get('draws')}D {g.get('losses')}L",file=sys.stderr)
