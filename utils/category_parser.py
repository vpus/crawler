import json
import re

with open("configs/categories.json") as f:
    CATEGORY_MAP = json.load(f)

TYPICAL_ESPORTS = [
    "dota2", "csgo", "leagueoflegends", "legendsofruneterra", "valorant",
    "mobilelegends"
]


def parse(category):
    parsed_category =  CATEGORY_MAP[re.sub('[^0-9a-zA-Z]+', "-",
                               category.replace("\n", "").lower())]
    if parsed_category not in TYPICAL_ESPORTS:
        return ["more-esports", parsed_category]
    else:
        return [parsed_category]
