from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_car_data(file_path):
    cars = []
    with open(file_path, mode="r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row['Price_Min'] = int(row['Price_Min'])
                row['Price_Max'] = int(row['Price_Max'])
                cars.append(row)
            except:
                continue
    return cars

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("About.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/price", methods=["GET", "POST"])
def price():
    cars = []
    searched = False  

    if request.method == "POST":
        searched = True  
        min_budget = int(request.form.get("min_budget", 0))
        max_budget = int(request.form.get("max_budget", 9999999))
        fuel = request.form.get("fuel", "").lower()
        transmission = request.form.get("Transmission", "").lower()

        all_cars = load_car_data("car.csv")

        for car in all_cars:
            if (
                min_budget <= car['Price_Min'] <= max_budget and
                (not fuel or car['Fuel'].lower() == fuel) and
                (not transmission or car['Transmission'].lower() == transmission)
            ):
                cars.append(car)

    return render_template("price.html", cars=cars, searched=searched)

@app.route('/')
def home():
    return "Hello from Render!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
