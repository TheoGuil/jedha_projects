from pydantic import BaseModel
from enum import Enum

class Model(str, Enum):
    Citroën = "Citroën"
    Renault = "Renault"
    BMW = "BMW"
    Peugeot = "Peugeot"
    Audi = "Audi"
    Nissan = "Nissan"
    Mitsubishi = "Mitsubishi"
    Mercedes = "Mercedes"
    Volkswagen = "Volkswagen"
    Toyota = "Toyota"
    SEAT = "SEAT"
    Subaru = "Subaru"
    Opel = "Opel"
    Ferrari = "Ferrari"
    PGO = "PGO"
    Maserati = "Maserati"
    Suzuki = "Suzuki"
    Porsche = "Porsche"
    Ford = "Ford"
    KIA_Motors = "KIA Motors"
    Alfa_Romeo = "Alfa Romeo"
    Fiat = "Fiat"
    Lexus = "Lexus"
    Lamborghini = "Lamborghini"
    Mini = "Mini"
    Mazda = "Mazda"
    Honda = "Honda"
    Yamaha = "Yamaha"   

class Fuel(str, Enum):
    diesel = "diesel"
    petrol = "petrol"
    hybrid_petrol = "hybrid_petrol"
    electro = "electro"
    
class PaintColor(str, Enum):
    black  = "black"   
    grey   = "grey"   
    blue   = "blue"   
    white  = "white"   
    brown  = "brown"   
    silver = "silver"   
    red    = "red"   
    beige  = "beige"   
    green  = "green"   
    orange = "orange" 

class Car_Type(str, Enum):
    estate = "estate"
    sedan = "sedan"
    suv = "suv"
    hatchback = "hatchback"
    subcompact = "subcompact"
    coupe = "coupe"
    convertible = "convertible"
    van = "van"

class Car(BaseModel):
    model_key: Model
    mileage: int
    engine_power: int
    fuel: Fuel
    paint_color: PaintColor
    car_type: Car_Type
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool
