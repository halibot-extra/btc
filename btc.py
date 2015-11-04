from halibot import HalModule
from blockchain import exchangerates

class BtcModule(HalModule):

	def receive(self, msg):
		coarse = msg.body.strip().split(' ')
		args = list(filter( lambda x: len(x) > 0, coarse ))

		if args[0] == '!btc':
			curs = args[1:]
			if len(curs) == 0:
				curs = [ self.config.get('currency', 'USD') ]

			# Simplistic rate limiting, TODO better rate limiting
			limit = self.config.get('limit', -1)
			if limit >= 0 and len(curs) > limit:
				self.reply(msg, body="Currency queries are limited to {}.".format(limit))
				return

			# Actually get a return the values
			ticker = exchangerates.get_ticker()
			hit = {} # for not showing the same currency twice

			for c in curs:
				c = c.upper()
				if not c in hit:
					if c in ticker:
						body = '1 BTC ~ {} {}'.format(ticker[c].p15min, c)
					else:
						body = 'Unknown currency: {}'.format(c)
					hit[c] = True
					self.reply(msg, body=body)


