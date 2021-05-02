#!/usr/bin/env python3

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
import sqlite3

REWARDS_CONTRACT = "cx10d59e8103ab44635190bd4139dbfd682fa2d07e"
BALN_CONTRACT = "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619"
BNUSD_CONTRACT = "cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
SICX_CONTRACT = "cx2609b924e33ef00b648a409245c7ea394c467824"
DEX_CONTRACT = "cxa0af3165c08318e988cb30993b3048335b94af6c"
ICX_CONTRACT = "cx0000000000000000000000000000000000000000"
SICXICX_POOL_ID = 1
EXA = 10**18
APY = 10**16

icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

def getAPY(pair) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(REWARDS_CONTRACT)\
                        .method("getAPY")\
                        .params({"_name": pair})\
                        .build()
    return int(icon_service.call(call), 0)

def getPriceByName(pair) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getPriceByName")\
                        .params({"_name": pair})\
                        .build()
    return int(icon_service.call(call), 0)

def getPoolBase(id) -> str:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getPoolBase")\
                        .params({"_id": id})\
                        .build()
    return icon_service.call(call)

def getBasePriceInQuote(id) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getBasePriceInQuote")\
                        .params({"_id": id})\
                        .build()
    return int(icon_service.call(call), 0)

def getQuotePriceInBase(id) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getQuotePriceInBase")\
                        .params({"_id": id})\
                        .build()
    return int(icon_service.call(call), 0)

def getPoolStats(id) -> dict:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getPoolStats")\
                        .params({"_id": id})\
                        .build()
    return icon_service.call(call)

def getPoolId(token1, token2) -> int:
    if (token1 == SICX_CONTRACT and token2 == ICX_CONTRACT):
        return SICXICX_POOL_ID
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getPoolId")\
                        .params({"_token1Address": token1, "_token2Address": token2})\
                        .build()
    return int(icon_service.call(call), 0)

def totalSupply(token) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(token)\
                        .method("totalSupply")\
                        .build()
    return int(icon_service.call(call), 0)

def totalStakedBalance(token) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(token)\
                        .method("totalStakedBalance")\
                        .build()
    return int(icon_service.call(call), 0)

def get_balanced_data() -> dict:
    sicx_icx_pool = getPoolId(SICX_CONTRACT, ICX_CONTRACT)
    sicx_bnusd_pool = getPoolId(SICX_CONTRACT, BNUSD_CONTRACT)
    baln_bnusd_pool = getPoolId(BALN_CONTRACT, BNUSD_CONTRACT)
    sicx_icx_stats = getPoolStats(sicx_icx_pool)
    sicx_bnusd_stats = getPoolStats(sicx_bnusd_pool)
    baln_bnusd_stats = getPoolStats(baln_bnusd_pool)

    return {
        "sicxIcxApy": getAPY('sICX/ICX'),
        "balnBnusdApy": getAPY('BALN/bnUSD'),
        "sicxBnusdApy": getAPY('sICX/bnUSD'),
        
        "totalBalnSupply": totalSupply(BALN_CONTRACT),
        "stakedBalnSupply": totalStakedBalance(BALN_CONTRACT),

        "balnBnusdPrice": getPriceByName('BALN/bnUSD'),
        "sicxBnusdPrice": getPriceByName('sICX/bnUSD'),

        "sicxIcxPool": int(sicx_icx_stats["quote"], 0),
        "sicxBnusdPool": [int(sicx_bnusd_stats["base"], 0), int(sicx_bnusd_stats["quote"], 0)],
        "balnBnusdPool": [int(baln_bnusd_stats["base"], 0), int(baln_bnusd_stats["quote"], 0)],
    }

# Get ping
data = get_balanced_data()
print(data)

# get db data
conn = sqlite3.connect('./baln.db')
c = conn.cursor()

c.execute("INSERT INTO balnBnusdApy VALUES (datetime('now', 'localtime'), %f)" % (data['balnBnusdApy'] / APY))
c.execute("INSERT INTO sicxBnusdApy VALUES (datetime('now', 'localtime'), %f)" % (data['sicxBnusdApy'] / APY))
c.execute("INSERT INTO sicxIcxApy VALUES (datetime('now', 'localtime'), %f)" % (data['sicxIcxApy'] / APY))
c.execute("INSERT INTO totalBalnSupply VALUES (datetime('now', 'localtime'), %f)" % (data['totalBalnSupply'] / EXA))
c.execute("INSERT INTO stakedBalnSupply VALUES (datetime('now', 'localtime'), %f)" % (data['stakedBalnSupply'] / EXA))
c.execute("INSERT INTO balnBnusdPrice VALUES (datetime('now', 'localtime'), %f)" % (data['balnBnusdPrice'] / EXA))
c.execute("INSERT INTO sicxBnusdPrice VALUES (datetime('now', 'localtime'), %f)" % (data['sicxBnusdPrice'] / EXA))
c.execute("INSERT INTO sicxIcxPool VALUES (datetime('now', 'localtime'), %f)" % (data['sicxIcxPool'] / EXA))
c.execute("INSERT INTO sicxBnusdPool VALUES (datetime('now', 'localtime'), %f, %f)" % (data['sicxBnusdPool'][0] / EXA, data['sicxBnusdPool'][1] / EXA))
c.execute("INSERT INTO balnBnusdPool VALUES (datetime('now', 'localtime'), %f, %f)" % (data['balnBnusdPool'][0] / EXA, data['balnBnusdPool'][1] / EXA))

conn.commit()
conn.close()
