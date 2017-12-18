from selenium import webdriver
import requests
import numpy as np
import re

web_driver = webdriver.Chrome()

print("Please enter the city the data will be collected from:")
city_page = input()
print("Please enter the number of data you want to collect:")
number_of_data = input()
print("Please enter the number of images you want to collect:")
number_of_images = input()
print("Please enter the path of the folder in which you want to store collected data:")
folder_path = input()

all_data = []
advertisement_ids = []


def number_of_room(str_number_of_room):
    number_of_rooms = [0, 0]
    if str_number_of_room == "Stüdyo (1+0)":
        number_of_rooms[1] = 1
        return number_of_rooms
    elif str_number_of_room == "10 Üzeri":
        number_of_rooms[0] = 1
        return number_of_rooms
    else:
        number_of_rooms[1] = int(number_of_room_element.split("+")[0]) + int(number_of_room_element.split("+")[1])
        return number_of_rooms


# def building_age(str_building_age):
#     age = [0, 0, 0, 0, 0, 0, 0]
#     if str_building_age == "5-10 arası":
#         age[0] = 1
#         return age
#     elif str_building_age == "11-15 arası":
#         age[1] = 1
#         return age
#     elif str_building_age == "16-20 arası":
#         age[2] = 1
#         return age
#     elif str_building_age == "21-25 arası":
#         age[3] = 1
#         return age
#     elif str_building_age == "26-30 arası":
#         age[4] = 1
#         return age
#     elif str_building_age == "31 ve üzeri":
#         age[5] = 1
#         return age
#     else:
#         age[6] = int(str_building_age)
#         return age


# def building_floor(str_building_floor):
#     floor_of_the_building = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     if str_building_floor == "Kot 4":
#         floor_of_the_building[0] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Kot 3":
#         floor_of_the_building[1] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Kot 2":
#         floor_of_the_building[2] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Kot 1":
#         floor_of_the_building[3] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Bodrum Kat":
#         floor_of_the_building[4] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Zemin Kat":
#         floor_of_the_building[5] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Bahçe Katı":
#         floor_of_the_building[6] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Giriş Katı":
#         floor_of_the_building[7] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Yüksek Giriş":
#         floor_of_the_building[8] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Müstakil":
#         floor_of_the_building[9] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Villa Tipi":
#         floor_of_the_building[10] = 1
#         return floor_of_the_building
#     elif str_building_floor == "Çatı Katı":
#         floor_of_the_building[11] = 1
#         return floor_of_the_building
#     elif str_building_floor == "30 ve üzeri":
#         floor_of_the_building[12] = 1
#         return floor_of_the_building
#     else:
#         floor_of_the_building[13] = int(str_building_floor)
#         return floor_of_the_building


# def total_floor(str_total_floor):
#     total_floor_in_building = [0,0]
#     if str_total_floor == "30 ve üzeri":
#         total_floor_in_building[0] = 1
#         return total_floor_in_building
#     else:
#         total_floor_in_building[1] = int(str_total_floor)
#         return total_floor_in_building


# def heating_type(str_heating_type):
#     heating_types = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     if str_heating_type == "Yok":
#         return heating_types
#     elif str_heating_type == "Soba":
#         heating_types[0] = 1
#         return heating_types
#     elif str_heating_type == "Doğalgaz Sobası":
#         heating_types[1] = 1
#         return heating_types
#     elif str_heating_type == "Kat Kaloriferi":
#         heating_types[2] = 1
#         return heating_types
#     elif str_heating_type == "Merkezi":
#         heating_types[3] = 1
#         return heating_types
#     elif str_heating_type == "Merkezi (Pay Ölçer)":
#         heating_types[4] = 1
#         return heating_types
#     elif str_heating_type == "Doğalgaz (Kombi)":
#         heating_types[5] = 1
#         return heating_types
#     elif str_heating_type == "Yerden Isıtma":
#         heating_types[6] = 1
#         return heating_types
#     elif str_heating_type == "Klima":
#         heating_types[7] = 1
#         return heating_types
#     elif str_heating_type == "Fancoil Ünitesi":
#         heating_types[8] = 1
#         return heating_types
#     elif str_heating_type == "Güneş Enerjisi":
#         heating_types[9] = 1
#         return heating_types
#     elif str_heating_type == "Jeotermal":
#         heating_types[10] = 1
#         return heating_types
#     elif str_heating_type == "Şömine":
#         heating_types[11] = 1
#         return heating_types
#     elif str_heating_type == "VRV":
#         heating_types[12] = 1
#         return heating_types
#     elif str_heating_type == "Isı Pompası":
#         heating_types[13] = 1
#         return heating_types


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


