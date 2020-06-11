#!/usr/bin/env python
# coding: utf-8

# In[6]:


#######################################################################################
## Claim tracker and draw odds calculator for secrethitler.io by H3R0
#######################################################################################
## License information: Not licensed
#######################################################################################
## Author: Roland Herman
## Copyright: Copyright 2020, H3RO
## Credits: H3RO
## License: Not licensed
## Version: 3.2
## Maintainer: Roland Herman
## Email: herman.roland@gmail.com
## Status: Completed
#######################################################################################
## Version control:
## 1.0 - Initial version with basic GUI and calculator
## 1.1 - Bug fix: limit set for number of policies (fascist 0-11, liberal 0-6)
## 2.0 - Major improvement: scrape claims with selenium webdriver
## 2.1 - New function: scrape investigation
## 2.2 - New function: scrape TD
## 3.0 - Major improvement: calculate remaining policies automatically based on claims
## 3.1 - Prettier GUI
## 3.2 - Exception handling: missing claim
#######################################################################################


## 1 Import modules ##
# GUI
import tkinter as tk

# Web scraping
from selenium import webdriver #
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BSoup

# Executable
import os.path
import sys

############################################################################################################################################################

## 2 Calculation of odds ##

# 2.1 Set default values
faspol_left = 11 #fascists policies left
libpol_left = 6 #liberal policies left

# 2.2 Define functions 
# Increase fascist policies left by 1
def faspol_increase():
    value = int(lbl_faspol_left["text"])
    if value < 11:
        lbl_faspol_left["text"] = f"{value + 1}"
    odds_calc()

# Decrease fascist policies left by 1
def faspol_decrease():
    value = int(lbl_faspol_left["text"])
    if value > 0:
        lbl_faspol_left["text"] = f"{value - 1}" 
    odds_calc()

# Increase liberal policies left by 1
def libpol_increase():
    value = int(lbl_libpol_left["text"])
    if value < 6:
        lbl_libpol_left["text"] = f"{value + 1}"
    odds_calc()

# Decrease liberal policies left by 1 
def libpol_decrease():
    value = int(lbl_libpol_left["text"])
    if value > 0:
        lbl_libpol_left["text"] = f"{value - 1}"
    odds_calc()

# Reset default values
def reset():
    lbl_libpol_left["text"] = libpol_left
    lbl_faspol_left["text"] = faspol_left
    lbl_bbb_pct["text"] = "2.94%"
    lbl_rrr_pct["text"] = "24.26%"
    lbl_bbr_pct["text"] = "24.26%"
    lbl_brr_pct["text"] = "48.53%"
    lbl_libtop_pct["text"] = "35.29%"
    lbl_fastop_pct["text"] = "64.71%"
    txtbox_claims.delete('1.0', tk.END)
    txtbox_gameurl.delete('1.0', tk.END)
    txtbox_notes.delete('1.0', tk.END)
    global driver
    driver.quit()
    #driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
    driver = webdriver.Chrome(resource_path('chromedriver.exe'))
    
# Calculate cards draw odds
def odds_calc():
    libleft = int(lbl_libpol_left["text"]) #fascist policies left
    fasleft = int(lbl_faspol_left["text"]) #liberal policies left
    cardsleft = libleft + fasleft #total policies left
    
    if cardsleft > 2:
        bbb = (libleft/cardsleft) * (libleft-1)/(cardsleft-1) * (libleft-2)/(cardsleft-2) * 100 #odds of drawing bbb
        rrr = (fasleft/cardsleft) * (fasleft-1)/(cardsleft-1) * (fasleft-2)/(cardsleft-2) * 100 #odds of drawing rrr
        bbr = (libleft/cardsleft) * (libleft-1)/(cardsleft-1) * (fasleft)/(cardsleft-2) * 3 * 100 #odds of drawing bbr
        brr = (libleft/cardsleft) * (fasleft)/(cardsleft-1) * (fasleft-1)/(cardsleft-2) * 3 * 100 #odds of drawing brr
    else:
        bbb = 0
        rrr = 0
        bbr = 0
        brr = 0
    
    if cardsleft > 0:
        libtop = libleft/cardsleft * 100 #odds of topdecking liberal policy
        fastop = fasleft/cardsleft * 100 #odds of topdecking fascist policy
    else:
        libtop = 0
        fastop = 0
    
    # assign odds to labels
    lbl_bbb_pct.config(text="%.2f" % bbb + '%')
    lbl_rrr_pct.config(text="%.2f" % rrr + '%') 
    lbl_bbr_pct.config(text="%.2f" % bbr + '%')
    lbl_brr_pct.config(text="%.2f" % brr + '%')
    
    lbl_libtop_pct.config(text="%.2f" % libtop + '%')
    lbl_fastop_pct.config(text="%.2f" % fastop + '%')
    
