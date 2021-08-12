import requests
import csv

page = 1

token = ""
headers = {"Authorization": "token " + token}

true = True




def make_repo_list():

    new_repos_list = []

    new_repo_data = open("new-repos.txt", "r")
    new_repos = new_repo_data.readlines()
    new_repo_data.close()


    for i in new_repos:
        c = i.strip()
        new_repos_list.append(c)
    for z in new_repos_list:
        if z == " ":
            new_repos_list.pop(z)

    return new_repos_list



def get_data_and_write_table(new_repos_list):

    global true
    global page 
    global headers

    for p in new_repos_list:
        
        contributors = {}

        while true:

            response = requests.get(url=f"https://api.github.com/repos/{p}/contributors?per_page=100&page={page}", headers=headers)
        
            yes = response.json()

            if yes == []:
                break

            for t in yes:
                contributors[t["login"]] = {"contributions": t["contributions"],}

            page +=1
            #IT IS THE PAGE THE GLOBAL VARIABLE UPDATES WHICH IS WHY THE NEXT REPOS ARE EMPTY!!!!
        
        page = 1

    
        for c in contributors:
            next_response = requests.get(url=f"https://api.github.com/users/{c}", headers=headers)

            next_yes = next_response.json()

            contributors[c]["email"] = next_yes["email"]
            contributors[c]["real_name"] = next_yes["name"]
            contributors[c]["website"] = next_yes["blog"]
            contributors[c]["hireable"] = next_yes["hireable"]
            contributors[c]["company"] = next_yes["company"]
            contributors[c]["location"] = next_yes["location"]

        filename = p.split("/")[1]

        newfile = open(filename + ".csv", "w", encoding="utf-8", newline='')
        newfile.write("GITHUB-NAME,CONTRIBUTIONS-TO-REPO,EMAIL,REAL-NAME,LOCATION,HIREABLE,COMPANY,WEBSITE\n")
        csv_writer = csv.writer(newfile)
        for i in contributors:
            newest_list = []
            newest_list.append([i, contributors[i]['contributions'], contributors[i]['email'], contributors[i]['real_name'], contributors[i]['location'], contributors[i]['hireable'], contributors[i]['company'], contributors[i]['website']])
            csv_writer.writerow(newest_list[0])
        newfile.close()

def arrange_documents(new_repos_list):
    list = []

    file = open("used-repos.txt", "r")
    read_file = file.readlines()
    for b in read_file:
        c = b.strip()
        list.append(c)
    
    for i in list:
        if i in new_repos_list:
            new_repos_list.remove(i)
    file.close()

    
    file = open("used-repos.txt", "a")
    for i in new_repos_list:
        file.write(f"\n{i}")
    file.close()

    new_repos = open("new-repos.txt", "w")
    new_repos.truncate()
    new_repos.close()

    
repo_list = make_repo_list()
get_data_and_write_table(repo_list)
arrange_documents(repo_list)
