import json,os,sys,urllib.request,urllib.error
E=os.environ["MAKEFUN_ENV_URL"]
V={"p":1,"n":3,"b":3,"r":5,"q":9,"k":100};N=[0]
def post(p,b={}):
 r=urllib.request.Request(E+p,json.dumps(b).encode(),{"ct":"ap/json"})
 try:
  with urllib.request.urlopen(r) as s:return json.load(s)
 except urllib.error.HTTPError:sys.exit(f"{p}:400")
def bd(f):
 b=[None]*64
 for i,r in enumerate(f.split()[0].split("/")):
  c=0
  for ch in r:
   if ch.isdigit():c+=int(ch)
   else:b[i*8+c]=ch;c+=1
 return b
def i2s(i):return f"{'abcdefgh'[i%8]}{8-i//8}"
def s2i(s):return(8-int(s[1]))*8+"abcdefgh".index(s[0])
def gm(bd,co):
 ms=[]
 for sq in range(64):
  x=bd[sq]
  if x is None:continue
  if(co=="w"==x.islower()or co=="b"==x.isupper()):continue
  pt=x.lower()
  if pt=="p":
   d=-8 if co=="w" else 8;pr=0 if co=="w" else 7;sr=6 if co=="w" else 1
   fw=sq+d
   if 0<=fw<64 and bd[fw] is None:
    if fw//8==pr:
     for p in"qnrb":ms.append((sq,fw,p))
    else:ms.append((sq,fw,None))
    if sq//8==sr:
     f2=sq+d*2
     if 0<=f2<64 and bd[f2] is None:ms.append((sq,f2,None))
   for o in(-1,1):
    cp=sq+d+o
    if 0<=cp<64 and abs(cp%8-sq%8)==1:
     t=bd[cp]
     if t and(co=="w"==t.islower()or co=="b"==t.isupper()):
      if cp//8==pr:
       for p in"qnrb":ms.append((sq,cp,p))
      else:ms.append((sq,cp,None))
  elif pt=="n":
   for dd in(-17,-15,-10,-6,6,10,15,17):
    nb=sq+dd
    if 0<=nb<64 and abs(nb%8-sq%8)<=2 and abs(nb//8-sq//8)<=2:
     t=bd[nb]
     if t is None or(co=="w"==t.islower()or co=="b"==t.isupper()):ms.append((sq,nb,None))
  elif pt=="b":
   for dd in(-9,-7,7,9):
    nb=sq+dd
    while 0<=nb<64 and abs(nb%8-(nb-dd)%8)<=1:
     t=bd[nb]
     if t:
      if co=="w"==t.islower()or co=="b"==t.isupper():ms.append((sq,nb,None))
      break
     ms.append((sq,nb,None));nb+=dd
  if pt=="r":
   for dd in(-8,-1,1,8):
    nb=sq+dd
    while 0<=nb<64 and(dd in(-8,8) or nb%8==sq%8):
     t=bd[nb]
     if t:
      if co=="w"==t.islower()or co=="b"==t.isupper():ms.append((sq,nb,None))
      break
     ms.append((sq,nb,None));nb+=dd
  if pt=="q":
   for dd in(-9,-8,-7,-1,1,7,8,9):
    nb=sq+dd
    while 0<=nb<64 and(abs(dd) in(1,8) or abs(nb%8-(nb-dd)%8)<=1):
     t=bd[nb]
     if t:
      if co=="w"==t.islower()or co=="b"==t.isupper():ms.append((sq,nb,None))
      break
     ms.append((sq,nb,None));nb+=dd
  if pt=="k":
   for dd in(-9,-8,-7,-1,1,7,8,9):
    nb=sq+dd
    if 0<=nb<64 and abs(nb%8-sq%8)<=2 and abs(nb//8-sq//8)<=2:
     t=bd[nb]
     if t is None or(co=="w"==t.islower()or co=="b"==t.isupper()):ms.append((sq,nb,None))
 return ms
def ap(bd,m):
 b=list(bd);b[m[1]]=m[2] or bd[m[0]];b[m[0]]=None;return b
def ev(bd):
 s=0
 for sq,x in enumerate(bd):
  if x is None:continue
  pt=x.lower();w=x.isupper();v=V.get(pt,0)
  s+=v*(1 if w else -1)
  if pt=="n" and sq in(27,28,35,36):s+=(1 if w else -1)
  if pt=="b" and sq in(27,28,35,36):s+=(1 if w else -1)
 return s
def ab(bd,d,a,bx,mx):
 if d<=0:return ev(bd)
 wc=sum(p.isupper() for p in bd if p)
 co="w" if wc>16 else "b"
 ms=gm(bd,co)
 if not ms:return-9999+(1 if mx else 0)*9999
 ms=sorted(ms,key=lambda m:V.get(bd[m[1]] or"x",0)*10-V.get(bd[m[0]] or"x",0),reverse=True)
 if mx:
  best=-99999
  for m in ms:
   N[0]+=1
   if N[0]>15000:break
   sc=-ab(ap(bd,m),d-1,-bx,-a,not mx);best=max(best,sc);a=max(a,sc)
   if bx<=a:break
  return best
 best=99999
 for m in ms:
   N[0]+=1
   if N[0]>15000:break
   sc=-ab(ap(bd,m),d-1,-bx,-a,not mx);best=min(best,sc);bx=min(bx,sc)
   if bx<=a:break
 return best
def ch(fen,lg):
 bd=bd(fen);b=None;bs=-99999
 for u in lg:
  f,t,p=s2i(u[:2]),s2i(u[2:4]),u[4] if len(u)>4 else None
  N[0]=0;sc=-ab(ap(bd,(f,t,p)),3,-99999,99999,False)
  if sc>bs:bs=sc;b=u
 return b
while True:
 g=post("/game")
 if g["status"]=="done":break
 while g["status"]=="your_move":
  m=ch(g["fen"],g["legal_moves"])
  if not m:post("/resign",{"game":g["game"]});break
  g=post("/move",{"game":g["game"],"move":m})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",f=sys.stderr)
print(f"done: {g.get('wins')}W {g.get('draws')}D {g.get('losses')}L",f=sys.stderr)
