from handlers.main import AddTransactionHandler, SpendHandler, AllBalancesHandler

url = [
    (r'/add', AddTransactionHandler),
    (r'/spend', SpendHandler),
    (r'/all', AllBalancesHandler),
]
