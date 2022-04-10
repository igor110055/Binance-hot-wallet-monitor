import requests
import urllib3
import time
import traceback
import pandas as pd
import datetime
from send_mail import send_mail


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def monitor_binance_hot_wallet(address_lis, timestamp=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')):
    url = "https://graphql.bitquery.io/"
    proxies = {'https': 'http://127.0.0.1:2802', 'http': 'http://127.0.0.1:2802'}    # VPN代理ID
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    while True:
        try:
            query1 = """{
              ethereum(network: bsc) {
                transfers(
                  options: {asc: "block.height", limit: 2000}
                  amount: {gt: 0}
                  currency: {notIn: ["""

            query2 = """]}
                  time: {after: "%s"}
                  sender: {in: [""" % timestamp

            query3 = """]}
                ) {
                  block {
                    timestamp {
                      time(format: "%Y-%m-%d %H:%M:%S")
                    }
                    height
                  }
                  sender {
                    address
                    annotation
                  }
                  receiver {
                    address
                    annotation
                  }
                  currency {
                    address
                    symbol
                  }
                  amount
                  transaction {
                    hash
                  }
                  external
                }
              }
            }"""
            # 将要抓取的列表中的address转化为query可识别的特定格式
            address_string = ""
            for i in range(len(address_lis)):
                if i == len(address_lis) - 1:
                    address_string += '"' + address_lis[i] + '"'
                else:
                    address_string += '"' + address_lis[i] + '"' + ','
            currency_lis = ["0x55d398326f99059ff775485246999027b3197955", "0xe9e7cea3dedca5984780bafc599bd69add087d56"]
            # currency filter for usdt and busd. 将usdt和busd排除，提升抓取效率

            currency_string = ""
            for i in range(len(currency_lis)):
                if i == len(currency_lis) - 1:
                    currency_string += '"' + currency_lis[i] + '"'
                else:
                    currency_string += '"' + currency_lis[i] + '"' + ','
            query = query1+currency_string+query2 + address_string + query3

            # scrap latest 2000 transfers of these binance hot wallets(the transfer's sender is hotwallet)
            req = requests.post(url, json={"query": query}, headers=headers, proxies=proxies, verify=False)
            if req.status_code == 200:
                r = req.json()
                print("200")
                if len(r['data']['ethereum']['transfers']) == 0:  # 无最新transfer记录
                    pass
                else:
                    token_lis = []
                    hash_lis = []
                    for each in r['data']['ethereum']['transfers']:
                        token_lis.append(each['currency']['symbol'].upper())   # token transferred out from hot wallet
                        hash_lis.append(each['transaction']['hash'])   # transaction hash
                    dic = dict(zip(token_lis, hash_lis))

                    timestamp = pd.Timestamp(r['data']['ethereum']['transfers'][-1]['block']['timestamp']['time']).strftime('%Y-%m-%dT%H:%M:%S')
                    # renew timestamp for next scrap
                    print(timestamp)
                    # BIAN_token 是币安现在已经上币了的所有token 和 symbol为NFT
                    BIAN_token = ['BTC', 'LTC', 'ETH', 'NEO', 'BNB', 'QTUM', 'EOS', 'SNT', 'BNT', 'GAS', 'BCC', 'USDT', 'HSR', 'OAX', 'DNT', 'MCO', 'ICN', 'ZRX', 'OMG', 'WTC', 'YOYO', 'LRC', 'TRX', 'SNGLS', 'STRAT', 'BQX', 'FUN', 'KNC', 'CDT', 'XVG', 'IOTA', 'SNM', 'LINK', 'CVC', 'TNT', 'REP', 'MDA', 'MTL', 'SALT', 'NULS', 'SUB', 'STX', 'MTH', 'ADX', 'ETC', 'ENG', 'ZEC', 'AST', 'GNT', 'DGD', 'BAT', 'DASH', 'POWR', 'BTG', 'REQ', 'XMR', 'EVX', 'VIB', 'ENJ', 'VEN', 'ARK', 'XRP', 'MOD', 'STORJ', 'KMD', 'RCN', 'EDO', 'DATA', 'DLT', 'MANA', 'PPT', 'RDN', 'GXS', 'AMB', 'ARN', 'BCPT', 'CND', 'GVT', 'POE', 'BTS', 'FUEL', 'XZC', 'QSP', 'LSK', 'BCD', 'TNB', 'ADA', 'LEND', 'XLM', 'CMT', 'WAVES', 'WABI', 'GTO', 'ICX', 'OST', 'ELF', 'AION', 'WINGS', 'BRD', 'NEBL', 'NAV', 'VIBE', 'LUN', 'TRIG', 'APPC', 'CHAT', 'RLC', 'INS', 'PIVX', 'IOST', 'STEEM', 'NANO', 'AE', 'VIA', 'BLZ', 'SYS', 'RPX', 'NCASH', 'POA', 'ONT', 'ZIL', 'STORM', 'XEM', 'WAN', 'WPR', 'QLC', 'GRS', 'CLOAK', 'LOOM', 'BCN', 'TUSD', 'ZEN', 'SKY', 'THETA', 'IOTX', 'QKC', 'AGI', 'NXS', 'SC', 'NPXS', 'KEY', 'NAS', 'MFT', 'DENT', 'IQ', 'ARDR', 'HOT', 'VET', 'DOCK', 'POLY', 'VTHO', 'ONG', 'PHX', 'HC', 'GO', 'PAX', 'RVN', 'DCR', 'USDC', 'MITH', 'BCHABC', 'BCHSV', 'REN', 'BTT', 'USDS', 'FET', 'TFUEL', 'CELR', 'MATIC', 'ATOM', 'PHB', 'ONE', 'FTM', 'BTCB', 'USDSB', 'CHZ', 'COS', 'ALGO', 'ERD', 'DOGE', 'BGBP', 'DUSK', 'ANKR', 'WIN', 'TUSDB', 'COCOS', 'PERL', 'TOMO', 'BUSD', 'BAND', 'BEAM', 'HBAR', 'XTZ', 'NGN', 'DGB', 'NKN', 'GBP', 'EUR', 'KAVA', 'RUB', 'UAH', 'ARPA', 'TRY', 'CTXC', 'AERGO', 'BCH', 'TROY', 'BRL', 'VITE', 'FTT', 'AUD', 'OGN', 'DREP', 'TCT', 'WRX', 'LTO', 'ZAR', 'MBL', 'COTI', 'BKRW', 'HIVE', 'STPT', 'SOL', 'IDRT', 'CTSI', 'CHR', 'HNT', 'JST', 'FIO', 'BIDR', 'STMX', 'MDT', 'PNT', 'COMP', 'IRIS', 'MKR', 'SXP', 'SNX', 'DAI', 'DOT', 'RUNE', 'AVA', 'BAL', 'YFI', 'SRM', 'ANT', 'CRV', 'SAND', 'OCEAN', 'NMR', 'LUNA', 'IDEX', 'RSR', 'PAXG', 'WNXM', 'TRB', 'EGLD', 'BZRX', 'WBTC', 'KSM', 'SUSHI', 'YFII', 'DIA', 'BEL', 'UMA', 'NBS', 'WING', 'SWRV', 'CREAM', 'UNI', 'OXT', 'SUN', 'AVAX', 'BURGER', 'BAKE', 'FLM', 'SCRT', 'XVS', 'CAKE', 'SPARTA', 'ALPHA', 'ORN', 'UTK', 'NEAR', 'VIDT', 'AAVE', 'FIL', 'INJ', 'CTK', 'EASY', 'AUDIO', 'BOT', 'AXS', 'AKRO', 'HARD', 'KP3R', 'RENBTC', 'SLP', 'STRAX', 'UNFI', 'CVP', 'BCHA', 'FOR', 'FRONT', 'ROSE', 'MDX', 'HEGIC', 'PROM', 'BETH', 'SKL', 'GLM', 'SUSD', 'COVER', 'GHST', 'DF', 'JUV', 'PSG', 'BVND', 'GRT', 'CELO', 'TWT', 'REEF', 'OG', 'ATM', 'ASR', '1INCH', 'RIF', 'BTCST', 'TRU', 'DEXE', 'CKB', 'FIRO', 'LIT', 'PROS', 'VAI', 'SFP', 'FXS', 'DODO', 'AUCTION', 'UFT', 'ACM', 'PHA', 'TVK', 'BADGER', 'FIS', 'QI', 'OM', 'POND', 'ALICE', 'DEGO', 'BIFI', 'LINA', 'PERP', 'RAMP', 'SUPER', 'CFX', 'TKO', 'AUTO', 'EPS', 'PUNDIX', 'TLM', 'MIR', 'BAR', 'FORTH', 'EZ', 'AR', 'ICP', 'SHIB', 'GYEN', 'POLS', 'MASK', 'LPT', 'AGIX', 'ATA', 'NU', 'GTC', 'KLAY', 'TORN', 'KEEP', 'ERN', 'BOND', 'MLN', 'C98', 'FLOW', 'QUICK', 'RAY', 'MINA', 'QNT', 'CLV', 'XEC', 'ALPACA', 'FARM', 'VGX', 'MBOX', 'WAXP', 'TRIBE', 'GNO', 'USDP', 'DYDX', 'GALA', 'ILV', 'YGG', 'FIDA', 'AGLD', 'BETA', 'RAD', 'RARE', 'SSV', 'LAZIO', 'MOVR', 'CHESS', 'DAR', 'BNX', 'RGT', 'CITY', 'ENS', 'PORTO', 'NFT']
                    # select new token

                    new_token_lis = []
                    for each_token in token_lis:
                        if each_token in BIAN_token or each_token[1:] in BIAN_token:  # 以Wrapped开头的币和没有Wrapped开头的币
                            pass
                        else:
                            new_token_lis.append(each_token)
                            print(each_token)
                            send_mail(msg='new transactions found' + each_token + ":" + dic[each_token])   # 发送邮件

                    if len(new_token_lis) == 0:   # 都是已经上的币，print pass
                        print("pass")

                # 若成功抓取，则休息1分钟
                time.sleep(60)
            else:
                print("404")
                time.sleep(3)

        except:
            traceback.print_exc()
            time.sleep(3)
            pass


if __name__ == "__main__":
    # 币安的热钱包地址
    address_lis = ["0x8894E0a0c962CB723c1976a4421c95949bE2D4E3", "0xe2fc31F816A9b94326492132018C3aEcC4a93aE1",
                   "0x3c783c21a0383057D128bae431894a5C19F9Cf06", "0xdccF3B77dA55107280bd850ea519DF3705D1a75a",
                   "0xEB2d2F1b8c558a40207669291Fda468E50c8A0bB", "0x161bA15A5f335c9f06BB5BbB0A9cE14076FBb645",
                   "0x515b72Ed8a97F42C568D6A143232775018f133C8", "0xBD612a3f30dcA67bF60a39Fd0D35e39B7aB80774",
                   "0xa180Fe01B906A1bE37BE6c534a3300785b20d947", "0x631Fc1EA2270e98fbD9D92658eCe0F5a269Aa161",
                   "0xB1256D6b31E4Ae87DA1D56E5890C66be7f1C038e", "0x17B692ae403a8Ff3a3B2eD7676cF194310ddE9Af",
                   "0x8fF804cc2143451F454779A40DE386F913dCff20", "0xAD9ffffd4573b642959D3B854027735579555Cbc",
                   "0x7a8A34DB9acD10C3b6277473b192FE47192569cA"]
    timestamp = "2021-11-22T01:00:00"
    monitor_binance_hot_wallet(address_lis, timestamp=timestamp)
