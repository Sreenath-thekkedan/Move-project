class ObjectCore:
    def __init__(self, owner):
        self.owner = owner
 
class Wallet:
    def __init__(self, amount, owner):
        self.amount = amount
        self.owner = owner
 
class Aptos:
    def __init__(self):
        self.current_round = None
 
class Proposal:
    def __init__(self, name, proposer, upvotes=0):
        self.name = name
        self.proposer = proposer
        self.upvotes = upvotes
        self.proposer_wallet = None
 
MAX_UPVOTES = 5
UPVOTE_PRICE = 10
 
def get_wallet(amount, owner):
    return Wallet(amount, owner)
 
def create_proposal(name, proposer):
    return Proposal(name, proposer)
 
def upvote_proposal(proposal, amount, upvoter_wallet):
    if proposal.proposer == upvoter_wallet.owner:
        print("Error: Cannot upvote own proposal.")
        return
 
    upvotes_needed = MAX_UPVOTES - proposal.upvotes
    upvotes_paid = min(amount // UPVOTE_PRICE, upvotes_needed)
 
    proposal.upvotes += upvotes_paid
    upvoter_wallet.amount -= upvotes_paid * UPVOTE_PRICE
 
def finish_round(aptos, dapp_wallet):
    if aptos.current_round is None:
        print("Error: No ongoing round.")
        return
 
    winning_proposal = max(aptos.current_round, key=lambda x: x.upvotes)
    total_amount = MAX_UPVOTES * UPVOTE_PRICE
 
    for proposal in aptos.current_round:
        if proposal == winning_proposal:
            proposal.proposer_wallet.amount += total_amount
        else:
            proposal.proposer_wallet.amount += total_amount // 2
            dapp_wallet.amount += total_amount // 2
 
    aptos.current_round = None
 
# Example usage:
participant_wallet = get_wallet(100, "Participant")
dapp_wallet = Wallet(0, "Dapp")
aptos = Aptos()
 
proposal1 = create_proposal("Proposal 1", "Participant")
proposal2 = create_proposal("Proposal 2", "second Participant")
 
proposal1.proposer_wallet = participant_wallet
proposal2.proposer_wallet = participant_wallet
 
aptos.current_round = [proposal1, proposal2]
 
upvote_proposal(proposal1, 20, participant_wallet)
upvote_proposal(proposal2, 15, participant_wallet)
 
finish_round(aptos, dapp_wallet)
 
print("Participant's wallet amount:", participant_wallet.amount)
print("Dapp's wallet amount:", dapp_wallet.amount)
