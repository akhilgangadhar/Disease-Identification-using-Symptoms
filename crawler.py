import os
import bs4 as bs
import urllib.request
import urllib.parse as parse

class Scrapper:
	def __init__(self,base_url):
		self.base_url = base_url
		self.first_layer_links = set()
		self.second_layer_links = set()
		self.path = 'queue.txt';

	def create_project_dir(self):
		if not os.path.exists(self.project_name):
			print('Creating project '+ self.project_name)
			os.makedirs(self.project_name)

	def write_file(self,data):
		f = open(self.path, 'w')
		f.write(data)
		f.close()

	def create_data_files(self):
		if not os.path.isfile(self.path):
			self.write_file('')

	def get_links_first_layer(self):
		sauce = urllib.request.urlopen(self.base_url).read()
		soup = bs.BeautifulSoup(sauce,'lxml')

		ol = soup.find('ol',class_ = 'alpha')
		a_tags = ol.find_all('a')
		for a_tag in a_tags:
			url = parse.urljoin(self.base_url,a_tag.get('href'))
			self.first_layer_links.add(url)
		return self.first_layer_links;

	def get_links_second_layer(self,url):
		sauce = urllib.request.urlopen(url).read()
		soup = bs.BeautifulSoup(sauce,'lxml')

		div = soup.find('div',class_ = 'index')
		ol = div.find('ol')

		a_tags = ol.find_all('a')
		for a_tag in a_tags:
			url = parse.urljoin(self.base_url,a_tag.get('href'))
			self.second_layer_links.add(url)
		return self.second_layer_links;

	def append_to_file(self, data):
		with open(self.path,'a') as file:
			file.write(data + '\n')

	def delete_file_contents(self):
		with open(self.path, 'w'):
			pass

	def set_to_file(self,links):
		self.delete_file_contents()
		for link in sorted(links):
			self.append_to_file(link)

if __name__ == '__main__':
	s = Scrapper('https://www.mayoclinic.org/diseases-conditions/index?letter=A')
	s.create_data_files();
	s.first_layer_links = s.get_links_first_layer();
	for link in s.first_layer_links:
		s.get_links_second_layer(link)
	s.set_to_file(s.second_layer_links)


