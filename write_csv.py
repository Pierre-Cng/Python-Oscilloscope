import csv
import time
import math

def generate_number():
    number = 0
    while True:
        value = math.sin(number)
        timestamp = time.time()
        yield (timestamp, value)
        number += 1  
        time.sleep(0.1)  

def save_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        #csv_writer.writerow(['Timestamp', 'Number'])
        for value in data:
            csv_writer.writerow([value[0], value[1]])
            csvfile.flush()
            time.sleep(0.1)  # Wait for 100 milliseconds before writing the next value

if __name__ == "__main__":
    generator = generate_number()
    csv_filename = "data.csv"
    try:
        save_to_csv(csv_filename, generator)
    except KeyboardInterrupt:
        print("\nCSV file generation interrupted.")
