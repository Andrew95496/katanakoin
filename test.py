# # # from wallet_key_generator import wallet_key_gen
# # from config import configs as cf
# # import psycopg2
# # # # wallet_key_gen()

# # # from create_tables import create_tables
# # # from katanakoins import generate_coins
# # # from wallet import buy_coins, create_wallet, send_coins


# # # # create_wallet('5022f42b976ce57797e67c03e2c4e07ed1b4ab71b8e764cdb2594414bb6c0b45')
# # # # create_wallet('226a31631f1522cdeb2beaa29066fb7bff7c219dcaa71f05db417f96fe5def29')

# # # # generate_coins(100)

# # # send_coins('226a31631f1522cdeb2beaa29066fb7bff7c219dcaa71f05db417f96fe5def29', 
# # # '560647fdb08290e4b5be3761b65cd8198cc73e0b435b3c800ca25d1f23677b93',
# # # 'aa70a9d1e64d835d0fc4c2313966a9a8292456109217fa9f240ab0ecf7c3f746',
# # # 1)


# # conn = None
# #     cur = None
# #     try:
# #         conn = psycopg2.connect(
# #             host = cf.hostname,
# #             dbname = cf.database,
# #             user = cf.username,
# #             password = cf.pwd,
# #             port = cf.port_id)

# #         # cursor
# #         cur = conn.cursor()
# #         cur.execute(f"SELECT * FROM transactions{address} ORDER BY timestamp DESC LIMIT 5")
# #         transactions = cur.fetchall()
# #         if transactions:
# #             for tran in transactions:
# #                 f'''Sender address: {tran[0]}\n
# #             Receiver address: {tran[1]}\n
# #             Amount: {transactions[2]}\n
# #             Timestamp: {transactions[3]}\n\n
# #             '''
# #         else:
# #             print("wrong")


# text = f'''Sender address: {transactions[i][j]}\n
#                     Receiver address: {transactions[i][j]}\n
#                     Amount: {transactions[i][j]}\n
#                     Timestamp: {transactions[i][j]}\n\n
#                     '''

# cur.execute(f'SELECT * FROM katanakoins ORDER BY  coin_number DESC LIMIT {amount_to_gen}')
#         for serial in cur.fetchall():
#             print(f'''\n{bcolors.OKBLUE}Coin #:{bcolors.ENDC} {bcolors.WARNING}{serial[0]}{bcolors.ENDC}
#             \n{bcolors.OKBLUE}Serial #:{bcolors.ENDC} {bcolors.BOLD}{serial[1]}{bcolors.ENDC}
#             \n{bcolors.OKBLUE}Hash:{bcolors.ENDC} {bcolors.BOLD}{serial[2]}{bcolors.ENDC}
#             \n{bcolors.OKBLUE}Owner:{bcolors.ENDC} {bcolors.WARNING}{serial[3]}{bcolors.ENDC}
#             \n{bcolors.OKBLUE}Timestamp:{bcolors.ENDC} {bcolors.WARNING}{serial[4]}{bcolors.ENDC}''')
