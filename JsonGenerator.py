#coding=utf-8
import json

def generate(str_json):
	hasnext = 0
	msgs = list()
	ret = json.loads(str_json)
	data = ret.get('data',{})
	if data is None:
		print ret
	else:
		hasnext = str(data.get('hasnext',None))
		items = data.get('info',[])
		for item in items:
			pics = item.get('pic',None)
			image_url = None
			if pics is not None:
				for image in pics['info']:
					image_url = ''.join(image['url']) + '/460.jpg'
					break
				if image_url is not None:
					content = str(item['text'] + image_url).encode('utf-8')
					msgs.append(content)
	return msgs,hasnext