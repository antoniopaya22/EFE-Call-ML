import csv

if __name__ == '__main__':
    with open("mapping.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for num in range(0, 800):
            if num <= 2:
                writer.writerow(["frame" + str(num) + ".jpg", 0])
            elif num == 3:
                writer.writerow(["frame" + str(num) + ".jpg", 3])
            elif 3 < num < 386:
                writer.writerow(["frame" + str(num) + ".jpg", 2])
            elif 386 <= num < 563:
                writer.writerow(["frame" + str(num) + ".jpg", 1])
            elif 563 <= num <= 800:
                writer.writerow(["frame" + str(num) + ".jpg", 0])