############################################################################################################################################################

## 3 Web Scraping claims ##
# 3.1 Scraping webdriver parameters
chrome_options = Options()
chrome_options.add_argument('--no-proxy-server') #performance tuning: no proxy
chrome_options.add_argument("--proxy-server='direct://'") #performance tuning: no proxy
chrome_options.add_argument("--proxy-bypass-list=*") #performance tuning: no proxy
chrome_options.add_argument('--blink-settings=imagesEnabled=false') #performance tuning: disable images
chrome_options.page_load_strategy='eager' #performance tuning: This stategy causes Selenium to wait for the DOMContentLoaded event (html content downloaded and parsed only).
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--start-maximized")
chrome_options.headless = True #performance tuning: headless browser
chrome_options.add_argument("--mute-audio") #disable sounds
    
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #slower than local driver
#driver = webdriver.Chrome("chromedriver.exe", options=chrome_options) #relative link, driver in same folder

# needed for executable
def resource_path(relative_path):
    try: 
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('chromedriver.exe'), options=chrome_options)
#------------------------------------------------------------------------------------------------------------------------------------------------------------

# 3.2 Define functions
# Load game
def load_game():
    driver.get(txtbox_gameurl.get("1.0", "end")) #loads url from textbox
    driver.find_element_by_xpath("/html/body/div/section/section/div[2]/section/section/div[1]/div/div[2]/section[2]/section[1]/a[1]/i").click() # turn off player chat

