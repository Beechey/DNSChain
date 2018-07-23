from flask import Flask, jsonify, abort, request
import json, random, string
from uuid import uuid4

class DNS(object):
    def __init__(self):
        self.data = {
            "malicious.com": "1.1.1.1"
        }

    def generate_data(self):
        """
        This generates a random URL and IP pair to add into the DNS and Blockchain
        :param url: <string> Randomly generated string to act as a dummy URL
        :param ip: <string> Randomly generated string to act as a dummy IP address

        :return: <int>, <int> Both the variables of the URL and IP
        """
        url = ''.join([random.choice(string.ascii_lowercase + string.digits)
                for _ in xrange(16)]) + ".com"

        # create an IP
        ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))

        return url, ip

    def store(self, url, ip):
        """
        This stores a URL and IP pair in a dictionary to act as the 'cache' for the DNS
        :param url: <string> URL dummy variable
        :param ip: <string> IP dummy variable
        :return: <dict> A JSON format of the full dictionary
        """
        dns_data = {
            url: ip
        }

        self.data.update(dns_data)

        return jsonify(self.data)

    def get_stored_data(self):
        """
        This simply returns a JSON format of the full dictionary of the DNS
        :return: <dict> The full dictionary of the DNS in JSON format
        """
        return jsonify(self.data)

    def check_for_url(self, check_url):  
        """
        This runs through the DNS to check for a dictionary entry with the key that matches the
        URL passed through
        :param check_url: <string> URL passed through to check through the dictionary
        :return: <string> Returns the corresponding IP address
        :return: <string> If the URL does not exist in the dictionary, then return "False"
        """      
        if check_url in self.data:
            return self.data[check_url]
        else:
            return "False"

    def overwrite_ip(self, url, ip):
        """
        Overwrites the 'value' of a dictionary entry of a specific key using parameters given
        :param url: <string> URL whose IP address will be overwritten
        :param ip: <string> The IP value to overwrite the current value
        :return: None
        """
        if url in self.data:
            self.data[url] = ip

    def remove_entry(self, url):
        """
        This removes an entry from the DNS dictionary using the URL passed through to identify it
        :return: None
        """
        del self.data[url]