import sys, os.path
import requests, re, json, urllib
from file import *
from time import sleep
from urllib2 import URLError, HTTPError, Request, urlopen

s = requests.Session()

def box(isi,kolor):
	bx = '{0}[{1}{2}{3}] '.format(
		r,kolor,isi,r
		)
	return bx

## admin finder
def adm_finder(site):
	sys.stdout.write(box("+",h)+"Scanning ...\r")
	sys.stdout.flush()
	if site.startswith("http://") is False:
		site = "http://"+site
	for i in admin_path:
		target = site+"/"+i
		try:
			req = Request(target)
			ope = urlopen(req)
		except URLError, HTTPError:
			continue
		except KeyboardInterrupt:
			break
		else:
			print box("+",h)+"FOUND: "+target

## http header information
def hthead(site):
	if site.startswith("http://") is False:
		site = "http://"+site
	try:
		for nisa,sabyan in s.get(site).headers.items():
			print box("+",h)+nisa+": "+sabyan; sleep(0.10)
	except:
		print "\n"+box("1",m)+"check your connection.\n"+box("2",m)+"invalid domain."

## subdomain scanner
def sub(site):
	if site.startswith('http') or site.startswith('https') is True:
		site = site.replace('http','').split('://')[1]

	try:
		res = urlopen('https://www.pagesinventory.com/search/?s=%s'%site).read()
		regx = re.findall('<td><a href=\"\/domain\/(.*?).html\">',res)
		if not regx:
			print box("!",m)+"query: "+site
			print box("!",m)+"Nothing was found"
		else:
			for foran in regx:
				print box("+",h)+foran; sleep(0.10)

	except (URLError, HTTPError) as er:
		print box("!",m)+"ERROR: "+str(er.reason)

	except KeyboardInterrupt:
		pass

## backdoor scanner
def backscan(site):
	sys.stdout.write(box("+",h)+"Scanning ...\r")
	sys.stdout.flush()
	if site.startswith("http://") is False:
		site = "http://"+str(site)
	for word_back in backdoor_path:
		try:
			target = site+"/"+word_back
			req = Request(target)
			bukaan = urlopen(req)
		except (URLError, HTTPError):
			continue
		except KeyboardInterrupt:
			break
		else:
			print box("+",h)+"FOUND: "+target

## dump all friends id
def dump_f(token,result_path="module/id_result.txt"):
	try:
		req = Request("https://graph.facebook.com/me/friends?access_token=%s"%token)
		ope = urlopen(req)
		text = ope.read()
		tojs = json.loads(text)
		gr = "="*30
		for i in tojs["data"]:
			try:
				hasil = "name: {0}\nid: {1}\n{2}\n".format(i['name'],i['id'],gr)
				open(result_path,"a+").write(''.join(hasil).encode('utf-8'))
			except (UnicodeEncodeError, KeyError):
				pass
		print box("+",h)+"id saved to: %s"%result_path
	except URLError:
		print "\n"+box("x",m)+"check your connection."

## facebook auto update status
def up_stat(**kwargs):
	data = {
		"id":kwargs["id"],
		"token":kwargs["token"],
		"message":kwargs["mess"]
	}
	
	url = "https://graph.facebook.com/"+data['id']+"/feed?message="+data['message']+"&access_token="+data["token"]
	try:
		req = s.post(url).text
		tojson = json.loads(req)
		if tojson.get("post_supports_client_mutation_id") is True:
			print box("+",h)+"Status update success"
		else:
			print box("!",m)+"FAILED: check your token valid and id."
	except requests.exceptions.RequestException:
		pass
