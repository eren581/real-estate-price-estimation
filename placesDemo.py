from selenium import webdriver
import time
import numpy as np

print("Please enter the path to folder which contains data:")
folder_path = input()

web_driver = webdriver.Chrome()

all_image_attributes = set()
house_list = list()

web_driver.get("http://places2.csail.mit.edu/demo.html")
i = 0
while i != -1:
    try:
        house_attributes = set()
        for j in range(10):
            file_upload_div = web_driver.find_element_by_id("file-upload")
            file_input_div = file_upload_div.find_element_by_id("fileinput")
            file_input_div.send_keys(folder_path + "\\" + str(i+1) + "_" + str(j+1) + ".jpg")
            predictions = web_driver.find_element_by_id("resultArea")
            time.sleep(0.5)
            attributes = predictions.find_elements_by_tag_name("li")[2].text.split(":")[1].split(",")
            for attribute in attributes:
                all_image_attributes.add(attribute.strip(" "))
                house_attributes.add(attribute.strip(" "))
        house_list.append(house_attributes)
        i += 1
    except:
        i = -1

all_data = list()
training_data = np.load(folder_path + "\\training_data.npy")
for i in range(len(training_data)):
    new_data = list(training_data[i])
    for attribute in all_image_attributes:
        if attribute in house_list[i]:
            new_data.append(1)
        new_data.append(all_data)
    print(new_data)

np.save(folder_path + "\\new_training_data.npy", np.array(all_data))
