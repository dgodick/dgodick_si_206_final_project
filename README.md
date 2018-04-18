# Danielle Godick Final Project SI 206

1. Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))

	-I chose to use the Washington Post for this project, where I crawled and scraped multiple pages in this site, which is a site I have not used before. The link for the Washington Post is https://www.washingtonpost.com.

	-I have set up a secrets.py file which contains my plotly login information.

2. Any other information needed to run the program (e.g., pointer to getting started info for plotly)

	-For this project, I used plotly to create my visualizations. Plotly requires a login to access my visualizations. Here are the instructions for getting started on plotly:

		-Create an account by creating a username and password. In addition, you will need to install plotly for Python by typing "pip install plotly" on your terminal. Once that is done, you can set your credentials by running the following lines in terminal:

			import plotly
			plotly.tools.set_credentials_file(username='YOUR_USERNAME', api_key='YOUR API KEY')

		-For complete directions on using plotly in Python, here is the link: https://plot.ly/python/getting-started/ 

3. Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.

	-The structure of my code begins with creating the database using sql. I create the two different tables within my database, titled Articles and Sections. Then, I create the cache, where data from the site will be stored. The next part of my code includes my class, where the section name and link is stored using a tuple and can be displayed to the user using the str method. The next two functions, get_sections and get_articles, are where the database gets populated and is where the scraping and crawling occurs.

	-The next part of my code includes 4 functions, get_opinions, get_politics, get_world, and get_home, that fetch the headline and link from the 4 different sections based on their section id. These functions are later used for the interactivity of my code.

	-I created a function for each of the 4 visualizations I created. The code within each function uses plotly to create various graphs.

4. Brief user guide, including how to run the program and how to choose presentation options.

	-The first thing that the user will be asked for is to enter a section id number (1-4) or enter "charts." If the user enters a section id number, then the user will see the article headlines and links that correspond to that section id number.

	-If the user enters "charts," he or she will be shown the 4 different titles of the graphs that I created with corresponding numbers (1-4) and will be asked which type of chart he/she would like to see. For example, if the user inputs 1, he or she will be taken to a plotly graph that displays a pie chart of the distribution of articles by section.

	-If the user wishes to exit the code, he or she will simply type "exit." If the user needs help, he/she will type "help" for assistance.