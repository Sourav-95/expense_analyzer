import pandas as pd

def map_subcategory(data):
    """
    Creates a keywords dictionary based on a list of indices.
    Args: Index_list: A list of indices.
    Returns: A dictionary where keys are indices and values are lists of keywords.
    """
    subcategory_dropdown = {
    "HDFC" : [], 
    "Fibe" : [], 
    "Credit Card" : [], 
    "Money View" : [],
    "Home" : [], 
    "Subscription": [],
    "Mobile" : [], 
    "Internet" : [], 
    "Water" : [], 
    "Electricity" : [], 
    "Maid" : [],
    "Personal One Time" : [], 
    "Personal Recurring" : ['hair c', 'hair cut', 'hair cut', 'ECS Txn Chrgs'], 
    "Music" : [],
    "Entertainment" : [], 
    "Father" : [], 
    "Tour" : [],
    "Restuarant" : ['KITCHEN', 'barkas', 'swiggy', 'zomato', 'PULAK DAS', 'Rais  Anwer'], 
    "Wife Recurring" : ['clip'], 
    "Birds" : ['fruits'], 
    "Extras" : [],
    "Grocery Regular" : ['Blinkit', 'Blinki', 'Mr SATISH KUMAR N', 'ASHRAF U K'], 
    "Quaterly" : [],
    "Fuel" : ['Serv', 'Sree Kodandarama Serv', 'AVIGHNA ENTERPRISES J'], 
    "Service" : ['bike'], 
    "Wash & Maintainence" : [], 
    "AutoCab" : [],
    "Tea & Others" : ['tea', 'IMPERIAL KOARAMANGALA', 'HARISH', 'GYANESWAR UPADHAYA', 
                      'KRISHANA KUMAR YADAV', 'GANAPATHI N NAIK ', 'SRINIDHI SAGAR FOODLI', 
                      'MEGHARAJ H C', 'MAHENDRA SHETTY'], 
    "Others" : ['RAMBABU YADAV'],
    "Snacks" : ['food', 'RAMKUMARGUPTASOMOOLC', 'fuchka'], 
    "FoodRegular" : ['Mr S Chandran', 'food'], 
    "Office Food" : ['Hunger', 'Cake way'], 
    "Cooking Gas" : [],
    "Medical" : ['Pharma', 'medici'],
    "Flower" : ['flower', 'MANIGANDAN', ], 
    "PujaOne" : ['puja', ],
    "Miscellaneous" : []
    }