# Scrape claims
def getclaims():   
    # parameters
    claims=[] #list to store claims
    president_claims=[] #list to store president claims
    chancellor_claims=[] #list to store chancellor claims
    lib_policies_enacted = 0 #no of lib policies enacted
    fas_policies_enacted = 0 #no of fas policies enacted
    lib_policies_discarded_deck1 = 0 #no of lib policies discarded in first deck
    fas_policies_discarded_deck1 = 0 #no of fas policies discarded in first deck
    txtbox_claims.delete('1.0', tk.END) #delete textbox content
    bs_obj = BSoup(driver.page_source, 'lxml') #bs4 lxml for better performance
    claimitems = bs_obj.findAll("div", {"class": "claim-item"}) #getting html elements -- bs4 for better performance
    claimlist = [claim.text for claim in claimitems] #getting text from html element
    inv_index = [] #investigation index list -- to paste claim after 2nd fas policy is enacted
    inv_index_pos = 0 #unpacked inv_index to get the actual number (position)
    policies_draw = ''
    missing_claim = 0 #if prez or chanc doesn't claim, default is 0
  
    # iterate over claims
    for claim in claimlist:
        if claim.split(' ')[3] == 'sees': #investigation
            if claim.split(' ')[18] == 'liberal':
                inv = (claim.split(' ')[2]).replace('{','').replace('}','') + ' invs ' + (claim.split(' ')[9]).replace('{','').replace('}','') + ' ' + claim.split(' ')[18]            
                inv_index = [idx for idx, claim in enumerate(claimlist) if claim.split(' ')[3] == 'sees']
                inv_index_pos = int(inv_index[0])//2 #e.g 2 fasc policies and 0 lib policies enacted --> 4 claims, postion is at 4/2 = 2
            else:
                inv = (claim.split(' ')[2]).replace('{','').replace('}','') + (claim.split(' ')[9]).replace('{','').replace('}','') + ' inv conf'
                inv_index = [idx for idx, claim in enumerate(claimlist) if claim.split(' ')[3] == 'sees']
                inv_index_pos = int(inv_index[0])//2
        elif claim.split(' ')[0] == 'President': #president claims
            president_claims.append((claim.split(' ')[2] + ' ' + claim.split(' ')[4][0:-1]).replace('{','').replace('}',''))
            policies_draw += claim.split(' ')[4][0:-1]
        elif claim.split(' ')[0] == 'Chancellor': #chancellor claims
            chancellor_claims.append((claim.split(' ')[2] + ' ' + claim.split(' ')[4][0:-1]).replace('{','').replace('}',''))
    
    # getting claim pairs and identifying conflicts
    for i in range(len(president_claims)):
        try:
            if (president_claims[i].split(' ')[1] == 'RBB' and chancellor_claims[i].split(' ')[1] == 'RR'):
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1] + ' conf')
                fas_policies_enacted += 1
                if i<5:
                    lib_policies_discarded_deck1 += 2
            elif (president_claims[i].split(' ')[1] == 'RRB' and chancellor_claims[i].split(' ')[1] in('BB','RR')): #BB meme claim
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1] + ' conf')
                fas_policies_enacted += 1
                if i<5:
                    fas_policies_discarded_deck1 += 1
                    lib_policies_discarded_deck1 += 1
            elif (president_claims[i].split(' ')[1] == 'BBB' and chancellor_claims[i].split(' ')[1] == 'RR'): #meme claim rrr
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' RRR')
                fas_policies_enacted += 1
                if i<5:
                    fas_policies_discarded_deck1 += 2
            elif (president_claims[i].split(' ')[1] == 'BBB' and chancellor_claims[i].split(' ')[1] == 'BB'):
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1])
                lib_policies_enacted += 1
                if i<5:
                    lib_policies_discarded_deck1 += 2
            elif (president_claims[i].split(' ')[1] == 'RRR' and chancellor_claims[i].split(' ')[1] in('BB','RR')): #BB meme claim
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1])
                fas_policies_enacted += 1
                if i<5:
                    fas_policies_discarded_deck1 += 2
            elif (president_claims[i].split(' ')[1] == 'RBB' and chancellor_claims[i].split(' ')[1] == 'BB'):
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1])
                lib_policies_enacted += 1
                if i<5:
                    lib_policies_discarded_deck1 += 1
                    fas_policies_discarded_deck1 += 1
            elif (president_claims[i].split(' ')[1] == 'RRB' and chancellor_claims[i].split(' ')[1] == 'RB'):
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1])
                lib_policies_enacted += 1
                if i<5:
                    fas_policies_discarded_deck1 += 2
            elif (president_claims[i].split(' ')[1] == 'RBB' and chancellor_claims[i].split(' ')[1] == 'RB'): #choicing
                claims.append(president_claims[i].split(' ')[0] + chancellor_claims[i].split(' ')[0] + ' ' + president_claims[i].split(' ')[1] + ' choicing')
                lib_policies_enacted += 1
                if i<5:
                    lib_policies_discarded_deck1 += 1
                    fas_policies_discarded_deck1 += 1
        except IndexError: #if prez or chanc doesn't claim
                missing_claim = 1
                   
    # insert inv claim after second fas policy enacted
    if inv_index_pos > 0:
        claims.insert(inv_index_pos, inv) 
     
    # insert tds after tracker maxed
    tdlist = []
    tds = []
    tditems = bs_obj.findAll("div", {"class": "game-chat"})
    td_lib = 0
    td_fas = 0
    trackermaxed_txt = "The third consecutive election has failed and the top policy is enacted."
    
    # find when tracker is maxed and top policy is enacted
    for tditem in tditems:
        if tditem.text.startswith("The third") or tditem.text.startswith("A liberal policy") or tditem.text.startswith("A fascist policy"):
            tdlist.append(tditem.text)
    
    # add TD to list
    if trackermaxed_txt in tdlist:
        tdlist.index(trackermaxed_txt)
        tdidxs = [idx for idx,td in enumerate(tdlist) if td == trackermaxed_txt]
        for idx in tdidxs:
            if tdlist[idx+1].split(' ')[1] == 'fascist':
                tds.append('TD R ' + str(idx))
                td_fas += 1
            else:
                tds.append('TD B ' + str(idx))
                td_lib += 1
    
    # add TD to claims
    for td in tds:
        if inv_index_pos > 0:
            claims.insert(int(td.split(' ')[2])+1, td.split(' ')[0] + ' ' + td.split(' ')[1])
        else:
            claims.insert(int(td.split(' ')[2]), td.split(' ')[0] + ' ' + td.split(' ')[1])

    # insert claims into txtbox
    if missing_claim == 1:
        txtbox_claims.insert(tk.END, "Missing claim")
    else:
        for claim in claims:
            txtbox_claims.insert(tk.END, claim + '\n')
        
    # count claimed policies in decks
    if len(policies_draw) < 27: #deck 1 & 2
        fas_policies_claimed = policies_draw.count('R')
        lib_policies_claimed = policies_draw.count('B')
    else: #deck 3
        fas_policies_claimed = policies_draw[27:].count('R')
        lib_policies_claimed = policies_draw[27:].count('B')
    
    # calculate remaining policies
    if lib_policies_enacted + fas_policies_enacted < 5: #deck 1
        lbl_libpol_left["text"] = libpol_left-lib_policies_claimed-td_lib
        lbl_faspol_left["text"] = faspol_left-fas_policies_claimed-td_fas
    elif (lib_policies_enacted + fas_policies_enacted + td_lib) == 5 or (lib_policies_enacted + fas_policies_enacted + td_fas) == 9: #after reshuffles
        lbl_libpol_left["text"] = libpol_left-lib_policies_enacted-td_lib
        lbl_faspol_left["text"] = faspol_left-fas_policies_enacted-td_fas
    elif lib_policies_enacted + fas_policies_enacted + td_fas + td_lib > 9: #deck 3
        lbl_libpol_left["text"] = libpol_left-lib_policies_enacted-td_lib-lib_policies_claimed
        lbl_faspol_left["text"] = faspol_left-fas_policies_claimed-td_fas-fas_policies_claimed
    else: # deck 2  
        lbl_libpol_left["text"] = libpol_left-lib_policies_claimed+lib_policies_discarded_deck1-td_lib
        lbl_faspol_left["text"] = faspol_left-fas_policies_claimed+fas_policies_discarded_deck1-td_fas
        
    odds_calc()

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# Refresh claims -- incremental -- inactive function
def refresh_claims():
    bs_obj = BSoup(driver.page_source, 'lxml')
    claimitems = bs_obj.findAll("div", {"class": "claim-item"})
    claimlist = [claim.text for claim in claimitems]
    
    claimsr = []
    president_claimsr = []
    chancellor_claimsr = []
    global lib_policies_enacted
    global fas_policies_enacted
    
    for claim in claimlist:
        if claim.split(' ')[3] == 'sees': #investigation
            if claim.split(' ')[18] == 'liberal':
                inv = (claim.split(' ')[2]).replace('{','').replace('}','') + ' invs ' + (claim.split(' ')[9]).replace('{','').replace('}','') + ' ' + claim.split(' ')[18]            
            else:
                inv = (claim.split(' ')[2]).replace('{','').replace('}','') + (claim.split(' ')[9]).replace('{','').replace('}','') + ' inv conf'
        elif claim.split(' ')[0] == 'President':
            president_claimsr.append((claim.split(' ')[2] + ' ' + claim.split(' ')[4][0:-1]).replace('{','').replace('}',''))
        elif claim.split(' ')[0] == 'Chancellor':
            chancellor_claimsr.append((claim.split(' ')[2] + ' ' + claim.split(' ')[4][0:-1]).replace('{','').replace('}',''))
    
    if (president_claimsr[-1].split(' ')[1] in('RBB','RRB') and chancellor_claimsr[-1].split(' ')[1] == 'RR'):
        claimsr.append(president_claimsr[-1].split(' ')[0] + chancellor_claimsr[-1].split(' ')[0] + ' ' + president_claimsr[-1].split(' ')[1] + ' conf')
        fas_policies_enacted += 1
    elif (president_claimsr[-1].split(' ')[1] == 'RRB' and chancellor_claimsr[-1].split(' ')[1] == 'BB'): #meme claim
        claimsr.append(president_claimsr[-1].split(' ')[0] + chancellor_claimsr[-1].split(' ')[0] + ' ' + president_claimsr[-1].split(' ')[1] + ' conf')
        fas_policies_enacted += 1
    elif (president_claimsr[-1].split(' ')[1] == 'BBB' and chancellor_claimsr[-1].split(' ')[1] == 'RR'): #meme claim rrr
        claimsr.append(president_claimsr[-1].split(' ')[0] + chancellor_claimsr[-1].split(' ')[0] + ' RRR')
        fas_policies_enacted += 1
    else:
        claimsr.append(president_claimsr[-1].split(' ')[0] + chancellor_claimsr[-1].split(' ')[0] + ' ' + president_claimsr[-1].split(' ')[1])
        if president_claimsr[-1].split(' ')[1] == 'RRR':
            fas_policies_enacted += 1
        else:
            lib_policies_enacted += 1
            
    policies_drawr = president_claimsr[-1].split(' ')[1]
    fas_policies_claimed = policies_drawr.count('R')
    lib_policies_claimed = policies_drawr.count('B')
       
    #insert inv claim into textbox
    if claimlist[-1].split(' ')[3] == 'sees':
        claimsr.append(inv)
        txtbox_claims.insert(tk.END, claimsr[-1] + '\n')        
 
    if len(president_claims) < len(president_claimsr):
        txtbox_claims.insert(tk.END, claimsr[-1] + '\n')
        president_claims.append((claimlist[-1].split(' ')[2] + ' ' + claimlist[-1].split(' ')[4][0:-1]).replace('{','').replace('}',''))
        if (lib_policies_enacted + fas_policies_enacted) == 5 or (lib_policies_enacted + fas_policies_enacted) == 9: #after reshuffles
            lbl_libpol_left["text"] = libpol_left-lib_policies_enacted
            lbl_faspol_left["text"] = faspol_left-fas_policies_enacted
        else: #if app not run from start of game
            lbl_libpol_left["text"] = lbl_libpol_left["text"]-lib_policies_claimed
            lbl_faspol_left["text"] = lbl_faspol_left["text"]-fas_policies_claimed
            
        odds_calc()
     
    if lib_policies_enacted == 5:
        txtbox_claims.insert(tk.END, 'Liberals win the game')
    elif fas_policies_enacted == 6:
        txtbox_claims.insert(tk.END, 'Fascists win the game')
        
