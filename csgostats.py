import re

from dateutil.parser import parse as parse_date

from csgostats_net import *

class MatchInfo():
    pass

def get_match_list_for_userid(browser, steamid):
    url = "https://csgostats.gg/player/" + str(steamid)
    return get_match_list_for(browser, url)

def get_match_list_for(browser, url):
    matches = []

    req = make_request(browser, url, (By.CLASS_NAME, 'has-banned'))
    if req == True:
        list_parent = browser.find_element_by_id("match-list-outer")
        match_rows = list_parent.find_elements_by_css_selector(".p-row.has-banned")

        for row in match_rows: 
            link_elem = row.find_elements_by_css_selector("[title='View Match']")[0]
            href_val = link_elem.get_attribute("href")
            match_id = re.match(r"^.+(\d+)$", href_val).group()
            matches.append({'id': match_id, 'url': href_val})
        
    return matches

def get_match(browser, m):
    req = make_request(browser, m['url'], (By.ID, 'content-tabs'))
    if req: 
        date_elem = browser.find_elements_by_css_selector("#match-details>div>div")[-1]
        date_text = date_elem.get_attribute("innerHTML")
        d = parse_date(date_text)

        match_players_parent = browser.find_elements_by_id("content-tabs")[0]
        banned_players = match_players_parent.find_elements_by_css_selector(".has-banned")
        print("    Match ", m['id'], " on ", d, " has ", len(banned_players), " banned player(s)")

        for banned_player in banned_players:
            player_name_link_elem = banned_player.find_element_by_css_selector("a.player-link")
            player_name_elem = player_name_link_elem.find_element_by_css_selector("span")
            player_name = player_name_elem.get_attribute("innerHTML")

            playerprofile_url = player_name_link_elem.get_attribute("href")
            playersteamid = re.match(r"^.+/(\d+)$", playerprofile_url).groups()[0]

            print("    Banned-player:", player_name, "   //  Steam ID: ", playersteamid)