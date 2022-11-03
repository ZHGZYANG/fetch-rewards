from tornado.web import RequestHandler
from tornado.web import MissingArgumentError
import json
from dateutil import parser as dateparser
from settings.models import User

info = {'status': 0, 'meta': {}}
user = User()


class AddTransactionHandler(RequestHandler):
    def post(self):
        try:
            payer = self.get_body_argument('payer')
            points = int(self.get_body_argument('points'))
            timestamp = dateparser.parse(self.get_body_argument('timestamp'))
            try:
                force_add = self.get_body_argument('force')
                force_add = True if force_add == 'true' else False
            except MissingArgumentError:
                force_add = False

            earn_result = user.earn(payer, points, timestamp, force_add)
            if earn_result:
                info['status'] = 0
                info['msg'] = 'Adding transaction successful.'
                info['meta']['count'] = 1
            else:
                info['status'] = 1
                info['msg'] = 'Action denied. Attempted points is negative and will make balance negative.'
                info['meta']['count'] = 0
        except MissingArgumentError:
            info['status'] = 2
            info['msg'] = 'Error. Please fill in all required fields.'
            info['meta']['count'] = 0
        except ValueError:
            info['status'] = 3
            info['msg'] = 'Error. Points inputted is invalid.'
            info['meta']['count'] = 0
        except Exception as e:  # dateutil.parser._parser.ParserError
            info['status'] = 3
            info['msg'] = 'Error. Timestamp inputted is invalid.'
            info['meta']['count'] = 0
        self.write(json.dumps(info))


class SpendHandler(RequestHandler):
    def post(self):
        try:
            points = int(self.get_body_argument('points'))
            if points > 0:
                spend_result = user.spend(points)
                if spend_result is not None:
                    info['status'] = 0
                    info['msg'] = spend_result
                    info['meta']['count'] = len(spend_result)
                else:
                    info['status'] = 1
                    info['msg'] = 'Action denied. Attempted points is greater than current balance.'
                    info['meta']['count'] = 0
            else:
                info['status'] = 3
                info['msg'] = 'Error. Points inputted is invalid.'
                info['meta']['count'] = 0
        except MissingArgumentError:
            info['status'] = 2
            info['msg'] = 'Error. Please fill in all required fields.'
            info['meta']['count'] = 0
        except ValueError:
            info['status'] = 3
            info['msg'] = 'Error. Points inputted is invalid.'
            info['meta']['count'] = 0
        self.write(json.dumps(info))


class AllBalancesHandler(RequestHandler):
    def get(self):
        info['status'] = 0
        info['msg'] = user.get_all_balances()
        info['meta']['count'] = len(info['msg'])
        self.write(json.dumps(info))
