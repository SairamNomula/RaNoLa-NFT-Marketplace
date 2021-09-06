
import smartpy as sp

NULL_ADDRESS = sp.address("tz1YtuZ4vhzzn7ssCt93Put8U9UJDdvCXci4")
NULL_BYTES = sp.bytes('0x')

class FA2ErrorMessage:
    """Static enum used for the FA2 related errors, using the `FA2_` prefix"""
    PREFIX = "FA2_"
    TOKEN_UNDEFINED = "{}TOKEN_UNDEFINED".format(PREFIX)
    """This error is thrown if the token id used in to defined"""
    INSUFFICIENT_BALANCE = "{}INSUFFICIENT_BALANCE".format(PREFIX)
    """This error is thrown if the source address transfers an amount that exceeds its balance"""
    NOT_OWNER = "{}_NOT_OWNER".format(PREFIX)
    """This error is thrown if not the owner is performing an action that he/she shouldn't"""
    NOT_OPERATOR = "{}_NOT_OPERATOR".format(PREFIX)
    """This error is thrown if neither token owner nor permitted operators are trying to transfer an amount"""

class TokenMetadata:
    """Token metadata object as per FA2 standard"""
    def get_type():
        """Returns a single token metadata type, layouted"""
        return sp.TRecord(token_id = sp.TNat, token_metadata = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_metadata"))
    def get_batch_type():
        """Returns a list type containing token metadata types"""
        return sp.TList(TokenMetadata.get_type())
        
class Transfer:
    """Transfer object as per FA2 standard"""
    def get_type():
        """Returns a single transfer type, layouted"""
        tx_type = sp.TRecord(to_ = sp.TAddress,
                             token_id = sp.TNat,
                             amount = sp.TNat).layout(
                ("to_", ("token_id", "amount"))
            )
        transfer_type = sp.TRecord(from_ = sp.TAddress,
                                   txs = sp.TList(tx_type)).layout(
                                       ("from_", "txs"))
        return transfer_type
    
    def get_batch_type():
        """Returns a list type containing transfer types"""
        return sp.TList(Transfer.get_type())
    
    def item(from_, txs):
        """Creates a typed transfer item"""
        return sp.set_type_expr(sp.record(from_ = from_, txs = txs), Transfer.get_type())

class UpdateOperator():
    """Update operators object as per FA2 standard"""
    def get_operator_param_type():
        """Parameters included in the update operator request"""
        return sp.TRecord(
            owner = sp.TAddress,
            operator = sp.TAddress,
            token_id = sp.TNat
            ).layout(("owner", ("operator", "token_id")))
    
    def get_type():
        """Returns a single update operator type, layouted"""
        return sp.TVariant(
                    add_operator = UpdateOperator.get_operator_param_type(),
                    remove_operator = UpdateOperator.get_operator_param_type())

    def get_batch_type():
        """Returns a list type containing update operator types"""
        return sp.TList(UpdateOperator.get_type())

class BalanceOf:
    """Balance of object as per FA2 standard"""
    def get_response_type():
        """Returns the balance_of reponse type, layouted"""
        return sp.TList(
            sp.TRecord(
                request = LedgerKey.get_type(),
                balance = sp.TNat).layout(("request", "balance")))
    def get_type():
        """Returns the balance_of type, layouted"""
        return sp.TRecord(
            requests = sp.TList(LedgerKey.get_type()),
            callback = sp.TContract(BalanceOf.get_response_type())
        ).layout(("requests", "callback"))

class LedgerKey:
    """Ledger key used when looking up balances"""
    def get_type():
        """Returns a single ledger key type, layouted"""
        return sp.TRecord(owner = sp.TAddress, token_id = sp.TNat).layout(("owner", "token_id"))
        
    def make(owner, token_id):
        """Creates a typed ledger key"""
        return sp.set_type_expr(sp.record(owner = owner, token_id = token_id), LedgerKey.get_type())

class OperatorKey:
    """Operator key used when looking up operation permissions"""
    def get_type():
        """Returns a single operator key type, layouted"""
        return sp.TRecord(owner = sp.TAddress, operator = sp.TAddress, token_id = sp.TNat).layout(("owner", ("operator", "token_id")))
        
    def make(owner, operator, token_id):
        """Creates a typed operator key"""
        return sp.set_type_expr(sp.record(owner = owner, operator = operator, token_id = token_id), OperatorKey.get_type())


class BaseFA2(sp.Contract):
    """Base FA2 contract, which implements the required entry points"""
    def get_init_storage(self):
        """Returns the initial storage of the contract"""
        return dict(
            ledger = sp.big_map(tkey=LedgerKey.get_type(), tvalue=sp.TNat),
            token_metadata = sp.big_map(tkey=sp.TNat, tvalue = TokenMetadata.get_type()),
            total_supply = sp.big_map(tkey=sp.TNat, tvalue = sp.TNat),
            operators = sp.big_map(tkey=OperatorKey.get_type(), tvalue = sp.TBool)
        )
    
    def __init__(self):
        """Has no constructor parameters, initialises the storage"""
        self.init(**self.get_init_storage())

    @sp.entry_point
    def transfer(self, transfers):
        """As per FA2 standard, allows a token owner or operator to transfer tokens"""
        sp.set_type(transfers, Transfer.get_batch_type())
        sp.for transfer in transfers:
            sp.for tx in transfer.txs:
                from_user = LedgerKey.make(transfer.from_, tx.token_id)
                to_user = LedgerKey.make(tx.to_, tx.token_id)
                operator_key = OperatorKey.make(transfer.from_, sp.sender, tx.token_id)

                sp.verify(self.data.ledger.get(from_user,sp.nat(0)) >= tx.amount, message = FA2ErrorMessage.INSUFFICIENT_BALANCE)                                     
                sp.verify((sp.sender == transfer.from_) | self.data.operators.get(operator_key, False), message=FA2ErrorMessage.NOT_OWNER)
                
                self.data.ledger[from_user] = sp.as_nat(self.data.ledger[from_user] - tx.amount)
                self.data.ledger[to_user] = self.data.ledger.get(to_user, 0) + tx.amount
                
                sp.if sp.sender != transfer.from_:
                    del self.data.operators[operator_key]
                    
                sp.if self.data.ledger.get(from_user,sp.nat(0)) == sp.nat(0):
                    del self.data.ledger[from_user]

    @sp.entry_point
    def update_operators(self, update_operators):
        """As per FA2 standard, allows a token owner to set an operator who will be allowed to perform transfers on her/his behalf"""
        sp.set_type(update_operators,UpdateOperator.get_batch_type())
        sp.for update_operator in update_operators:
            with update_operator.match_cases() as argument:
                with argument.match("add_operator") as update:
                    sp.verify(update.owner == sp.sender, message=FA2ErrorMessage.NOT_OWNER)
                    operator_key = OperatorKey.make(update.owner, update.operator, update.token_id)
                    self.data.operators[operator_key] = True
                with argument.match("remove_operator") as update:
                    sp.verify(update.owner == sp.sender, message=FA2ErrorMessage.NOT_OWNER)
                    operator_key = OperatorKey.make(update.owner, update.operator, update.token_id)
                    del self.data.operators[operator_key]

    @sp.entry_point
    def balance_of(self, balance_of_request):
        """As per FA2 standard, takes balance_of requests and reponds on the provided callback contract"""
        sp.set_type(balance_of_request, BalanceOf.get_type())
        
        responses = sp.local("responses", sp.set_type_expr(sp.list([]),BalanceOf.get_response_type()))
        sp.for request in balance_of_request.requests:
            sp.verify(self.data.token_metadata.contains(request.token_id), message = FA2ErrorMessage.TOKEN_UNDEFINED)
            responses.value.push(sp.record(request = request, balance = self.data.ledger.get(LedgerKey.make(request.owner, request.token_id),0)))
            
        sp.transfer(responses.value, sp.mutez(0), balance_of_request.callback)


class AdministratorState:
    """Static enum used for the admin rights and propose flow"""    
    IS_ADMIN = sp.nat(1)
    """This state shows that the admin right is there"""
    IS_PROPOSED_ADMIN = sp.nat(2)
    """This state shows that the admin has been proposed but not full admin yet"""

class AdministrableErrorMessage:
    """Static enum used for the FA2 related errors, using the `FA2_` prefix"""
    PREFIX = "ADM_"
    NOT_ADMIN = "{}NOT_ADMIN".format(PREFIX)

class AdministrableFA2(BaseFA2):
    """FA2 Contract with administrators per token""" 
    def get_init_storage(self):
        """Returns the initial storage of the contract"""
        storage = super().get_init_storage()
        storage['administrator_allowmap'] = sp.set_type_expr(self.administrator_allowmap, sp.TMap(sp.TAddress, sp.TBool))
        storage['administrators'] = sp.big_map(tkey=LedgerKey.get_type(), tvalue = sp.TNat)
        return storage
        
    def __init__(self, administrator_allowmap={}):
        """With the allowmap you can control who can become administrator. If this map is empty then there are no limitations"""
        self.administrator_allowmap = administrator_allowmap
        super().__init__()
    
    @sp.entry_point
    def set_token_metadata(self, token_metadata_list):
        """The definition of a new token requires its metadata to be set. Only the administrators of a certain token can edit existing. 
        If no token metadata is set for a given ID the sender will become admin of that token automatically"""
        sp.set_type(token_metadata_list, TokenMetadata.get_batch_type())
        sp.for token_metadata in token_metadata_list:
            administrator_ledger_key = LedgerKey.make(sp.sender, token_metadata.token_id)
            sp.if self.data.token_metadata.contains(token_metadata.token_id):
                sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            sp.else:
                sp.if sp.len(self.data.administrator_allowmap)>0:    
                    sp.verify(self.data.administrator_allowmap.get(sp.sender, False), message = AdministrableErrorMessage.NOT_ADMIN)
                self.data.administrators[administrator_ledger_key] = AdministratorState.IS_ADMIN    
            self.data.token_metadata[token_metadata.token_id] = token_metadata
    
    @sp.entry_point
    def propose_administrator(self, proposed_administrator_ledger_key):
        """This kicks off the adding of a new administrator for a specific token. First you propose and then the proposed admin 
        can set him/herself with the set_administrator endpoint"""
        sp.set_type(proposed_administrator_ledger_key, LedgerKey.get_type())

        administrator_ledger_key = LedgerKey.make(sp.sender, proposed_administrator_ledger_key.token_id)

        sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
        self.data.administrators[proposed_administrator_ledger_key] = AdministratorState.IS_PROPOSED_ADMIN

    @sp.entry_point
    def set_administrator(self, token_id):
        """Only a proposed admin can call this entrypoint. If the sender is correct the new admin is set"""
        sp.set_type(token_id, sp.TNat)

        administrator_ledger_key = LedgerKey.make(sp.sender, token_id)

        sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_PROPOSED_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
        self.data.administrators[administrator_ledger_key] = AdministratorState.IS_ADMIN
    
    @sp.entry_point
    def remove_administrator(self, administrator_to_remove_ledger_key):
        """This removes a administrator entry entirely from the map"""
        sp.set_type(administrator_to_remove_ledger_key, LedgerKey.get_type())
        
        administrator_ledger_key = LedgerKey.make(sp.sender, administrator_to_remove_ledger_key.token_id)

        sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
        del self.data.administrators[administrator_to_remove_ledger_key]
    
class TokenAmount:
    def get_type():
        return sp.TRecord(token_id = sp.TNat, amount = sp.TNat).layout(("token_id", "amount"))
    def get_batch_type():
        return sp.TList(TokenAmount.get_type())

class RedeemAddress:
    def get_type():
        return sp.TRecord(token_id = sp.TNat, address = sp.TAddress).layout(("token_id", "address"))
    def get_request_type():
        return sp.TRecord(token_ids = sp.TList(sp.TNat), callback = sp.TContract(RedeemAddress.get_batch_type())).layout(("token_ids", "callback"))
    def get_batch_type():
        return sp.TList(RedeemAddress.get_type())

class TokenId:
    def get_type():
        return sp.TNat
    def get_batch_type():
        return sp.TList(TokenId.get_type())
        
class TokenContext:
    def get_type():
        return sp.TRecord(total_minted=sp.TNat, total_burned=sp.TNat, redeem_address=sp.TAddress, is_paused=sp.TBool).layout(("total_minted", ("total_burned", ("redeem_address", "is_paused"))))
    def get_batch_type():
        return sp.TList(TokenContext.get_type())
   

class TZWFA2ErrorMessage:
    """Static enum used for the FA2 related errors, using the `FA2_` prefix"""
    PREFIX = "TZW_"
    TOKEN_PAUSED = "{}TOKEN_PAUSED".format(PREFIX)
    TOKEN_EXISTS = "{}TOKEN_EXISTS".format(PREFIX)
    SAME_REASSIGN = "{}SAME_REASSIGN".format(PREFIX)
    CANNOT_TRANSFER = "{}CANNOT_TRANSFER".format(PREFIX)
        
class TzWrappedFA2(AdministrableFA2):
    """FA2 Contract for TzWrappedFA2 tokens""" 
    def get_init_storage(self):
        """Returns the initial storage of the contract"""
        storage = super().get_init_storage()
        storage['token_context'] = sp.big_map(tkey=sp.TNat, tvalue=TokenContext.get_type())
        return storage
        
    def __init__(self, administrator_allowmap={}):
        super().__init__(administrator_allowmap)
        
    # Owner Entrypoints 
    # --- START ---
    @sp.entry_point
    def initialise_token(self, token_ids):
        """Initialise the token with the required additional token context, can only be called once per token and only one of its admin can call this"""
        sp.set_type_expr(token_ids, sp.TList(sp.TNat))

        sp.for token_id in token_ids:
            sp.verify((~self.data.token_context.contains(token_id)), message = TZWFA2ErrorMessage.TOKEN_EXISTS)            
            administrator_ledger_key = LedgerKey.make(sp.sender, token_id)
            sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            self.data.token_context[token_id] = sp.record(total_minted=0, total_burned=0, redeem_address=NULL_ADDRESS, is_paused=False)

    @sp.entry_point
    def mint(self, token_amounts):
        """Allows to issue new tokens to the calling admin's address, only a token administrator can do this"""
        sp.set_type(token_amounts, TokenAmount.get_batch_type())
        sp.for token_amount in token_amounts:
            administrator_ledger_key = LedgerKey.make(sp.sender, token_amount.token_id)
            sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            sp.verify(self.data.token_metadata.contains(token_amount.token_id), message = FA2ErrorMessage.TOKEN_UNDEFINED)
            self.data.ledger[administrator_ledger_key] = self.data.ledger.get(administrator_ledger_key, 0) + token_amount.amount
            self.data.total_supply[token_amount.token_id] = self.data.total_supply.get(token_amount.token_id, 0) + token_amount.amount
            
            token_context = self.data.token_context[token_amount.token_id]
            token_context.total_minted += token_amount.amount
            self.data.token_context[token_amount.token_id] = token_context
    
    @sp.entry_point
    def burn(self, token_amounts):
        """Allows to burn tokens on the calling admin's address, only a token administrator can do this"""
        sp.set_type(token_amounts, TokenAmount.get_batch_type())
        sp.for token_amount in token_amounts:
            token_context = self.data.token_context[token_amount.token_id]
            administrator_ledger_key = LedgerKey.make(sp.sender, token_amount.token_id)
            redeem_address_ledger_key = LedgerKey.make(token_context.redeem_address, token_amount.token_id)
            sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            sp.verify(self.data.ledger[redeem_address_ledger_key]>=token_amount.amount, message = FA2ErrorMessage.INSUFFICIENT_BALANCE)
            self.data.ledger[redeem_address_ledger_key] = sp.as_nat(self.data.ledger.get(redeem_address_ledger_key, 0) - token_amount.amount)
            self.data.total_supply[token_amount.token_id] = sp.as_nat(self.data.total_supply.get(token_amount.token_id, 0) - token_amount.amount)
            
            token_context.total_burned += token_amount.amount
            self.data.token_context[token_amount.token_id] = token_context
            
            sp.if self.data.ledger[administrator_ledger_key] == 0:
                del self.data.ledger[administrator_ledger_key]
                
    @sp.entry_point
    def pause(self, token_ids):
        """Allows to pause tokens, only a token administrator can do this"""
        sp.set_type(token_ids, sp.TList(sp.TNat))
        sp.for token_id in token_ids:
            administrator_ledger_key = LedgerKey.make(sp.sender, token_id)
            sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            token_context = self.data.token_context[token_id]
            token_context.is_paused = True
            self.data.token_context[token_id] = token_context
            
    @sp.entry_point
    def unpause(self, token_ids):
        """Allows to unpause tokens, only a token administrator can do this"""
        sp.set_type(token_ids, sp.TList(sp.TNat))
        sp.for token_id in token_ids:
            administrator_ledger_key = LedgerKey.make(sp.sender, token_id)
            sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            token_context = self.data.token_context[token_id]
            token_context.is_paused = False
            self.data.token_context[token_id] = token_context
                
    @sp.entry_point
    def set_redeem_addresses(self, redeem_addresses):
        """Allows to specify the burn adress for a  contract for a specific token, only a token administrator can do this"""
        sp.set_type(redeem_addresses, RedeemAddress.get_batch_type())
        sp.for redeem_address in redeem_addresses:
            administrator_ledger_key = LedgerKey.make(sp.sender, redeem_address.token_id)
            sp.verify(self.data.administrators.get(administrator_ledger_key, sp.nat(0))==AdministratorState.IS_ADMIN, message = AdministrableErrorMessage.NOT_ADMIN)
            self.data.token_context[redeem_address.token_id].redeem_address = redeem_address.address
    # Owner entrypoints
    # --- END ---
    
    # Open Entrypoints
    @sp.entry_point
    def transfer(self, transfers):
        """Sligthly adapted FA2 transfer method which includes pause functionality"""
        sp.set_type(transfers, Transfer.get_batch_type())
        sp.for transfer in  transfers:
           sp.for tx in transfer.txs:
                token_context = self.data.token_context[tx.token_id]
                sp.verify((transfer.from_ == sp.sender), message = FA2ErrorMessage.NOT_OWNER)
                sp.verify(self.data.token_metadata.contains(tx.token_id), message = FA2ErrorMessage.TOKEN_UNDEFINED)
                sp.verify(~token_context.is_paused, message = TZWFA2ErrorMessage.TOKEN_PAUSED)
                sp.if (tx.amount > sp.nat(0)):
                    from_user = LedgerKey.make(transfer.from_, tx.token_id)
                    to_user = LedgerKey.make(tx.to_, tx.token_id)
                    sp.verify((self.data.ledger[from_user] >= tx.amount), message = FA2ErrorMessage.INSUFFICIENT_BALANCE)
                    self.data.ledger[from_user] = sp.as_nat(self.data.ledger[from_user] - tx.amount)
                    self.data.ledger[to_user] = self.data.ledger.get(to_user, 0) + tx.amount

                    sp.if self.data.ledger[from_user] == 0:
                        del self.data.ledger[from_user]
    
    # Read only endpoints
    @sp.entry_point
    def get_redeem_addresses(self, get_redeem_address_request):
        """As per FA2 standard, takes balance_of requests and reponds on the provided callback contract"""
        sp.set_type(get_redeem_address_request, RedeemAddress.get_request_type())
        
        responses = sp.local("responses", sp.set_type_expr(sp.list([]),RedeemAddress.get_batch_type()))
        sp.for token_id in get_redeem_address_request.token_ids:
            sp.verify(self.data.token_metadata.contains(token_id), message = FA2ErrorMessage.TOKEN_UNDEFINED)
            responses.value.push(sp.record(token_id = token_id, address = self.data.token_context[token_id].redeem_address))
            
        sp.transfer(responses.value, sp.mutez(0), get_redeem_address_request.callback)


@sp.add_test(name="TzWrappedFA2 Blueprint")
def test():
    scenario = sp.test_scenario()
    scenario.h1("TzWrappedFA2 - A blueprint TzWrappedFA2 implementation")
    scenario.table_of_contents()

    administrator = sp.test_account("Adiministrator")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")
    dan = sp.test_account("Dan")


    scenario.h2("Accounts")
    scenario.show([administrator, alice, bob, dan])
    tzwrapped_fa2_contract = TzWrappedFA2({administrator.address:True})
    scenario += tzwrapped_fa2_contract
    
    scenario.h2("Admin Calls")
    scenario.h3("Initialise 3 tokens")
    token_metadata_list = [sp.record(token_id=sp.nat(0), token_metadata=sp.map()),sp.record(token_id=sp.nat(1), token_metadata=sp.map()),sp.record(token_id=sp.nat(2), token_metadata=sp.map())]
    scenario += tzwrapped_fa2_contract.set_token_metadata(token_metadata_list).run(sender=administrator)
    scenario += tzwrapped_fa2_contract.initialise_token([sp.nat(0),sp.nat(1),sp.nat(2)]).run(sender=administrator)
    
    
    scenario.h2("Owner Only Calls")
    scenario.h3("Transferring the Ownership to the individual owners")
    ownerships = [sp.record(token_id=sp.nat(0), owner=alice.address),sp.record(token_id=sp.nat(1), proposed_administrator=bob.address),sp.record(token_id=sp.nat(2), owner=dan.address)]
    
    scenario.p("Not admin trying to propose new owner")
    scenario += tzwrapped_fa2_contract.propose_administrator(LedgerKey.make(alice.address, sp.nat(0))).run(sender=alice, valid=False)
    
    scenario.p("Not admin trying to transfer directly")
    scenario += tzwrapped_fa2_contract.set_administrator(sp.nat(0)).run(sender=bob, valid=False)
    
    scenario.p("Correct admin trying to transfer directly")
    scenario += tzwrapped_fa2_contract.set_administrator(sp.nat(0)).run(sender=administrator, valid=False)
    
    scenario.p("Correct admin trying to propose transfer")
    scenario += tzwrapped_fa2_contract.propose_administrator(LedgerKey.make(alice.address, sp.nat(0))).run(sender=administrator, valid=True)
    scenario += tzwrapped_fa2_contract.propose_administrator(LedgerKey.make(bob.address, sp.nat(1))).run(sender=administrator, valid=True)
    scenario += tzwrapped_fa2_contract.propose_administrator(LedgerKey.make(dan.address, sp.nat(2))).run(sender=administrator, valid=True)
    
    scenario.p("Correct admin (but not proposed) trying to transfer")
    scenario += tzwrapped_fa2_contract.set_administrator(sp.nat(0)).run(sender=administrator, valid=False)    
    
    scenario.p("Proposed admin trying to transfer")
    scenario += tzwrapped_fa2_contract.set_administrator(sp.nat(0)).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.set_administrator(sp.nat(1)).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.set_administrator(sp.nat(2)).run(sender=dan, valid=True)
    
    scenario.p("Non Admin deletes rights")
    scenario += tzwrapped_fa2_contract.remove_administrator(LedgerKey.make(administrator.address, sp.nat(0))).run(sender=dan, valid=False)
    scenario += tzwrapped_fa2_contract.remove_administrator(LedgerKey.make(administrator.address, sp.nat(1))).run(sender=alice, valid=False)
    scenario += tzwrapped_fa2_contract.remove_administrator(LedgerKey.make(administrator.address, sp.nat(2))).run(sender=bob, valid=False)
    
    scenario.p("Admin deletes own rights")
    scenario += tzwrapped_fa2_contract.remove_administrator(LedgerKey.make(administrator.address, sp.nat(0))).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.remove_administrator(LedgerKey.make(administrator.address, sp.nat(1))).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.remove_administrator(LedgerKey.make(administrator.address, sp.nat(2))).run(sender=dan, valid=True)
   
    scenario.h3("Issuing")
    scenario.p("Correct admin but not owner trying to issue")
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(0), amount=sp.nat(100))]).run(sender=administrator, valid=False)
    
    scenario.p("Incorrect owner trying to issue (Alice is owner of 0 not 1)")
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=alice, valid=False)
    
    scenario.p("Correct owner trying to batch issue (Alice is owner of 0 not 1 and 2)")
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(0), amount=sp.nat(100)), sp.record(token_id=sp.nat(1), amount=sp.nat(100)), sp.record(token_id=sp.nat(2), amount=sp.nat(100))]).run(sender=alice, valid=False)
    
    scenario.p("Correct owners issuing tokens")
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(0), amount=sp.nat(100))]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(2), amount=sp.nat(100))]).run(sender=dan, valid=True)
    
    scenario.p("Correct owners issuing additional amounts of tokens")
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(0), amount=sp.nat(101))]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(1), amount=sp.nat(101))]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(2), amount=sp.nat(101))]).run(sender=dan, valid=True)
    scenario.verify(tzwrapped_fa2_contract.data.ledger[LedgerKey.make(alice.address, 0)] == 201)
    scenario.verify(tzwrapped_fa2_contract.data.ledger[LedgerKey.make(bob.address, 1)] == 201)
    scenario.verify(tzwrapped_fa2_contract.data.ledger[LedgerKey.make(dan.address, 2)] == 201)
    
    
    scenario.h3("Setting Redeem Address")
    scenario.p("Correct admin but not owner trying to set redeem address")
    scenario += tzwrapped_fa2_contract.set_redeem_addresses([sp.record(token_id=sp.nat(0), address=alice.address)]).run(sender=administrator, valid=False)
    
    scenario.p("Correct owners setting redeem addresses")
    scenario += tzwrapped_fa2_contract.set_redeem_addresses([sp.record(token_id=sp.nat(0), address=alice.address)]).run(sender=alice)
    scenario += tzwrapped_fa2_contract.set_redeem_addresses([sp.record(token_id=sp.nat(1), address=bob.address)]).run(sender=bob)
    scenario += tzwrapped_fa2_contract.set_redeem_addresses([sp.record(token_id=sp.nat(2), address=dan.address)]).run(sender=dan)
    
    scenario.p("Incorrect owner trying to burn (Alice is owner of 0 not 1)")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=alice, valid=False)
    
    scenario.p("Correct owner trying to batch burn (Alice is owner of 0 not 1 and 2)")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(0), amount=sp.nat(100)), sp.record(token_id=sp.nat(1), amount=sp.nat(100)), sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=alice, valid=False)
    
    scenario.h3("Redemption")
    scenario.p("Correct admin but not owner trying to burn")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(0), amount=sp.nat(100))]).run(sender=administrator, valid=False)
    
    scenario.p("Incorrect owner trying to burn (Alice is owner of 0 not 1)")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=alice, valid=False)
    
    scenario.p("Correct owner trying to batch burn (Alice is owner of 0 not 1 and 2)")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(0), amount=sp.nat(100)), sp.record(token_id=sp.nat(1), amount=sp.nat(100)), sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=alice, valid=False)
    
    scenario.p("Correct owners burning tokens")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(0), amount=sp.nat(100))]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(1), amount=sp.nat(100))]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(2), amount=sp.nat(100))]).run(sender=dan, valid=True)
    scenario.verify(tzwrapped_fa2_contract.data.ledger[LedgerKey.make(alice.address, 0)] == 101)
    scenario.verify(tzwrapped_fa2_contract.data.ledger[LedgerKey.make(bob.address, 1)] == 101)
    scenario.verify(tzwrapped_fa2_contract.data.ledger[LedgerKey.make(dan.address, 2)] == 101)
    
    scenario.p("Cannot burn more than owner has")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(0), amount=sp.nat(201))]).run(sender=alice, valid=False)
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(1), amount=sp.nat(201))]).run(sender=bob, valid=False)
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(2), amount=sp.nat(201))]).run(sender=dan, valid=False)
    
    scenario.p("Correct owners burning additional amounts of tokens")
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(0), amount=sp.nat(101))]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(1), amount=sp.nat(101))]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.burn([sp.record(token_id=sp.nat(2), amount=sp.nat(101))]).run(sender=dan, valid=True)
    scenario.verify(~tzwrapped_fa2_contract.data.ledger.contains(LedgerKey.make(alice.address, 0)))
    scenario.verify(~tzwrapped_fa2_contract.data.ledger.contains(LedgerKey.make(bob.address, 1)))
    scenario.verify(~tzwrapped_fa2_contract.data.ledger.contains(LedgerKey.make(dan.address, 2)))
    
    scenario.h3("Reassign")
    scenario.p("Bootstrapping by issuing some tokens")
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(0), amount=sp.nat(50))]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(1), amount=sp.nat(47))]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.mint([sp.record(token_id=sp.nat(2), amount=sp.nat(39))]).run(sender=dan, valid=True)
    
    scenario.h3("Pause")
    scenario.p("Correct admin but not owner trying to pause")
    scenario += tzwrapped_fa2_contract.pause([sp.nat(0)]).run(sender=administrator, valid=False)
    
    scenario.p("Incorrect owner trying to pause (Alice is owner of 0 not 1)")
    scenario += tzwrapped_fa2_contract.pause([sp.nat(1)]).run(sender=alice, valid=False)
    
    scenario.p("Correct owner trying to batch pause (Alice is owner of 0 not 1 and 2)")
    scenario += tzwrapped_fa2_contract.pause([sp.nat(0), sp.nat(1), sp.nat(2)]).run(sender=alice, valid=False)
    
    scenario.p("Correct owners pauseing tokens")
    scenario += tzwrapped_fa2_contract.pause([sp.nat(1)]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.pause([sp.nat(2)]).run(sender=dan, valid=True)
    
    
    scenario.h3("Unpause")
    scenario.p("Correct admin but not owner trying to unpause")
    scenario += tzwrapped_fa2_contract.unpause([sp.nat(0)]).run(sender=administrator, valid=False)
    
    scenario.p("Incorrect owner trying to unpause (Alice is owner of 0 not 1)")
    scenario += tzwrapped_fa2_contract.unpause([sp.nat(1)]).run(sender=alice, valid=False)
    
    scenario.p("Correct owner trying to batch unpause (Alice is owner of 0 not 1 and 2)")
    scenario += tzwrapped_fa2_contract.unpause([sp.nat(0), sp.nat(1), sp.nat(2)]).run(sender=alice, valid=False)
    
    scenario.p("Correct owners unpauseing tokens")
    scenario += tzwrapped_fa2_contract.unpause([sp.nat(1)]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.unpause([sp.nat(2)]).run(sender=dan, valid=True)
    
    scenario.h2("Token Holder Calls")
    scenario.h3("Transfer")
    scenario.p("Holder with no balance tries transfer")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=bob.address, txs=[sp.record(to_=dan.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=bob, valid=False)
    
    scenario.p("Admin with no balance tries transfer")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=administrator.address, txs=[sp.record(to_=dan.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=administrator, valid=False)
    
    scenario.p("Admin tries transfer of third parties balance")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=alice.address, txs=[sp.record(to_=dan.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=administrator, valid=False)
    
    scenario.p("Owner performs initial transfer of own balance")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=alice.address, txs=[sp.record(to_=dan.address, token_id=sp.nat(0), amount=sp.nat(10))])]).run(sender=alice, valid=True)
    
    scenario.p("Owner tries transfer of third party balance")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=dan.address, txs=[sp.record(to_=bob.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=alice, valid=False)
    
    scenario.p("Holder transfers own balance")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=dan.address, txs=[sp.record(to_=bob.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=dan, valid=True)
    
    scenario.p("Holder transfers too much")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=dan.address, txs=[sp.record(to_=bob.address, token_id=sp.nat(0), amount=sp.nat(11))])]).run(sender=dan, valid=False)
    
    scenario.h3("Pause/Unpause")
    scenario.p("Holder transfers too much")
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=dan.address, txs=[sp.record(to_=bob.address, token_id=sp.nat(0), amount=sp.nat(11))])]).run(sender=dan, valid=False)
    
    scenario.p("Holder transfers paused token")
    scenario += tzwrapped_fa2_contract.pause([sp.nat(0)]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.pause([sp.nat(1)]).run(sender=bob, valid=True)
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=dan.address, txs=[sp.record(to_=bob.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=dan, valid=False)
    
    scenario.p("Holder transfers resumed token")
    scenario += tzwrapped_fa2_contract.unpause([sp.nat(0)]).run(sender=alice, valid=True)
    scenario += tzwrapped_fa2_contract.transfer([sp.record(from_=dan.address, txs=[sp.record(to_=bob.address, token_id=sp.nat(0), amount=sp.nat(1))])]).run(sender=dan, valid=True)
    
