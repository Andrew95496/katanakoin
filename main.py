from tkinter import *
import psycopg2
import easygui
from config import configs as cf
from wallet import buy_coins, create_wallet, send_coins
from wallet_key_generator import wallet_key_gen



root = Tk()
root.title('KatanaKoin')
root.iconbitmap('c:/Users/drewskikatana/Downloads/katanakoin-main/katanakoin/images/favicon.ico')
root.state("zoomed")

# GET KEY AND CREATE WALLET!!!
# button to generate wallet key
wallet_gen_btn = Button(root, text="Create Key",
padx=50, pady=30, 
command=wallet_key_gen,
)

# button to create wallet key
key = Entry(root)
key.insert(0, "Enter Private Key")
create_wallet_btn = Button(root, text="Create Wallet",
padx=50, pady=30, 
command=lambda: create_wallet(key.get())
)
#Wallet Page
address = Entry(root)
address.insert(0, "Enter Wallet address")
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
            myLabel = Label(root, text=text, fg="green")
            myLabel.place(x=90, y=335)
            myLabel.after(30000, myLabel.destroy)
        else:
            myLabel = Label(root, text=f"NO wallet{address} WAS FOUND", fg="red" )
            myLabel.place(x=1150, y=370,anchor='s')
            myLabel.after(30000, myLabel.destroy)


        #queries
    
        conn.commit()

    except Exception as error:
        print(error)
        myLabel = Label(root, text=f"WALLET FOR '{address}' DOES NOT EXIST", fg="red" )
        myLabel.place(x=1150, y=420,anchor='s')
        myLabel.after(3000, myLabel.destroy)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

trans_key = Entry(root)
trans_key.insert(0, "Enter Wallet Address")
def get_recent_transactions(trans_key):
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
        cur.execute(f'SELECT count(*) FROM wallet{trans_key}')
        amount_to_gen = cur.fetchone()
        cur.execute(f'SELECT * FROM transactions{trans_key} ORDER BY timestamp DESC LIMIT 5')
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
show_transactions_btn = Button(root, text="Show Wallet",
padx=50, pady=30, 
command= lambda: get_recent_transactions(trans_key.get())
)

#Buy coins Button
buy_key = Entry(root)
buy_address = Entry(root)
buy_amount = Entry(root)
buy_key.insert(0, "Enter Private Key")
buy_address.insert(0, "Enter Wallet address")
buy_amount.insert(0, "Buy Amount")
buy_coins_btn = Button(root, text="Buy Coins",
padx=50, pady=30, 
command=lambda: buy_coins(buy_key.get(), buy_address.get(), int(buy_amount.get())))


#Send Money
send_key = Entry(root)
send_address = Entry(root)
receiver_address = Entry(root)
send_amount = Entry(root)
send_key.insert(0, "Enter Private Key")
send_address.insert(0, "Enter Wallet Address")
receiver_address.insert(0, "Enter Address Payment Receiver")
send_amount.insert(0, "Send Amount")
send_coins_btn = Button(root, text="Send Coins",
relief=GROOVE,
padx=50, pady=30, 
command=lambda: send_coins(send_key.get(), send_address.get(), receiver_address.get(),int(send_amount.get())))


#Displays

#wallet key generator, creator display, and show
create_wallet_title = Label(root, text="CREATE WALLET")
create_wallet_title.place(x=350, y=50)
wallet_gen_btn.place(x=100, y=100)
key.place(x=520, y=190)
create_wallet_btn.place(x=508, y=100)
address.place(x=307, y=190)
show_wallet_btn.place(x=300, y=100)
trans_key.place(x=100, y=280)
show_transactions_btn.place(x= 100, y= 190 )

#Buy coins display
buy_key.place(x=953, y=190)
buy_address.place(x=953, y=230)
buy_amount.place(x=953, y=270)
buy_coins_btn.place(x=951, y=100)

#Send coins display
send_key.place(x=1150, y=190)
send_address.place(x=1150, y=230)
receiver_address.place(x=1150, y=270)
send_amount.place(x=1150, y=310)
send_coins_btn.place(x=1145, y=100)

#Transaction
transactions_title = Label(root, text="WALLET INFORMATION")
transactions_title.place(x=330, y=310)

root.mainloop()
