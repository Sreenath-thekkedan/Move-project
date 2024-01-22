import datetime

class Aptos:
    def __init__(self):
        self.events = []
        self.users = []
        self.tickets_for_sale = []

    def create_user(self, username):
        user = User(username)
        self.users.append(user)
        return user

    def create_event(self, organizer, initial_price, total_tickets, event_date):
        event = Event(organizer, initial_price, total_tickets, event_date)
        self.events.append(event)
        return event

    def create_ticket(self, event, owner, price):
        ticket = Ticket(event, owner, price)
        self.tickets_for_sale.append(ticket)
        return ticket

    def buy_ticket(self, buyer, max_price=None):
        if max_price is not None:
            available_tickets = [ticket for ticket in self.tickets_for_sale if ticket.price <= max_price]
            if not available_tickets:
                return None
            ticket_to_buy = min(available_tickets, key=lambda x: x.price)
        else:
            if not self.tickets_for_sale:
                return None
            ticket_to_buy = min(self.tickets_for_sale, key=lambda x: x.price)

        buyer_balance = buyer.get_balance()
        if buyer_balance < ticket_to_buy.price:
            return None  # Buyer can't afford the ticket

        commission = 0.01 * ticket_to_buy.price
        seller_earning = ticket_to_buy.price - commission

        buyer.decrease_balance(ticket_to_buy.price)
        ticket_to_buy.owner.increase_balance(seller_earning)
        self.tickets_for_sale.remove(ticket_to_buy)

        return ticket_to_buy


class User:
    def __init__(self, username):
        self.username = username
        self.balance = 0

    def get_balance(self):
        return self.balance

    def increase_balance(self, amount):
        self.balance += amount

    def decrease_balance(self, amount):
        self.balance -= amount


class Organizer(User):
    def __init__(self, username):
        super().__init__(username)


class Event:
    def __init__(self, organizer, initial_price, total_tickets, event_date):
        self.organizer = organizer
        self.initial_price = initial_price
        self.total_tickets = total_tickets
        self.event_date = event_date
        self.tickets_sold = 0

    def create_ticket(self, owner, price):
        if self.tickets_sold >= self.total_tickets:
            return None  # Event is sold out

        ticket = Ticket(self, owner, price)
        self.tickets_sold += 1
        return ticket


class Ticket:
    def __init__(self, event, owner, price):
        self.event = event
        self.owner = owner
        self.price = price


# Example:
aptos = Aptos()

organizer = Organizer("Organizer1")
event = aptos.create_event(organizer, 50, 100, datetime.datetime.now() + datetime.timedelta(days=7))

user1 = aptos.create_user("User1")
user2 = aptos.create_user("User2")

ticket1 = event.create_ticket(user1, 50)
ticket2 = event.create_ticket(user1, 60)
ticket3 = event.create_ticket(user2, 55)

#second-hand buying
bought_ticket = aptos.buy_ticket(user2, max_price=60)
if bought_ticket:
    print(f"{user2.username} bought a ticket for {event.event_date} at {bought_ticket.price}")
else:
    print(f"{user2.username} couldn't buy a ticket.")

#buying the cheapest ticket
cheapest_ticket = aptos.buy_ticket(user1)
if cheapest_ticket:
    print(f"{user1.username} bought the cheapest ticket for {event.event_date} at {cheapest_ticket.price}")
else:
    print(f"{user1.username} couldn't buy a ticket.")