############################################################################################################################################################

## 4 GUI ##
# Main window
window = tk.Tk() #initialize
window.title("[sh.io] Claim Tracker & Calculator by H3R0") 
window.geometry("395x355")
window.configure(background='gray12')
window.iconbitmap("hit.ico") #relative link, icon in same folder

# quit driver when closing app via window manager
def on_closing():
    driver.quit()
    window.destroy()

# color and font settings
main_color = "gray12"
alt_color = "gray20"
font_color = "white"
fas_color = "#D7020F"
lib_color = "#4169E1"
fnt = "Helvetica"
load_color = "#AB47BC"
reset_color = "limegreen"
getclaim_color = "#FF6F00"

# Widgets
# Game url
lbl_gameurl = tk.Label(window, text='Game:', bg=main_color, fg=font_color)
lbl_gameurl.place(x=15, y=15)

txtbox_gameurl = tk.Text(window, height=1, width = 30, font=(fnt, 10), fg=font_color, bg=alt_color, borderwidth=0)
txtbox_gameurl.place(in_=lbl_gameurl, relx=1.0, relheight=1.0, bordermode="outside")

# Load game
btn_load_game = tk.Button(master=window, text="Load", command=load_game, height = 1, width = 6, font="fnt 10 bold", fg=font_color, bg=load_color, borderwidth=0)
btn_load_game.place(in_=txtbox_gameurl, relx=1, relheight=1.0, bordermode="outside")

