from selenium import webdriver
import requests
import numpy as np
import re
import random

web_driver = webdriver.Chrome()

print("Please enter the city the data will be collected from:")
city_name = input()
print("Please enter the path to towns.txt file:")
towns_path = input()
print("Please enter the number of data you want to collect from each town:")
number_of_data = input()
print("Please enter the number of images you want to collect:")
number_of_images = input()
print("Please enter the path of the folder in which you want to store collected data:")
folder_path = input()

all_data = []
advertisement_ids = []


def number_of_room(str_number_of_room):
    if str_number_of_room == "Stüdyo (1+0)":
        return 1
    elif str_number_of_room == "10 Üzeri":
        return 18
    else:
        return int(str_number_of_room.split("+")[0]) + int(str_number_of_room.split("+")[1])


def building_age(str_building_age):
    if str_building_age == "5-10 arası":
        return 8
    elif str_building_age == "11-15 arası":
        return 13
    elif str_building_age == "16-20 arası":
        return 18
    elif str_building_age == "21-25 arası":
        return 23
    elif str_building_age == "26-30 arası":
        return 28
    elif str_building_age == "31 ve üzeri":
        return 35   # An arbitrary age is given in this case
    else:
        return 2


def building_floor(str_building_floor):
    floor_of_the_building = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if str_building_floor == "Kot 1" or str_building_floor == "Kot 2" or str_building_floor == "Kot 3" or str_building_floor == "Kot 4":
        floor_of_the_building[0] = 1
        return floor_of_the_building
        return floor_of_the_building
    elif str_building_floor == "Bodrum Kat":
        floor_of_the_building[1] = 1
        return floor_of_the_building
    elif str_building_floor == "Zemin Kat":
        floor_of_the_building[2] = 1
        return floor_of_the_building
    elif str_building_floor == "Bahçe Katı":
        floor_of_the_building[3] = 1
        return floor_of_the_building
    elif str_building_floor == "Giriş Katı":
        floor_of_the_building[4] = 1
        return floor_of_the_building
    elif str_building_floor == "Yüksek Giriş":
        floor_of_the_building[5] = 1
        return floor_of_the_building
    elif str_building_floor == "Müstakil":
        floor_of_the_building[6] = 1
        return floor_of_the_building
    elif str_building_floor == "Villa Tipi":
        floor_of_the_building[7] = 1
        return floor_of_the_building
    elif str_building_floor == "Çatı Katı":
        floor_of_the_building[8] = 1
        return floor_of_the_building
    elif str_building_floor == "30 ve üzeri":
        floor_of_the_building[9] = 1
        return floor_of_the_building
    else:
        floor_of_the_building[10] = int(str_building_floor)
        return floor_of_the_building


def total_floor(str_total_floor):
    if str_total_floor == "30 ve üzeri":
        return 40
    else:
        return int(str_total_floor)


def heating_type(str_heating_type):
    heating_types = [0, 0, 0, 0, 0, 0, 0, 0]
    if str_heating_type == "Yok":
        return heating_types
    elif str_heating_type == "Soba":
        heating_types[0] = 1
        return heating_types
    elif str_heating_type == "Doğalgaz Sobası":
        heating_types[1] = 1
        return heating_types
    elif str_heating_type == "Kat Kaloriferi":
        heating_types[2] = 1
        return heating_types
    elif str_heating_type == "Merkezi" or str_heating_type == "Merkezi (Pay Ölçer)":
        heating_types[3] = 1
        return heating_types
    elif str_heating_type == "Doğalgaz (Kombi)":
        heating_types[5] = 1
        return heating_types
    elif str_heating_type == "Yerden Isıtma":
        heating_types[6] = 1
        return heating_types
    elif str_heating_type == "Şömine":
        heating_types[11] = 1
        return heating_types


def meter_square_to_int(str_meter_square):
    try:
        return int(str_meter_square)
    except:
        return int("".join(str_meter_square.split(".")))


def has_balcony(str_has_balcony):
    if str_has_balcony == "Var":
        return 1
    else:
        return 0


