from tkinter import *
from ttkbootstrap import Style
from PIL import Image, ImageTk


from bs4 import  BeautifulSoup
import requests
import threading

import easygui
import psycopg2


from config import configs as cf
from wallet import buy_coins, create_wallet, send_coins
from wallet_key_generator import wallet_key_gen

root = Tk()
style = Style(theme='superhero')
root.title('KatanaKoin')
root.state("zoomed")
root.configure(background='#383537')

#STYLES
#colors
main_gray = '#383537'
dark_gray = '#262325'
helio_gray = '#A3999F'
purple = '#420122'

# ADD LOGO
Logo = Image.open("/Users/drewskikatana/katanakoin/images/KATANAKOINS-LOGO-TRANSPARENT.png")
Logo = Logo.resize((200, 200), Image.ANTIALIAS)
test = ImageTk.PhotoImage(Logo)

main_logo = Label(image=test, bg=f"{main_gray}" )
main_logo.place(x=1000, y=0)


#Backgrouds

#Login background
login_bg = Label(root, text="", bg=f"{dark_gray}", padx=162, pady=38)
login_bg.place(x=90,y=63)

#create wallet backgroud
create_wallet_bg = Label(root, text="", bg=f"{dark_gray}", padx=309, pady=112)
create_wallet_bg.place(x=90,y=240)

#wallet info background
wallet_info_bg = Label(root, text="", bg=f"{dark_gray}", padx=309, pady=50)
wallet_info_bg.place(x=90,y=500)

#buy and sell background
buy_send_bg = Label(root, text="", bg=f"{dark_gray}", padx=199, pady=112)
buy_send_bg.place(x=940,y=240)

#instructions background
instructions_bg = Label(root, text="", bg=f"{dark_gray}", padx=199, pady=150)
instructions_bg.place(x=940,y=500)

#Enter private key and wallet address
key = Entry(root, width=50)
key.insert(0, "Enter Private Key")
address = Entry(root, width=50)
address.insert(0, "Enter Wallet address")


# GET KEY AND CREATE WALLET!!!
# button to generate wallet key
key_gen_btn = Button(root, text="Create Key",
padx=50, pady=30, 
command=wallet_key_gen,
)

# button to create wallet key
create_wallet_btn = Button(root, text="Create Wallet",
padx=50, pady=30, 
command=lambda: create_wallet(key.get())
)

#Get price
def get_price():
        result = requests.get('https://crypto.com/price/shiba-inu')
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')
        price = soup.find("span", {"class": "chakra-text"}).get_text(" ", strip=True)
        coin_price = Label(root, text=price, font=('Ariel', 25), bg=f'{main_gray}')
        coin_price.place(x=610, y=150)
        print(price)
        threading.Timer(1, get_price).start()

#show price
get_price()
        

#Wallet Page
#get user page
def user_page(address):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)
        # cursor
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM wallet{address}")
        wallet = cur.fetchone()
        if wallet:
            text = f'''\nWALLET KEY: {wallet[1]}\nWALLET ADDRESS: {wallet[2]}\nBALANCE: {wallet[3]}'''
            myLabel = Label(root, text=text, fg="green", bg="#262325")
            myLabel.place(x=390, y=539, anchor="n")
            myLabel.after(30000, myLabel.destroy)
        else:
            myLabel = Label(root, text=f"NO wallet{address} WAS FOUND", fg="red", bg="#262325" )
            myLabel.place(x=390, y=530, anchor="n")
            myLabel.after(30000, myLabel.destroy)

        #queries
        conn.commit()
    except Exception as error:
        print(error)
        myLabel = Label(root, text=f"WALLET FOR '{address}' DOES NOT EXIST", fg="red", bg="#262325")
        myLabel.place(x=390, y=530, anchor="n")
        myLabel.after(3000, myLabel.destroy)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

#get recent transactions
def get_recent_transactions(key):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)
        
        # cursor
        cur = conn.cursor()

        #queries
        recent_trans = []
        cur.execute(f'SELECT count(*) FROM wallet{key}')
        amount_to_gen = cur.fetchone()
        cur.execute(f'SELECT * FROM transactions{key} ORDER BY timestamp DESC LIMIT 5')
        if amount_to_gen[0] > 0:
            for serial in cur.fetchall():
                transact = f'''\nSender Address: {serial[0]}
                \nReceiver Address: {serial[1]}
                \nAmount: {serial[2]}
                \nTimestamp: {serial[3]}'''
                recent_trans.append(transact)
            easygui.msgbox(recent_trans)
        else:
            easygui.msgbox("NO TRANSACTIONS MADE")
        
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# button to create wallet key
show_wallet_btn = Button(root, text="Show Wallet",
padx=50, pady=30, 
command= lambda: user_page(address.get())
)


# button to see recent transactions
show_transactions_btn = Button(root, text="Transactions",
padx=50, pady=30, 
command= lambda: get_recent_transactions(address.get())
)

#Buy coins Button
buy_amount = Entry(root, width=28)
buy_amount.insert(0, "Buy Amount")
buy_coins_btn = Button(root, text="Buy Coins",
padx=50, pady=30, 
command=lambda: buy_coins(key.get(), address.get(), int(buy_amount.get())))


#Send Money
receiver_address = Entry(root, width=28)
send_amount = Entry(root, width=28)
receiver_address.insert(0, "Enter Receiver Address ")
send_amount.insert(0, "Send Amount")
send_coins_btn = Button(root, text="Send Coins",
relief=GROOVE,
padx=50, pady=30, 
command=lambda: send_coins(key.get(), address.get(), receiver_address.get(),int(send_amount.get())))


#Displays

#main title
main_title = Label(root, text="Katanakoins", bg=f'{main_gray}', font=('Ariel', 100))
main_title.place(x=475, y=20)


#wallet logins display
login_title = Label(root, text="LOGIN", bg=f"{dark_gray}")
login_title.place(x=230, y=70)
key.place(x=100, y=100)
address.place(x=100, y=120)

#wallet key generator, creator, and show display
create_wallet_title = Label(root, text="CREATE WALLET", bg=f"{dark_gray}")
create_wallet_title.place(x=350, y=250)

key_gen_btn.place(x=100, y=300)
show_wallet_btn.place(x=302, y=300)
create_wallet_btn.place(x=508, y=300)
show_transactions_btn.place(x= 302, y= 390 )


#Buy coins and Send coins display
buy_and_send_title = Label(root, text="BUY AND SEND COINS", bg=f'{dark_gray}')
buy_and_send_title.place(x=1080, y=250)

buy_coins_btn.place(x=951, y=300)
buy_amount.place(x=953, y=400)

send_coins_btn.place(x=1145, y=300)
receiver_address.place(x=1149, y=400)
send_amount.place(x=1149, y=440)

#Wallet info
wallet_info_title = Label(root, text="WALLET INFORMATION", bg=f'{dark_gray}')
wallet_info_title.place(x=330, y=510)

#Instructions
instructions_title = Label(root, text="INSTRUCTIONS", bg=f'{dark_gray}')
info = '''
*** STORE YOUR KEY AND ADDRESS SOMEWHERE ***\n
*** SO YOU CAN ACCESS IT AGAIN! ****\n\n\n
1. click CREATE KEY to get your PRIVATE KEY\n
copy and paste your private key into login\n\n
2. click CREATE WALLET to get your wallet address\n
copy and paste your address into login\n
'''
instructions_title.place(x=1095, y=510)
instructions_info = Label(root, text=f'{info}', bg=f'{dark_gray}')
instructions_info.place(x=1000, y=560)

easygui.msgbox(info)

root.mainloop()
