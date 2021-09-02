# Your imports go here
import logging
import json
import os

logger = logging.getLogger(__name__)

'''
    Given a directory with receipt file and OCR output, this function should extract the amount

    Parameters:
    dirpath (str): directory path containing receipt and ocr output

    Returns:
    float: returns the extracted amount

'''
def extract_amount(dirpath: str) -> float:

    logger.info('extract_amount called for dir %s', dirpath)

    for file in os.listdir(dirpath):
	    f = open(os.path.join(dirpath,r'ocr.json'))
	    data = json.load(f)
	    f.close()

	    for i in data['Blocks']:
	      if i['BlockType'] == 'PAGE':
	        w,h = i['Geometry']['BoundingBox']['Width'],i['Geometry']['BoundingBox']['Height']
	        offset = i['Geometry']['Polygon'][1]['Y'] - i['Geometry']['Polygon'][0]['Y']
	        break
	    
	    
	    amount = []
	    loc = []
	    if 0.85 < h/w < 1:
	        for i in data['Blocks']:
	          try:
	            if (i['Text'][0]) == '$' and len(i['Text'][1:]) > 0 :
	                amount.append(float(i['Text'][1:].replace(',','').replace(' USD','')))
	          except KeyError:
	            None 

	    else:
	      for i in data['Blocks']:
	        try:
	          if i['Text'] =='TOTAL' or i['Text'] == 'Total' or i['Text'] == 'CREDIT' or i['Text'] == 'Amount' or i['Text'] == 'PAID' or i['Text'] == 'Total:' or i['Text'] == 'Payment': 
	            y = i['Geometry']['Polygon'][1]['Y']
	            loc.append(y)
	        except KeyError:
	          None
	      lim = 0.00
	      amount = []
	      if loc != []:
	        while amount == []:
	          try:
	            for i in data['Blocks']:
	              a = i['Geometry']['Polygon'][1]['Y'] -  offset
	              for j in loc:
	                if j + lim  >= a and j - lim  <= a:               
	                  text = i['Text']
	                  try:
	                    if type(float(text)) == float:
	                      amount.append(float(text))
	                  except ValueError:
	                    None
	                  try:
	                    if type(float(text[1:])) == float:
	                      amount.append(float(text[1:]))
	                  except ValueError:
	                    None
	          except KeyError:
	            None
	          lim += 0.01

	      else:
	        if amount == []:
	          for i in data['Blocks']:
	            try: 
	              if (i['Text'][0]) == '$' and len(i['Text'][1:]) > 0 :
	                  amount.append(float(i['Text'][1:].replace(',','').replace(' USD','')))
	            except KeyError:
	              None 
    return max(amount)
