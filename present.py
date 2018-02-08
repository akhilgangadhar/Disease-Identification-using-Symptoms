import os
import bs4 as bs
import urllib.request
import urllib.parse as parse
import sqlite3
import pandas as pd

conn = sqlite3.connect('diseases.db')
c = conn.cursor();
l = ['Symptoms','Causes'];


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS diseases(Id REAL,Name TEXT,Symptoms TEXT,Causes TEXT)')

def data_entry(id,name,symptoms,causes):
	c.execute('INSERT INTO diseases (Id,Name,Symptoms,Causes) VALUES(?,?,?,?)',(id,name,symptoms,causes))
	conn.commit()
	#c.close()
	#conn.close()

def read_from_db():
	#c.execute('SELECT * FROM diseases')
	#for row in c.fetchall():
	#	print(row)
	df = pd.read_sql_query('SELECT * FROM diseases',conn);
	print(df.head())

def file_to_set(file_name):
	results = set()
	with open(file_name, 'r') as f:
		for line in f:
			results.add(line.replace('\n',''))
	return results

def get_data(id,url):
		sauce = urllib.request.urlopen(url).read()
		soup = bs.BeautifulSoup(sauce,'lxml')
		#dic = dict()
		u = []
		h1 = soup.find('h1')
		#dic["Name"] = h1.get_text()
		u.append(h1.get_text())
		div = soup.find('div',class_ = 'content')

		h2_tag = div.find('h2')
		while h2_tag is not None:
			if h2_tag.get_text() in l:
				#print(h2_tag.get_text())
				if h2_tag.nextSibling is not None:
					#print(h2_tag.nextSibling.get_text())
					#dic[h2_tag.get_text()] = h2_tag.nextSibling.get_text().replace('\n','')
					s = h2_tag.nextSibling.get_text().replace('\n','')
					if h2_tag.find_next_sibling("ul") is not None:
						s = s + h2_tag.find_next_sibling("ul").get_text().replace('\n',' ')
					#q = dic[h2_tag.get_text()]+s;
					#dic[h2_tag.get_text()] = q;
					u.append(s)
			h2_tag = h2_tag.find_next_sibling("h2")
		#print(u)
		if len(u) == 3:
			#data_entry(id,dic["Name"],dic["Symptoms"],dic["Causes"])
			data_entry(id,u[0],u[1],u[2])
		#print(dic)
				

if __name__ == '__main__':
	create_table();
	results = file_to_set('queue.txt')
	id = 0
	for link in results:
		id += 1
		get_data(id,link)
	c.close()
	conn.close() 
	#read_from_db()
	#c.close()
	#conn.close()