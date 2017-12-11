import hashlib
import json


# @staticmethod
def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"


def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    return proof


def hash_block(block):
    block_string = json.dumps(block.previous_hash, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()
