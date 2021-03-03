import csv

if __name__ == '__main__':
    with open("data/slides_data/test/testing1.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(1475, 2500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing2.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(2500, 3500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing3.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(3500, 4500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing4.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(4500, 5500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing5.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(5500, 6500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing6.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(6500, 7500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing7.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(7500, 8500):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
    with open("data/slides_data/test/testing8.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(8500, 9898):  
            writer.writerow(["frame" + str(num) + ".jpg", 0])