def with_furniture(str_with_furniture):
    if str_with_furniture == "Evet":
        return 1
    else:
        return 0


def property_to_boolean(properties, element_index):
    if properties[element_index].get_attribute("class") == "selected":
        return 1
    else:
        return 0


def collect_data(city_page, town, total_data_count, number_of_img):
    web_driver.get("https://www.sahibinden.com/satilik/" + city_page.lower() + "-" + town.lower() + "?pagingOffset=")
    search_results = web_driver.find_elements_by_class_name("searchResultsTitleValue ")
    number_of_results_str = web_driver.find_element_by_class_name("result-text").find_elements_by_tag_name("span")[1].text
    number_of_results = int("".join(number_of_results_str.split(" ")[0].split(".")))

    current_data_count = 0
    i = 0
    while current_data_count < number_of_results and current_data_count < int(total_data_count):
        print("Starting to parse data from page!")
        j = 0
        while j in range(20) and current_data_count<number_of_results and current_data_count<int(total_data_count):
            advertisement_url = search_results[j].find_element_by_class_name(" classifiedTitle").get_attribute("href")
            web_driver.get(advertisement_url)
            try:
                # Get the attribute data
                info_div = web_driver.find_element_by_class_name("classifiedDetailContent")
                details = info_div.find_element_by_class_name("classifiedInfoList")
                info_list = details.find_elements_by_tag_name("li")

                # Create an array of attributes
                inp_array = list()

                # ID of the advertisement. This information will be used to prevent using the same advertisement again.
                advertisement_id = info_div.find_element_by_id("classifiedId").text

                if advertisement_id not in advertisement_ids:
                    # Price of the house
                    price = int(
                        "".join(info_div.find_element_by_tag_name("h3").text.split("\n")[0].strip(' TL').split(".")))
                    inp_array.append(price)

                    # City that the house located in
                    city = info_div.find_element_by_tag_name("h2").find_elements_by_tag_name("a")[0].text
                    inp_array.append(city)

                    # District of the city
                    district = info_div.find_element_by_tag_name("h2").find_elements_by_tag_name("a")[1].text
                    inp_array.append(district)

                    # Size(area) of the house in meter square
                    size = int(info_list[3].find_element_by_tag_name("span").text)
                    inp_array.append(size)

                    # Total number of rooms in the house
                    number_of_room_element = info_list[4].find_element_by_tag_name("span").text
                    number_of_rooms = number_of_room(number_of_room_element.strip(" "))
                    inp_array.append(number_of_rooms)

                    # Age of the building
                    age = building_age(info_list[5].find_element_by_tag_name("span").text.strip(" "))
                    inp_array.append(age)

                    # The floor of the apartment
                    apartment_floor = building_floor(info_list[6].find_element_by_tag_name("span").text.strip(" "))
                    inp_array.extend(apartment_floor)

                    # Total number of floors in the building
                    number_of_floors_in_building = total_floor(
                        info_list[7].find_element_by_tag_name("span").text.strip(" "))
                    inp_array.append(number_of_floors_in_building)

                    # Heating type of the building
                    heating_type_of_building = heating_type(
                        info_list[8].find_element_by_tag_name("span").text.strip(" "))
                    inp_array.extend(heating_type_of_building)

                    # Total number of bathrooms in the house
                    number_of_bathrooms = int(info_list[9].find_element_by_tag_name("span").text)
                    inp_array.append(number_of_bathrooms)

                    # Does apartment have a balcony
                    has_balcony = info_list[10].find_element_by_tag_name("span").text
                    inp_array.append(has_balcony)

                    # Is the apartment being sold with furniture
                    with_furniture = info_list[11].find_element_by_tag_name("span").text
                    inp_array.append(with_furniture)

                    # Get other properties of the house. These have also boolean values.
                    properties = web_driver.find_element_by_id("classifiedProperties").find_elements_by_tag_name("li")

                    # Does the house have woodwork
                    woodwork = property_to_boolean(properties, 5)
                    inp_array.append(woodwork)

                    # Does the house have thief alert
                    thief_alert = property_to_boolean(properties, 7)
                    inp_array.append(thief_alert)

                    # Does the building have elevator(important for apartments)
                    elevator = property_to_boolean(properties, 12)
                    inp_array.append(elevator)

                    # Does the house have fiber internet
                    fiber_net = property_to_boolean(properties, 17)
                    inp_array.append(fiber_net)

                    # Does the house have laminated ground
                    laminated_ground = property_to_boolean(properties, 30)
                    inp_array.append(laminated_ground)

                    # parquet
                    parquet = property_to_boolean(properties, 38)
                    inp_array.append(parquet)

                    # Does the house have security
                    security = property_to_boolean(properties, 57)
                    inp_array.append(security)

                    # Does the house have heat insulation
                    heat_ins = property_to_boolean(properties, 59)
                    inp_array.append(heat_ins)

                    # Does the house have parking lot
                    parking_lot = property_to_boolean(properties, 65)
                    inp_array.append(parking_lot)

                    # Does the house have sport facilities
                    sport = property_to_boolean(properties, 69)
                    inp_array.append(sport)

                    # Is there any shopping mall around the house
                    shopping_mall = property_to_boolean(properties, 89)
                    inp_array.append(shopping_mall)

                    # Is there any hospital around the house
                    hospital = property_to_boolean(properties, 97)
                    inp_array.append(hospital)

                    # Is there any market place around the house
                    market_place = property_to_boolean(properties, 101)
                    inp_array.append(market_place)

                    # Is there any university around the house
                    university = property_to_boolean(properties, 107)
                    inp_array.append(university)

                    # primary school
                    primary_school = property_to_boolean(properties, 108)
                    inp_array.append(primary_school)

                    # Is the house in town center
                    town_center = property_to_boolean(properties, 110)
                    inp_array.append(town_center)

                    # Is the house close to a main road
                    main_road = property_to_boolean(properties, 111)
                    inp_array.append(main_road)

                    # Is the house close to a metro station
                    metro = property_to_boolean(properties, 120)
                    inp_array.append(metro)

                    # Is the house clsoe to a bus station
                    bus_station = property_to_boolean(properties, 123)
                    inp_array.append(bus_station)

                    # minibus
                    minibus = property_to_boolean(properties, 122)
                    inp_array.append(minibus)

                    # Does the house have nature view
                    nature_view = property_to_boolean(properties, 132)
                    inp_array.append(nature_view)

                    # Get image data
                    images_div = web_driver.find_element_by_class_name("classifiedDetailThumbListContainer")
                    img_elements = images_div.find_elements_by_tag_name("label")

                    # Save image data
                    # current_img_count = 0
                    # for k in random_img_indices:
                    #     img_src = img_elements[k].find_element_by_tag_name("img").get_attribute("src")  # Thumbnail sized image
                    #     img_src = re.sub('thmb', 'x5', img_src)  # Convert thumbnail sized image to its real size
                    #     img = requests.get(img_src)
                    #     image_file = open(folder_path + "/" + str(len(all_data)) + "_" + str(current_img_count + 1) + ".jpg", "wb")
                    #     image_file.write(img.content)
                    #     current_img_count += 1
                    #all_data.append(inp_array)
                    current_data_count += 1
                    advertisement_ids.append(advertisement_id)
                    print("Data is added!")
                else:
                    print("Data already exists!")
            except:
                print("Unexpected data occurred!")
            web_driver.get("https://www.sahibinden.com/satilik/"+city_page.lower()+"-"+town.lower()+"?pagingOffset="+str(i))
            search_results = web_driver.find_elements_by_class_name("searchResultsTitleValue ")
            j += 1
        i += 20
        print("End of page!")


towns_file = open(towns_path, "r")
for line in towns_file:
    collect_data(city_name, line, number_of_data, number_of_images)

np.save(folder_path + "/training_data.npy", np.array(all_data))
