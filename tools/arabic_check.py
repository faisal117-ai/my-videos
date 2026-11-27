import json,sys,subprocess,base64,re
d,i=sys.argv[1],int(sys.argv[2]);PH=sys.argv[3] if len(sys.argv)>3 else "Hasbunallahu wa ni'mal wakeel, or Astaghfirullah";S="/tmp"  # usage: python3 tools/arabic_check.py <short-id> <line-index> (run from repo root)
t=json.load(open(f"shorts/{d}/assets/timings.json"))
subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",str(t[i]["start"]),"-to",str(t[i]["end"]),"-i",f"shorts/{d}/assets/narration.wav","-ac","1","-ar","16000",f"{S}/x.mp3"],check=True)
a=base64.b64encode(open(f"{S}/x.mp3","rb").read()).decode()
body={"contents":[{"parts":[{"inline_data":{"mime_type":"audio/mp3","data":a}},{"text":"Listen to the Arabic phrase in this clip (expected: "+PH+"). Reply ONLY with JSON: {\"verdict\":\"YES\" or \"NO\",\"why\":\"short reason\"}. YES means a listener would clearly hear the correct Arabic words (غ as a fricative, not an English hard g)."}]}],"generationConfig":{"responseMimeType":"application/json"}}
open(f"{S}/b.json","w").write(json.dumps(body))
r=json.loads(subprocess.run(["curl","-sS","-H","x-goog-api-key: proxy-injected","-H","Content-Type: application/json","-d",f"@{S}/b.json","https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"],capture_output=True,text=True).stdout)
v=json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
print(v["verdict"],"|",v["why"][:150])
