from countrygroups import UNSTATS_GEOGRAPHICAL_REGIONS
from countrygroups import EUROPEAN_UNION
from shortcountrynames import to_name

essentials = {
    "tissues": "20",
    "toothpaste": "100",
    "tooth_brush": "70",
    "shower_gel": "300",
    "shampoo": "300",
    "antiperspirant": "200",
    "brush": "150",
    "ID_card": "10",
    "cards": "4",
    "pills": "20",
}

# recommended = {
#     "cash_money": "10",
#     "sun_protection": "100",
#     "driving_license": "10",
#     "passport": "10",
#     "cosmetic_cream": "150",
# }

electronics = {
    "charger": "80",
    "battery": "200",
    "phone": "200",
    "headphones": "50",
    "cable": "5",
}

# el_opt = {
#     "laptop": "2000",
#     "eReader": "100",
#     "gopro": "120",
#     "sd_card": "2",
#     "photo_camera": "500",
# }

# clothes = {
#     "jeans": "250",
#     "t-shirt": "100",
#     "underpants": "25",
#     "denim_shorts": "220",
#     "boxer_shorts": "61",
#     "socks": "30",
#     "blouse": "120",
#     "shirt": "150",
#     "hoodie": "450",
#     "shoes": "750",
#     "pijamas": "150",
#     "jacket": "600",
#     "scarf": "150",
#     "hat": "60",
#     "boots": "1500",
#     "gloves": "100",
#     "flip_flops": "110",
#     "shorts": "100",
#     "swim_suit": "90",
#     "beach_bag": "300",
# }


def process_baggage(visitor, weather, trip):
    baggage = {}
    baggage.update({"essentials": essentials})
    baggage.update({"electronics": electronics})
    baggage.update({"recommended": {}})
    baggage.update({"clothes_common": {}})
    baggage.update({"clothes": {}})

    if to_name(trip.get("country")) not in EUROPEAN_UNION.names:
        baggage.get("essentials").update({"passport": "10"})

    if to_name(trip.get("country")) not in UNSTATS_GEOGRAPHICAL_REGIONS.EUROPE.names:
        baggage.get("recommended").update({"eReader": "100"})
        baggage.get("recommended").update({"gopro": "120"})
        baggage.get("recommended").update({"sd_card": "2"})

    if to_name(trip.get("country")) in UNSTATS_GEOGRAPHICAL_REGIONS.AMERICAS.names:
        baggage.get("essentials").update({"visa": "10"})

    baggage.get("clothes_common").update({"flip_flops": "110"})

    if visitor.get("gender") == "F":
        baggage.get("recommended").update({"makeup": "500"})
        baggage.get("recommended").update({"cosmetic_cream": "500"})

    for i in range(len(weather) // 3):
        baggage.get("clothes_common").update({f"pijamas_{i+1}": "150"})

    if len(weather) > 7:
        baggage.get("recommended").update({"laptop": "2000"})

    for day in weather:
        baggage.get("clothes").update({f"{day.get('date')}": {}})

        baggage.get("clothes").get(f"{day.get('date')}").update({"underwear": "25"})
        baggage.get("clothes").get(f"{day.get('date')}").update({"socks": "30"})

        if int(day.get("temp")) > 30:
            baggage.get("recommended").update({"sun_protection": "100"})
            baggage.get("clothes_common").update({"hat": "60"})
            if visitor.get("gender") == "M":
                baggage.get("clothes").get(f"{day.get('date')}").update(
                    {"shorts": "100"}
                )
            else:
                baggage.update(
                    {"clothes": {f"{day.get('date')}": {"denim_shorts": "220"}}}
                )
        if int(day.get("temp")) in range(20, 99):
            baggage.get("clothes").get(f"{day.get('date')}").update({"t-shirt": "100"})
        if int(day.get("temp")) in range(20, 29):
            baggage.get("clothes").get(f"{day.get('date')}").update({"jeans": "250"})
        if int(day.get("temp")) in range(15, 19):
            baggage.get("clothes").get(f"{day.get('date')}").update({"jeans": "250"})
            baggage.get("clothes").get(f"{day.get('date')}").update({"blouse": "150"})
        if int(day.get("temp")) in range(5, 14):
            baggage.get("clothes").get(f"{day.get('date')}").update({"jeans": "250"})
            baggage.get("clothes_common").update({"jacket": "600"})
            baggage.get("clothes").get(f"{day.get('date')}").update({"blouse": "150"})
            baggage.get("clothes_common").update({"hoodie": "600"})
        if int(day.get("temp")) < 5:
            baggage.get("clothes_common").update({"boots": "1500"})
            baggage.get("clothes").get(f"{day.get('date')}").update({"jeans": "250"})
            baggage.get("clothes").get(f"{day.get('date')}").update({"blouse": "150"})
            baggage.get("clothes_common").update({"gloves": "100"})
            baggage.get("clothes_common").update({"hat": "60"})
            baggage.get("clothes_common").update({"winter_jacket": "1000"})
        if int(day.get("temp")) < -5:
            baggage.get("clothes").get(f"{day.get('date')}").update({"leggings": "100"})
        if int(day.get("precipitation")) > 200 and int(day.get("temp")) > 0:
            baggage.get("recommended").update({"umbrella": "300"})
            baggage.get("clothes_common").update({"raincoat": "500"})
        if int(day.get("wind")) > 100 and int(day.get("temp")) in range(5, 14):
            baggage.get("clothes").get(f"{day.get('date')}").update(
                {"wind_jacket": "100"}
            )
    total_weight = 0
    for key in baggage:
        if key in ["essentials", "electronics", "recommended", "clothes_common"]:
            for item_key in baggage.get(key):
                total_weight += int(baggage.get(key).get(item_key))
        elif key == "clothes":
            for day_key in baggage.get(key):
                for item_day_key in baggage.get(key).get(day_key):
                    total_weight += int(baggage[key][day_key][item_day_key])

    baggage.update({"total_weight": str(total_weight / 1000)})

    return baggage
