from flask import Flask, jsonify, abort, request
from uuid import uuid4
from blockchain import Blockchain
from dns import DNS
import json
import requests
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

port = raw_input("Please specify the port that this node will run: ")
print("Booting up on \"127.0.0.1:" + port + "\"")

app = Flask(__name__)

ports = []

# Create an instance of the class Blockchain
blockchain = Blockchain()

# create an instance of the class DNS
dns = DNS()

@app.route('/', methods=['GET'])
def home():
	return "<h2><b>DNSChain</b>: Protecting DNS with Blockchain.</h2> \
			<br> \
			<ul> \
				<li>DNS data is automatically generated. That data is then stored in that DNS 'server', and \
					also stored in the Blockchain.</li> \
				<li>When the user requests a URL to be checked, the DNS will check its own records, if the \
					record exists, it will check it matches the Blockchain record, then serve that data to the user</li> \
				<li>If the data does not match for whatever reason, the user is informed, the 'server' data is overwritten \
					using the data from the Blockchain, and that data is served to the user</li> \
			</ul> \
			<br> \
			This system does make the assumption that data on the Blockchain will never need to be altered (for example for \
			dynamic IP changes), and as such, there will be no system in place for this. \
			<br> \
			<hr> \
			<h3>Available URL paths</h3> \
			<ol> \
				<li>127.0.0.1:" + port + "/<b>chain</b> - This lists the entire Blockchain</li> \
                <li>127.0.0.1:" + port + "/ <b> add_entry </b> - This creates a new URL and IP address request to add to the \
                    Blockchain < /li > \
                <li>127.0.0.1:" + port + "/<b>add_dns_entry</b> - This creates a new URL and IP address request to add only to the DNS</li> \
                <li>127.0.0.1:" + port + "/<b>add_corrupted_entry</b> - This creates a new URL, but different IP addresses for the DNS \
                    and Blockchain</li> \
                <li>127.0.0.1:" + port + "/<b>query/url</b> - This performs a check on the Blockchain and local DNS to see whether \
                    the URL given exists</li> \
                <li>127.0.0.1" + port + "/<b>dns_data</b> - This returns the data currently stored in the list on the DNS 'server'</li> \
            </ol>"


@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/add_entry')
def add_entry():
    data = dns.generate_data()

    url = data[0]
    ip = data[1]
    
    previous_block = blockchain.previous_block
    previous_hash = blockchain.hash_block(previous_block)
    blockchain.new_transaction(url, ip)

    blockchain.new_block(previous_hash)

    # blockchain_hash = blockchain.hash_chain()
    # blockchain.history_block(blockchain_hash)

    print('---------------------------------------------------')
    print('New block generated with the following data: ')
    print('URL: ' + url)
    print('IP: ' + ip)
    dns.store(url, ip)
    print('Data stored locally in \'DNS\' server')
    print('---------------------------------------------------')
    
    return "Block generated, click <a href=\"/chain\">here</a> to see the full chain."

@app.route('/add_dns_entry')
def add_dns_entry():
    data = dns.generate_data()
    
    url = data[0]
    ip = data[1]

    dns.store(url, ip)

    print('---------------------------------------------------')
    print('New block generated with the following data: ')
    print('URL: ' + url)
    print('IP: ' + ip)
    print('Data has been stored locally in \'DNS\' server')
    print('---------------------------------------------------')

    return "Data generated, click <a href=\"/dns_data\">here</a> to see the DNS storage."

@app.route('/add_corrupted_entry')
def add_corrupted_entry():
    data1 = dns.generate_data()
    data2 = dns.generate_data()

    url = data1[0]

    dns_ip = data1[1]
    blockchain_ip = data2[1]

    previous_block = blockchain.previous_block
    previous_hash = blockchain.hash_block(previous_block)
    blockchain.new_transaction(url, blockchain_ip)

    blockchain.new_block(previous_hash)

    dns.store(url, dns_ip)

    print('---------------------------------------------------')
    print('New block generated with the following data: ')
    print('URL: ' + url)
    print('IP: ' + blockchain_ip)
    print('---------------------------------------------------')
    print('Data stored locally (DNS) is as follows: ')
    print('URL: ' + url)
    print('IP: ' + dns_ip)
    print('---------------------------------------------------')

    return "Block has been generated, click <a href=\"/chain\">here</a> to see the full chain. \
    <br> \
    Or click <a href=\"/dns_data\">here</a> to see the DNS data"

@app.route('/dns_data')
def dns_data():
    data = dns.get_stored_data()
    return data


@app.route('/query/<url>')
def query_data(url):
    url = url.strip()

    dns_data = dns.check_for_url(url)
    print('---------------------------------------------------')
    print("Checked DNS for URL: " + url)

    blockchain_data = blockchain.check_for_url(url)
    print("Checked Blockchain for URL: " + blockchain_data)
    
    # If the requested URL exists in the DNS server's data
    if dns_data != "False":
        # If it also exists in the Blockchain
        if(blockchain_data != "False"):
            if dns_data == blockchain_data:
                print("The data matches")
                print('---------------------------------------------------')
            else:
                print("Error: the data does not match")
                print('---------------------------------------------------')

                # If it does, get IP from Blockchain
                ip = blockchain_data

                # Store (OVERWRITE) the URL and IP in the DNS
                dns.overwrite_ip(url, ip)

                print("The IP for " + url + " has been overwritten using the Blockchain data")
                print('---------------------------------------------------')

                return "The IP for " + url + " has been overwritten using the Blockchain data"
        
        else:
            print("Error: the URL exists in the DNS but not in the Blockchain")
            dns.remove_entry(url)
            print("The entry for the URL " + url + " has been removed from the DNS")
            print('---------------------------------------------------')

            return "The entry for the URL " + url + " has been removed from the DNS"

        # print("Data retrieved from the Blockchain and stored in the DNS")
        # print('---------------------------------------------------')
        return "The requested URL's IP address is: " + dns_data
    else:
        # If it also does not exist in the Blockchain
        print("Error: this data does not exist in the DNS or Blockchain")
        print('---------------------------------------------------')
        return "Error: this data does not exist in the DNS or Blockchain"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port)
    app.run(debug=True)

