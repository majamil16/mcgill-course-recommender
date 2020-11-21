from bs4 import BeautifulSoup
import hashlib
import os.path as osp
import requests


def get_page_contents(url, cache_dir, verbose,use_cache=True):
	"""
	Returns the HTML of the selected page. Saves to a cache directory for fast lookup the next time that page neeeds to be accessed.

	All pages are of the form mcgill.ca/study/... so just fill in the page number
	"""
	#url=f"https://www.mcgill.ca/study/2020-2021/courses/search?page={page_num}"
	fname = hashlib.sha1(url.encode('utf-8')).hexdigest() # hash the url so we can save the cache
	full_fname = osp.join(cache_dir, fname)
	if osp.exists(full_fname) and use_cache: #if the page has already been cached...
		if(verbose):
			print(f"Loading {url} from cache")
		contents = open(full_fname, 'r').read()
		
	else:
		if(verbose):
			print(f"Loading {url} from source")
		r = requests.get(url)
		contents = r.text
		with open(full_fname, 'w') as f: # write the cache
			f.write(contents)
	return contents, full_fname # return the full hashed fname so we can use it...


def find_total_num_pages(filename):
	"""
	Finds the total number of page sin the ecalendar. Should only have to use this once in a while, like once every time the script is run bc there shouldn't be that many pages being added/removed...
	"""
	soup =	BeautifulSoup(open(filename, 'r'), 'html.parser')
	total_num_courses_li = soup.find("li", "pager-last last")
	total_num_courses_a = total_num_courses_li.find('a')
	num_courses_link = total_num_courses_a['href']
	num_pages = num_courses_link.split('=')[-1]
	total_num_pages = int(num_pages)
	return total_num_pages



def scrape_all_course_names(filename, verbose):
	""" 
	Find all the CourseName, CourseNumber, of McGill classes from the ecalendar, as well as the max number of pages in the ecalendar.

	input:
	------
	filename = the saved HTML of the page you want to extract info from 
	"""
   
	soup =	BeautifulSoup(open(filename, 'r'), 'html.parser')
	#print(soup)
	courses = []
	# all the courses are stored in a div w/class=view-content
		
	h4_field_content = soup.find('h4', 'field-content')
	#print(h4_field_content)
	all_course_content = soup.find("div", "view-content") # this contains ALL the classes...
	if all_course_content == None:
		print("There are no courses on this page. Try a smaller page number!")
		return []
	
	candidate_classes  = all_course_content.find_all('a') # we want all the 'a' tags within
	class_list=[]
        course_code_and_number = {}
	for c in candidate_classes:
		#print(c.text, "\n")
		text = c.text # ex. AEMA 611 Experimental Designs 1 (3 credits)
		text = text.split(" ")# split on the space
		course_id = " ".join(text[:2]).replace('\n', '') # the first 2 are the course id
		course_name = " ".join(text[2:-2]).replace('\n', '')
		num_credits = text[-2].replace("(", "")# just get the course number, replace the ( with nothing 
	
	
		#print(f"{course_id}\n{course_name}\n{num_credits}\n")
		try:# Check that the course number is a digit bc sometimes it is something weird
			float(num_credits)
		except ValueError:
			#print(f"Wrong course format. Ignoring {c}")
			if(verbose):
				print(f"Wrong course format. Ignoring course: {c.text}")
			continue
		class_list.append(course_id)
	return class_list


def scrape_all_course_info():
	return
	# https://www.mcgill.ca/study/2020-2021/courses/ansc-250


def main():

	fname = "page1.html"
	total_num_pages = find_total_num_pages(fname) 
	print(total_num_pages)
	cache_dir = ".cache" 
	base_url = "https://www.mcgill.ca/study/2020-2021/courses/search?page="
	for i in range(1,25):   # only use some cached pages for now for efficiency# total_num_pages):
		 new_page = base_url + str(i)
		 contents, hashed_fname = get_page_contents(new_page,cache_dir , verbose=True)
		 print(scrape_all_course_names(hashed_fname, verbose=True))
	   
		
if __name__ == "__main__":
	main()