# Reset game
btn_reset = tk.Button(master=window, text="Reset", fg=font_color, bg=reset_color, command=reset, height = 1, width = 6, font="fnt 10 bold", borderwidth=0)
btn_reset.place(in_=btn_load_game, relx=1.0, relheight=1.0, bordermode="outside")

# Remaining fascist policies
btn_faspol_decrease = tk.Button(master=window, text="-", command=faspol_decrease, height = 1, width = 1, font=(fnt, 11), fg=font_color, bg=alt_color, borderwidth=0)
btn_faspol_decrease.place(x=20, y=80)
lbl_fas = tk.Label(window, text="Fas policy left", font=(fnt, 8), fg=font_color, bg=main_color)
lbl_fas.place(in_=btn_faspol_decrease, rely=-1.0, relheight=1.0, bordermode="outside")
lbl_faspol_left = tk.Label(window, text=faspol_left, fg=font_color, bg=fas_color, height = 1, width = 3, font=(fnt, 14))
lbl_faspol_left.place(in_=btn_faspol_decrease, relx=1.0, relheight=1.0, bordermode="outside")
btn_faspol_increase = tk.Button(master=window, text="+", command=faspol_increase, height = 1, width = 1, font=(fnt, 11), fg=font_color, bg=alt_color, borderwidth=0)
btn_faspol_increase.place(in_=lbl_faspol_left, relx=1.0, relheight=1.0, bordermode="outside")