current_data_count = 0
i = 0
while current_data_count < int(number_of_data):
    web_driver.get("https://www.sahibinden.com/satilik/" + city_page.lower() + "?pagingOffset=" + str(i))
    search_results = web_driver.find_elements_by_class_name("searchResultsTitleValue ")
    print("Starting to parse data from page!")

    j = 0
    while j in range(20) and current_data_count < int(number_of_data):
        advertisement_url = search_results[j].find_element_by_class_name(" classifiedTitle").get_attribute("href")
        web_driver.get(advertisement_url)
        try:
            # Get the attribute data
            info_div = web_driver.find_element_by_class_name("classifiedDetailContent")
            details = info_div.find_element_by_class_name("classifiedInfoList")
            info_list = details.find_elements_by_tag_name("li")

            # ID of the advertisement. This information will be used to prevent using the same advertisement again.
            advertisement_id = info_div.find_element_by_id("classifiedId").text

            if advertisement_id in advertisement_ids:
                break;

            # Price of the house
            price = int("".join(info_div.find_element_by_tag_name("h3").text.split("\n")[0].strip(' TL').split(".")))

            # City that the house located in
            city = info_div.find_element_by_tag_name("h2").find_elements_by_tag_name("a")[0].text

            # District of the city
            district = info_div.find_element_by_tag_name("h2").find_elements_by_tag_name("a")[1].text

            # Size(area) of the house in meter square
            size = int(info_list[3].find_element_by_tag_name("span").text)

            # Total number of rooms in the house
            number_of_room_element = info_list[4].find_element_by_tag_name("span").text
            number_of_rooms = number_of_room(number_of_room_element.strip(" "))
            #number_of_rooms = number_of_room(number_of_room_element.strip(" "))

            # Age of the building
            info_list[5].find_element_by_tag_name("span").text.strip(" ")
            #age = building_age(info_list[5].find_element_by_tag_name("span").text.strip(" "))

            # The floor of the apartment
            apartment_floor = info_list[6].find_element_by_tag_name("span").text.strip(" ")
            #apartment_floor = building_floor(info_list[6].find_element_by_tag_name("span").text.strip(" "))

            # Total number of floors in the building
            number_of_floors_in_building = int(info_list[7].find_element_by_tag_name("span").text.strip(" "))
            #number_of_floors_in_building = total_floor(info_list[7].find_element_by_tag_name("span").text.strip(" "))

            # Heating type of the building
            heating_type_of_building = info_list[8].find_element_by_tag_name("span").text.strip(" ")
            #heating_type_of_building = heating_type(info_list[8].find_element_by_tag_name("span").text.strip(" "))

            # Total number of bathrooms in the house
            number_of_bathrooms = int(info_list[9].find_element_by_tag_name("span").text)

            # Does apartment have a balcony
            has_balcony = info_list[10].find_element_by_tag_name("span").text

            # Is the apartment being sold with furniture
            with_furniture = info_list[11].find_element_by_tag_name("span").text

            # Get other properties of the house. These have also boolean values.
            properties = web_driver.find_element_by_id("classifiedProperties").find_elements_by_tag_name("li")

            # Does the house have woodwork
            woodwork = property_to_boolean(properties, 5)

            # Does the house have thief alert
            thief_alert = property_to_boolean(properties, 7)

            # Does the building have elevator(important for apartments)
            elevator = property_to_boolean(properties, 12)

            # Does the house have security
            security = property_to_boolean(properties, 57)

            # Does the house have heat insulation
            heat_ins = property_to_boolean(properties, 59)

            # Does the house have parking lot
            parking_lot = property_to_boolean(properties, 65)

            # Does the house have sport facilities
            sport = property_to_boolean(properties, 69)

            # Is there any shopping mall around the house
            shopping_mall = property_to_boolean(properties, 89)

            # Is there any hospital around the house
            hospital = property_to_boolean(properties, 97)

            # Is there any market place around the house
            market_place = property_to_boolean(properties, 101)

            # Is there any university around the house
            university = property_to_boolean(properties, 107)

            # Is the house in town center
            town_center = property_to_boolean(properties, 110)

            # Is the house close to a main road
            main_road = property_to_boolean(properties, 111)

            # Is the house close to a metro station
            metro = property_to_boolean(properties, 120)

            # Is the house clsoe to a bus station
            bus_station = property_to_boolean(properties, 123)

            # Does the house have sea view
            sea_view = property_to_boolean(properties, 131)

            # Does the house have nature view
            nature_view = property_to_boolean(properties, 132)

            # Create an array of attributes
            inp_array = list()
            inp_array.append(price)
            inp_array.append(city)
            inp_array.append(district)
            inp_array.append(size)
            inp_array.append(number_of_rooms)
            inp_array.append(age)
            inp_array.append(apartment_floor)
            inp_array.append(number_of_floors_in_building)
            inp_array.append(heating_type_of_building)
            inp_array.append(number_of_bathrooms)
            inp_array.append(has_balcony)
            inp_array.append(with_furniture)
            inp_array.append(woodwork)
            inp_array.append(thief_alert)
            inp_array.append(elevator)
            inp_array.append(security)
            inp_array.append(heat_ins)
            inp_array.append(parking_lot)
            inp_array.append(sport)
            inp_array.append(shopping_mall)
            inp_array.append(hospital)
            inp_array.append(market_place)
            inp_array.append(university)
            inp_array.append(town_center)
            inp_array.append(main_road)
            inp_array.append(metro)
            inp_array.append(bus_station)
            inp_array.append(sea_view)
            inp_array.append(nature_view)

            # Get image data
            images_div = web_driver.find_element_by_class_name("classifiedDetailThumbListContainer")
            img_elements = images_div.find_elements_by_tag_name("label")

            # Save image data
            for k in range(int(number_of_images)):
                img_src = img_elements[k].find_element_by_tag_name("img").get_attribute("src")  # Thumbnail sized image
                img_src = re.sub('thmb', 'x5', img_src)  # Convert thumbnail sized image to its real size
                img = requests.get(img_src)
                image_file = open(folder_path + "/" + str(current_data_count+1) + "_" + str(k + 1) + ".jpg", "wb")
                image_file.write(img.content)
            all_data.append(inp_array)
            current_data_count += 1
            print("Data is added!")
        except:
            print("Unexpected data occurred!")
        web_driver.get("https://www.sahibinden.com/satilik/" + city_page.lower() + "?pagingOffset=" + str(i))
        search_results = web_driver.find_elements_by_class_name("searchResultsTitleValue ")
        j += 1
    i += 20
    print("End of page!")

np.save(folder_path + "/training_data.npy", np.array(all_data))
