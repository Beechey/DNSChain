from time import time
import hashlib
import json
from uuid import uuid4
import requests
from flask import Flask, jsonify, request


class Blockchain(object):
	def __init__(self):
		"""
		This is the initial Blockchain setup, it ensures the Blockchain is empty initially, as well as the
		"current_transactions" variable, before creating the "Genesis Block"
		:return: Nothing
		"""
		self.chain = []
		self.current_transactions = {}

		# Create the genesis block (the initial block of the chain)
		self.new_block(previous_hash = 1)

		# Create history by hashing entire Blockchain as a new Block after every new Block

	def new_transaction(self, url, ip):
		"""
		This creates a new transaction that will go into the next block to be hashed and added to the chain
		:param url: <string> URL to be stored
		:param ip: <string> corredponding IP address to be stored
		:return: <int> The index of the block that will hold this transaction
		"""

		self.current_transactions.update({
			'url': url,
			'ip': ip
		})
		
		return self.previous_block['index'] +1

	def new_block(self, previous_hash):
		"""
		This creates a new Block in the Blockchain
        :param previous_hash: <string> A hash of previous Block
        :return: <dict> A new Block
		"""

		block = {
			'index': len(self.chain) +1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'previous_hash': previous_hash
		}

		# Transactions have been added to the block, so can be reset
		self.current_transactions = {}

		# Add this block to the chain
		self.chain.append(block)

		return block

	@property
	def previous_block(self):
		"""
		This returns the Block in Blockchain from the current index (-1), which is the previous Block
		:return: <dict> The Block with the index of current (-1)
		"""
		return self.chain[-1]

	@staticmethod
	def hash_block(block):
		"""
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block to be hashed
		:return: <string> A hexdigest of the block
        """
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	def check_for_url(self, url):
		"""
		This iterates through the Blockchain to find the URL passed in
		:param url: <string> URL the user wants to query
		:return: <string> The IP address that corresponds to the URL previously passed in
		:return: <string> If the URL does not exist in the Blockchain, then the function returns "False"
		"""
		for block in self.chain:
			if block['transactions'].get('url') == url:
				return block['transactions'].get('ip')
		
		return "False"

	def history_block(self, chain_hash):
		"""
		This creates a new history Block in the Blockchain
        :param chain_hash: <string> A hash of the entire chain
        :return: <dict> A new history Block
		"""

		history = {
			'history': chain_hash
		}

		self.chain.append(history)

		return history

	# def get_chain(self):
	# 	return self.chain

	def hash_chain(self):
		"""
        Creates a SHA-256 hash of the entire Blockchain
		:return: <string> A hexdigest of the the entire Blockchain
        """
		chain_string = json.dumps(self.chain, sort_keys=True).encode()
		return hashlib.sha256(chain_string).hexdigest()