# Remaining liberal policies
btn_libpol_decrease = tk.Button(master=window, text="-", command=libpol_decrease, height = 1, width = 1, font=(fnt, 11), fg=font_color, bg=alt_color, borderwidth=0)
btn_libpol_decrease.place(x=110, y=80)
lbl_lib = tk.Label(window, text="Lib policy left", font=(fnt, 8), fg=font_color, bg=main_color)
lbl_lib.place(in_=btn_libpol_decrease, rely=-1.0, relheight=1.0, bordermode="outside")
lbl_libpol_left = tk.Label(window, text=libpol_left, fg=font_color, bg=lib_color, height = 1, width = 3, font=(fnt, 14))
lbl_libpol_left.place(in_=btn_libpol_decrease, relx=1.0, relheight=1.0, bordermode="outside")
btn_libpol_increase = tk.Button(master=window, text="+", command=libpol_increase, height = 1, width = 1, font=(fnt, 11), fg=font_color, bg=alt_color, borderwidth=0)
btn_libpol_increase.place(in_=lbl_libpol_left, relx=1.0, relheight=1.0, bordermode="outside")

# Draw and TD Odds
lbl_draw = tk.Label(window, text='Draw',font=(fnt, 10), fg=font_color, bg=main_color)
lbl_draw.place(x=20, y=115)

lbl_td = tk.Label(window, text='Topdeck',font=(fnt, 10), fg=font_color, bg=main_color)
lbl_td.place(x=110, y=115)

