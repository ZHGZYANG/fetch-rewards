from collections import deque


class Payer:
    def __init__(self, name):
        self._name = name
        self._balance = 0
        self._transactions = deque()

    def add_transaction(self, points, timestamp):
        if points > 0:
            self._transactions.append([timestamp, points])
            self._transactions = deque(sorted(self._transactions))
            self._balance += points
        else:
            points = -points
            self._balance -= points
            while points > 0:
                if points < self._transactions[0][1]:  # [timestamp, points]
                    self._transactions[0][1] -= points
                    points -= points
                else:
                    oldest_points = self._transactions.popleft()[1]
                    points -= oldest_points

    def spend(self, points):  # only the first transaction can be spent because this is focus on this payer only
        if points >= self._transactions[0][1]:
            spent = self._transactions.popleft()[1]
            self._balance -= spent
            return spent
        else:
            self._transactions[0][1] -= points
            self._balance -= points
            return points

    def get_oldest_date(self):
        if len(self._transactions) > 0:
            return self._transactions[0][0]  # [timestamp, points]
        return None

    def get_name(self):
        return self._name

    def get_balance(self):
        return self._balance


class User:
    def __init__(self):
        self.balance = 0
        self.records = []  # for reference purpose
        self._payers = []

    def earn(self, payer_name, points, timestamp, force_add):
        for item in self._payers:  # find the payer or add a new one
            if item.get_name() == payer_name:
                payer = item
                break
        else:
            payer = Payer(payer_name)
            self._payers.append(payer)

        # points < 0
        if points + payer.get_balance() < 0:
            if force_add:
                self.balance -= payer.get_balance()
                payer.add_transaction(-payer.get_balance(), timestamp)
                self.records.append(
                    {'activity': 'earn', 'payer_name': payer_name, 'points': points, 'timestamp': timestamp})
                return True
            return False

        # points >= 0
        payer.add_transaction(points, timestamp)
        self.balance += points
        self.records.append(
            {'activity': 'earn', 'payer_name': payer_name, 'points': points, 'timestamp': timestamp})
        return True

    def spend(self, points):
        if points > self.balance:
            return None

        result = []
        self.balance -= points
        self.records.append({'activity': 'spend', 'points': points})

        while points > 0:
            oldest_payer = self._get_oldest_payer()
            spent = oldest_payer.spend(points)
            points -= spent
            result.append({'payer': oldest_payer.get_name(), 'points': -spent})

        return result

    def _get_oldest_payer(self):
        oldest_payer = None
        oldest_time = None
        for payer in self._payers:
            payer_time = payer.get_oldest_date()
            if payer_time is None:
                continue
            if oldest_time is None:
                oldest_time = payer_time
                oldest_payer = payer
                continue

            if oldest_time > payer_time:
                oldest_time = payer_time
                oldest_payer = payer
        return oldest_payer

    def get_all_balances(self):
        result = {}
        for payer in self._payers:
            result[payer.get_name()] = payer.get_balance()
        return result
