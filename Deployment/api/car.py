from pydantic import BaseModel
from typing import Literal

class Car(BaseModel):
    model_key: Literal["Citroën", "Renault", "BMW", "Peugeot", "Audi", "Nissan", "Mitsubishi", "Mercedes", "Volkswagen", "Toyota", "SEAT", "Subaru", "Opel", "Ferrari", "PGO", "Maserati", "Suzuki", "Porsche", "Ford", "KIA Motors", "Alfa Romeo", "Fiat", "Lexus", "Lamborghini", "Mini", "Mazda", "Honda", "Yamaha"]
    mileage: int
    engine_power: int
    fuel: Literal["diesel", "petrol", "hybrid_petrol", "electro"]
    paint_color: Literal["black", "grey", "blue", "white", "brown", "silver", "red", "beige", "green", "orange"]
    car_type: Literal["estate", "sedan", "suv", "hatchback", "subcompact", "coupe", "convertible", "van"]
    private_parking_available: bool = False
    has_gps: bool = False
    has_air_conditioning: bool = False
    automatic_car: bool = False
    has_getaround_connect: bool = False
    has_speed_regulator: bool = False
    winter_tires: bool = False

class CarResponse(Car):
    prediction_price: float