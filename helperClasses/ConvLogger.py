# -*- coding: utf-8 -*-
# Anne: for Logging
import json
import time
import datetime
import math


# File is saved with human readable timestamp as unique file name
def save_to_json(conversation):
    curr_timestamp = math.trunc(time.time())
    converted_timestamp = datetime.datetime.fromtimestamp(curr_timestamp)
    file_name = str(converted_timestamp)
    file_name = file_name.replace(":", "_").replace(" ", "_")
    with open("./ConversationOutputs/" + file_name + ".json", "w", encoding="utf-8") as json_file:
        json.dump(conversation, json_file, indent=2, ensure_ascii=False)
