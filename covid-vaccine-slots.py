import requests
import MySQLdb
import json
from fake_useragent import UserAgent
from datetime import datetime
from datetime import timedelta
import sys

def get_info(item):
	vac = {}
	vac["center_id"] = int(item["center_id"])
	vac["name"] = "'" + item["name"] + "'"
	vac["address"] = "'" + item["address"] + "'"
	vac["pincode"] = "'" + str(item["pincode"]) + "'"
	vac["district_name"] = "'" + item["district_name"] + "'"
	vac["date"] = "'" + datetime.strptime(item["date"],"%d-%m-%Y").strftime("%Y-%m-%d") + "'"
	vac["available_capacity_dose1"] = int(item["available_capacity_dose1"])
	vac["available_capacity_dose2"] = int(item["available_capacity_dose2"])
	vac["fee"] = "'" + item["fee"] + "'"
	vac["min_age_limit"] = int(item["min_age_limit"])
	vac["vaccine"] = "'" + item["vaccine"] + "'"
	vac["slots"] = "'" + str(len(item["slots"])) + "'"
	return vac;


number_of_days = range(int(sys.argv[1]))
vac_date_list = []

for i in number_of_days:
	vac_date_list.append((datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d"))	

pin_code_list = [147001,324009,560103,208023]

db = MySQLdb.connect("127.0.0.1","root","","test")
# db = MySQLdb.connect("nv29.mysql.pythonanywhere-services.com", "nv29", "vaccineslots", "nv29$vaccine_slots")

cursor = db.cursor()

temp_user_agent = UserAgent()
# browser_header = {'User-Agent': str(temp_user_agent.random)}
browser_header = {'User-Agent': "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"}


for vac_date in vac_date_list:
	for pin_code in pin_code_list:
		url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + str(pin_code)  + "&date=" + str(vac_date)
		table_name = "vaccine_slots"
		response = requests.request("GET", url, headers=browser_header)
		res = json.loads(response.text)
		for item in res["sessions"]:
			vac = get_info(item)
			query = "INSERT INTO " + table_name + " (center_id, name, address, pincode, district_name, date, available_capacity_dose1, available_capacity_dose2, fee, min_age_limit, vaccine, slots) VALUES (" + str(vac["center_id"]) + "," + str(vac["name"]) + "," + str(vac["address"]) + "," + str(vac["pincode"]) + "," + str(vac["district_name"]) + "," + str(vac["date"]) + "," + str(vac["available_capacity_dose1"]) + "," + str(vac["available_capacity_dose2"]) + "," + str(vac["fee"]) + "," + str(vac["min_age_limit"]) + "," + str(vac["vaccine"]) + "," + str(vac["slots"]) + ")"
			print query
			cursor.execute(query)

db.commit()