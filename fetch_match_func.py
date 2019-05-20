def fetch_match(url):
    from bs4 import BeautifulSoup
    from datetime import datetime
    import pandas as pd
    import requests
    import re

    print("Start Fetching: ", url)
    souped_content = BeautifulSoup(requests.get(url).text)
    team_left = souped_content.find("h3", {"class": "report-squadra squadra-a"}).get_text()
    team_right = souped_content.find("h3", {"class": "report-squadra squadra-b"}).get_text()

    names_home_formation_raw_ls = souped_content.find("section", {"class": "report-formazioni"}).find_all("tbody")[0].find_all("tr") # get_text()
    names_guest_formation_raw_ls = souped_content.find("section", {"class": "report-formazioni"}).find_all("tbody")[1].find_all("tr") # get_text()
    names_home_bench_raw_ls = souped_content.find("section", {"class": "report-panchina"}).find_all("tbody")[0].find_all("tr") # get_text()
    names_guest_bench_raw_ls = souped_content.find("section", {"class": "report-panchina"}).find_all("tbody")[1].find_all("tr") # get_text()

    names_home_formation_ls = []
    names_guest_formation_ls = []
    names_home_bench_ls = []
    names_guest_bench_ls = []

    for name_raw in names_home_formation_raw_ls:
        names_home_formation_ls.append(re.sub("[^a-zA-Z ]", "", name_raw.get_text()).strip())

    for name_raw in names_guest_formation_raw_ls:
        names_guest_formation_ls.append(re.sub("[^a-zA-Z ]", "", name_raw.get_text()).strip())

    for name_raw in names_home_bench_raw_ls:
        names_home_bench_ls.append(re.sub("[^a-zA-Z ]", "", name_raw.get_text()).strip())

    for name_raw in names_guest_bench_raw_ls:
        names_guest_bench_ls.append(re.sub("[^a-zA-Z ]", "", name_raw.get_text()).strip())

    info_ls = re.sub("\n+", "\n", souped_content.find("div", {"class": "report-data"}).get_text().strip()).split("\n")


    date = datetime.strptime(info_ls[0].strip(), "%d/%m/%Y - %H:%M")
    stadium = info_ls[1].strip().split(":")[1].strip()
    referee = info_ls[2].strip().split(":")[1].strip()
    status = info_ls[3].strip()

    score_home = None
    score_guest = None

    if status == "Finished":
        score_home = souped_content.find("div", {"class": "squadra-risultato squadra-a"}).get_text().strip()
        score_guest = souped_content.find("div", {"class": "squadra-risultato squadra-b"}).get_text().strip()

    res = pd.DataFrame([("home_formation", name) for name in names_home_formation_ls] +
                       [("guest_formation", name) for name in names_guest_formation_ls] +
                       [("home_bench", name) for name in names_home_bench_ls] +
                       [("guest_bench", name) for name in names_guest_bench_ls], columns = ["team", "player"])
    res["date"] = date
    res["stadium"] = stadium
    res["referee"] = referee
    res["status"] = status
    res["score_home"] = score_home
    res["score_guest"] = score_guest
    res["url"] = url

    return res