# RRR
lbl_rrr = tk.Label(window, text='RRR', fg=font_color, bg=alt_color)
lbl_rrr.place(x=20, y=140)
lbl_rrr_pct = tk.Label(window, text='24.26%', bg=fas_color, fg=font_color)
lbl_rrr_pct.place(in_=lbl_rrr, relx=1.05, relheight=1.0, bordermode="outside")

# BBB
lbl_bbb = tk.Label(window, text='BBB', fg=font_color, bg=alt_color)
lbl_bbb.place(x=20, y=170)
lbl_bbb_pct = tk.Label(window, text='2.94%', bg=lib_color, fg=font_color)
lbl_bbb_pct.place(in_=lbl_bbb, relx=1.05, relheight=1.0, bordermode="outside")

# RBB
lbl_bbr = tk.Label(window, text='RBB', fg=font_color, bg=alt_color)
lbl_bbr.place(x=20, y=200)
lbl_bbr_pct = tk.Label(window, text='24.26%', bg=lib_color, fg=font_color)
lbl_bbr_pct.place(in_=lbl_bbr, relx=1.05, relheight=1.0, bordermode="outside")

# RRB
lbl_brr = tk.Label(window, text='RRB', fg=font_color, bg=alt_color)
lbl_brr.place(x=20, y=230)
lbl_brr_pct = tk.Label(window, text='48.53%', bg=lib_color, fg=font_color)
lbl_brr_pct.place(in_=lbl_brr, relx=1.05, relheight=1.0, bordermode="outside")

# TD R
lbl_fastop = tk.Label(window, text='R', fg=font_color, bg=alt_color)
lbl_fastop.place(x=110, y=140)
lbl_fastop_pct = tk.Label(window, text='64.71%', bg=fas_color, fg=font_color)
lbl_fastop_pct.place(in_=lbl_fastop, relx=1.05, relheight=1.0, bordermode="outside")

# TD B
lbl_libtop = tk.Label(window, text='B', fg=font_color, bg=alt_color)
lbl_libtop.place(x=110, y=170)
lbl_libtop_pct = tk.Label(window, text='35.29%', bg=lib_color, fg=font_color)
lbl_libtop_pct.place(in_=lbl_libtop, relx=1.05, relheight=1.0, bordermode="outside")

# Button for scraping claims
btn_scrape = tk.Button(master=window, text="Get claims", command=getclaims, height = 1, width = 21, font="fnt 10 bold", fg=font_color, bg=getclaim_color, borderwidth=0)
btn_scrape.place(x=200, y=63)

# Textbox for claims with scrollbar
txtbox_claims = tk.Text(window, fg=font_color, bg=alt_color)
txtbox_claims.place(in_=btn_scrape, rely=1.3, relheight=7.0, relwidth=0.9, bordermode="outside")
scrollb_claims = tk.Scrollbar(window,command=txtbox_claims.yview)
scrollb_claims.place(in_=txtbox_claims, relx=1.0, relheight=1.0, bordermode="outside")
txtbox_claims['yscrollcommand'] = scrollb_claims.set

# Textbox for notes with scrollbar
lbl_notes = tk.Label(window, text='Notes:', bg=main_color, fg=font_color)
lbl_notes.place(in_=lbl_brr, rely=1.7, relheight=1.0, bordermode="outside")
txtbox_notes = tk.Text(window, height=1, width = 42, fg=font_color, bg=alt_color, borderwidth=0)
txtbox_notes.place(in_=lbl_notes, rely=1, relheight=2.5, bordermode="outside")
scrollb_notes = tk.Scrollbar(window,command=txtbox_notes.yview)
scrollb_notes.place(in_=txtbox_notes, relx=1.0, relheight=1.0, bordermode="outside")
txtbox_notes['yscrollcommand'] = scrollb_notes.set

# Refresh claims button -- inactive
#btn_refresh = tk.Button(master=window, text="Refresh claims", command=refresh_claims, height = 1, width = 11, font=(fnt, 11))
#btn_refresh.place(x=340, y=35)

# close window
window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()


# In[ ]:




