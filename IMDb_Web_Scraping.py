#IMDb Web Scraping - Top 10,000 Films. 

#packages required

"""pip install beautifulsoup4
pip install requests
pip install lxml
pip install python-csv"""


#importing modules

from bs4 import BeautifulSoup
import requests
import lxml
import csv

#creating file to store the data into a csv file

file2=open("Top 10K Movies.csv","w")
writer=csv.writer(file2)
writer.writerow(["Movie","Year","Duration","Rating","Genre","Metascore","Gross","Vote","Director","Stars"])

#Website of Top 10,000 Films

url="https://www.imdb.com/search/title/?num_votes=10000,&sort=user_rating,desc&title_type=feature"
html=requests.get(url,"lxml").text
soup=BeautifulSoup(html)
films=soup.find_all("div",class_="lister-item mode-advanced")

#creating empty list for storing

votes=[]
grosses=[]
movies=[]
pages=[]

#creating for loop to append page value for scraping next next pages

for i in range(0,10000):
    if (i%50 == 0):
        pages.append(i)

#for loop to pass the next page movies list for scraping 

for page in pages:
  url=f"https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&sort=user_rating,desc&start={page}&ref_=adv_nxt"
  html=requests.get(url,"lxml").text
  soup =BeautifulSoup(html)
  films=soup.find_all("div",class_="lister-item mode-advanced")

  #scraping information regarding movies
  for f in films:
    movie=f.h3.a.text 
    year=f.h3.find("span",class_="lister-item-year text-muted unbold").text.replace("(","").replace(")","")
    duration=f.p.find("span",class_="runtime").text
    rating=f.find("div",class_="inline-block ratings-imdb-rating").text.strip()
    genre=f.p.find("span",class_="genre").text.strip()
    values=f.find_all("span",attrs={'name':'nv'})
    vote=values[0].text
    gross=values[1].text if len(values)>1 else "-----"
    metascore=f.find("span",class_="metascore").text if f.find("span",class_="metascore") else "---"
    director=f.find("p",class_="").find_all("a")[0].text
    star=[actor.text for actor in f.find('p',class_='').find_all('a')[1:]]
    stars=str(star)[1:-1]
    movies.append(movie)

    writer.writerow([movie,year,duration,rating,genre,metascore,gross,vote,director,stars])

file2.close()


