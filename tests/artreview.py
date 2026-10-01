# Ask Gemini (vision) to review stage renders for scale problems. usage: python3 tests/artreview.py PKL OUTJSON   (PKL from the venues.py render script: {id:[PIL frames]})
import sys,json,base64,subprocess,io,pickle,os
from concurrent.futures import ThreadPoolExecutor
PROMPT=("This is a 2D pixel-art game stage: the red-haired player on the left and a caller on the right are each about 95 pixels tall, standing on the stage floor; the held guitars are about 45 pixels long. "
"Review ONLY the proportions and scale of the painted background props relative to these two characters (for example a guitar, amp, stool, table, door, window or jukebox that is far too big or too small to be real next to them). "
"Ignore art style. Reply with strict JSON: {\"issues\":[{\"object\":\"...\",\"where\":\"left|centre|right, high|low\",\"problem\":\"too big|too small\",\"severity\":1-3,\"fix\":\"...\"}],\"overall\":\"ok|minor|needs work\"}. Use an empty issues list if all is in proportion.")
def review(item):
    i,im=item; b=io.BytesIO(); im.save(b,'PNG')
    body=json.dumps({"contents":[{"parts":[{"text":PROMPT},{"inlineData":{"mimeType":"image/png","data":base64.b64encode(b.getvalue()).decode()}}]}],"generationConfig":{"responseMimeType":"application/json"}})
    rq=f"/tmp/req_rev_{i}.json"; open(rq,'w').write(body)
    r=subprocess.run(["curl","-sS","-X","POST","https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent","-H","Content-Type: application/json","-d","@"+rq],capture_output=True,text=True)
    try: return i,json.loads(json.loads(r.stdout)['candidates'][0]['content']['parts'][0]['text'])
    except Exception as e: return i,{'error':str(e)[:120],'raw':r.stdout[:200]}
if __name__=='__main__':
    d=pickle.load(open(sys.argv[1],'rb')); items=[(i,v[0]) for i,v in d.items()]
    with ThreadPoolExecutor(4) as ex: res=dict(ex.map(review,items))
    json.dump(res,open(sys.argv[2],'w'),indent=1)
    for i,r in res.items(): print(i,r.get('overall',r.get('error')),'|',[ (x['object'],x['problem'],x['severity']) for x in r.get('issues',[])])
