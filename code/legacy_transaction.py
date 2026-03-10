from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user = "bitcoin"
rpc_password = "bitcoin123"

node = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443"
)

wallet_name = "legacywallet"

# create wallet if needed
try:
    node.createwallet(wallet_name)
    print("Wallet created")
except JSONRPCException:
    print("Wallet already exists")

# connect to wallet
rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}"
)

print("\n--- Generating Addresses ---")

A = rpc.getnewaddress("", "legacy")
B = rpc.getnewaddress("", "legacy")
C = rpc.getnewaddress("", "legacy")

print("A:", A)
print("B:", B)
print("C:", C)

print("\n--- Mining coins to A ---")

rpc.generatetoaddress(101, A)

print("Balance:", rpc.getbalance())

print("\n--- Transaction A -> B ---")

txid1 = rpc.sendtoaddress(B, 5)

print("TXID1:", txid1)

rpc.generatetoaddress(1, A)

print("\n--- Decoding Transaction A -> B ---")

tx1 = rpc.gettransaction(txid1)
decoded_tx1 = rpc.decoderawtransaction(tx1["hex"])

print("Decoded TX1:")
print(decoded_tx1)

print("\n--- Finding UTXO for B ---")

utxos = rpc.listunspent()

for u in utxos:
    if u["address"] == B:
        print("UTXO belonging to B: ")
        print(u)

utxo = None
for u in utxos:
    if u["address"] == B:
        utxo = u
        break

if utxo is None:
    print("No UTXO found for B!")
    exit()

print("UTXO:", utxo)

print("\n--- Creating B -> C raw transaction ---")

inputs = [{
    "txid": utxo["txid"],
    "vout": utxo["vout"]
}]

outputs = {
    C: 1,
    B:3.999
    }

raw_tx = rpc.createrawtransaction(inputs, outputs)

print("Raw TX:", raw_tx)

print("\n--- Signing Transaction ---")

signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

signed_hex = signed_tx["hex"]

print("Signed TX:", signed_hex)

print("\n--- Broadcasting Transaction ---")

txid2 = rpc.sendrawtransaction(signed_hex)

print("TXID2:", txid2)

rpc.generatetoaddress(1, A)

print("\n--- Decoding Transaction B -> C ---")

decoded_tx2 = rpc.decoderawtransaction(signed_hex)

print("Decoded TX2:")
print(decoded_tx2)

print("\nProgram finished successfully")