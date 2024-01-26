from netmiko import ConnectHandler
import csv

output =[]
f = open("ipList.txt", "r")
ipList = f.read().split("\n")

for ip in ipList:
    try:
        MT = {
            'device_type': 'mikrotik_routeros',
            'host': ip,
            'username': 'pt',
            'password': 'pt2024',
            'conn_timeout': 30,
            'banner_timeout': 30,
            'port': '8989'
        }
        net_connect = ConnectHandler(**MT)

        # check IDENTY
        check_identy = net_connect.send_command('system identity print', read_timeout=15000)
        identy_result = check_identy.split("\n")

        # check socks
        check_socks = net_connect.send_command('ip socks print', read_timeout=15000)
        socks_result = check_socks.split("\n")

        # check DNS Remote Request
        check_DNS = net_connect.send_command('ip dns print', read_timeout=15000)
        DNS_result = check_DNS.split('\n')

        # check proxy check
        check_proxy = net_connect.send_command('ip proxy print', read_timeout=15000)
        proxy_result = check_proxy.split('\n')

        # check PPTP server status
        check_PPTP_SERVER_STATUS = net_connect.send_command('interface pptp-server server print', read_timeout=15000)
        PPTP_SERVER_STATUS_result = check_PPTP_SERVER_STATUS.split('\n')

        # check L2TP server status
        check_L2TP_SERVER_STATUS = net_connect.send_command('interface l2tp-server server print', read_timeout=15000)
        L2TP_SERVER_STATUS_result = check_L2TP_SERVER_STATUS.split('\n')

        # check OVPN server status
        check_OVPN_SERVER_STATUS = net_connect.send_command('interface ovpn-server server print', read_timeout=15000)
        OVPN_SERVER_STATUS_result = check_OVPN_SERVER_STATUS.split('\n')

        # check SSTP server status
        check_SSTP_SERVER_STATUS = net_connect.send_command('interface sstp-server server print', read_timeout=15000)
        SSTP_SERVER_STATUS_result = check_SSTP_SERVER_STATUS.split('\n')

        # check USERS
        check_USER_STATUS = net_connect.send_command('user print', read_timeout=15000)
        USER_STATUS_result = check_USER_STATUS.split('\n')
        user_count = 0
        for e in USER_STATUS_result:
            user_count = user_count+1
            if (user_count>=3):
                aaa = e.split(" ")
                print(aaa[5])


        # check script status
        check_SCRIPT = net_connect.send_command('system script print', read_timeout=15000)
        SCRIPT_row_result = check_SCRIPT.split('\n')
        SCRIPT_result = []
        for e in SCRIPT_row_result:
            if (len(e) > 80):
                x = e.split('"')
                y = "Name=", x[1], " Owner=", x[3]
                SCRIPT_result.append(y)



        # output final filter
        id = identy_result[0].split(":")
        socks = socks_result[0].split(":")
        DNS = DNS_result[4].split(":")
        PPTP = PPTP_SERVER_STATUS_result[0].split(":")
        L2TP = L2TP_SERVER_STATUS_result[0].split(":")
        SSTP = SSTP_SERVER_STATUS_result[0].split(":")
        #OVPN = OVPN_SERVER_STATUS_result
        Web_Proxy = proxy_result[0].split(":")
        USER = USER_STATUS_result

        # output
        #print(USER)
        print("==================================")
        print("[+] IP : ", ip)
        print("ID: ", id[1])
        print("Socks: ", socks[1])
        print("DNS: ", DNS[1])
        print("PPTP: ", PPTP[1])
        print("L2TP: ", L2TP[1])
        print("OVPN: ", OVPN_SERVER_STATUS_result[0])
        print("SSTP: ", SSTP[1])
        print("Web Proxy: ", Web_Proxy[1])
        print(SCRIPT_result)
        print("==================================")

        # add data into output array
        data = [ip, id[1], socks[1], DNS[1], PPTP[1], L2TP[1], OVPN_SERVER_STATUS_result[0], SSTP[1], Web_Proxy[1],
                SCRIPT_result]
        output.append(data)

    except:
        print("[-] Error!!! (",MT['host'],")")

#file write
with open('output.csv', 'w', newline='') as file:
    outputFile = csv.writer(file)
    field = ["IP", "NAME", "SOCKS", "DNS", "PPTP SERVER STATUS", "L2TP SERVER STATUS", "OVPN SERVER STATUS", "SSTP SERVER STATUS", "Web Proxy", "Script"]
    outputFile.writerow(field)
    for e in output:
        outputFile.writerow(e)

# file close
f.close()
