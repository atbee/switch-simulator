#####################################################################################
#              [198 340 Computer Networks] Project Switch Simulator                 #
#  By Mr.Athibet Prawane 593040685-3 and Mr.Chalermchai Viriyamanatham 593040658-6  #
#####################################################################################
import time
import forwarding_table as table

seconds = 5


def timer():
    global seconds
    for i in range(seconds, -1, -1):
        time.sleep(1)
        if i == 0:
            table.removeTable()
            timer()


timer()
