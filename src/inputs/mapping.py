
def map_subcategory():
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
    "Home Accessories" : ['home', 'homeac','Furnit','furnit' ,'plate', 'gift'], 
    "Subscription": [],
    "Mobile" : [], 
    "Internet" : [], 
    "Water" : [], 
    "Electricity" : ['electric', 'electricity', 'electr'], 
    "Maid" : [],
    "Personal One Time" : ['ECS Txn Chrgs Incl GST'], 
    "Personal Recurring" : ['hair c', 'hair cut', 'hair cut', 'ECS Txn Chrgs'], 
    "Music" : [],
    "Entertainment" : [], 
    "Father" : [], 
    "Tour" : [],
    "Restuarant" : ['KITCHEN', 'barkas', 'swiggy', 'zomato', 'PULAK DAS', 'Rais  Anwer', 'Zomato'], 
    "Family Monthly" : ['clip', 'wife', 'dress'], 
    "Birds" : ['fruits', 'V SANTHOSH'], 
    "Extras" : [],
    "Grocery Regular" : ['Blinkit', 'Blinki', 'Mr SATISH KUMAR N', 'ASHRAF U K', 'grocer', 'grocery'], 
    "Quaterly" : [],
    "Fuel" : ['Serv', 'Sree Kodandarama Serv', 'AVIGHNA ENTERPRISES J', 'fuel'],
    "Bike Service" : ['parkin'],
    "Service" : ['bike'], 
    "Wash & Maintainence" : [], 
    "AutoCab" : [],
    "Tea & Others" : ['tea', 'IMPERIAL KOARAMANGALA', 'HARISH', 'GYANESWAR UPADHAYA', 
                      'KRISHANA KUMAR YADAV', 'GANAPATHI N NAIK ', 'SRINIDHI SAGAR FOODLI', 
                      'MEGHARAJ H C', 'MAHENDRA SHETTY', 'sri annapoorneshwary', 'MOHAMAD N.',
                      'GANAPATHI N NAIK', 'SHETTY', 'smk', 'bevera'], 
    "Others" : ['RAMBABU YADAV', 'other', 'others'],
    "Snacks" : ['food', 'RAMKUMARGUPTASOMOOLC', 'fuchka'], 
    "FoodRegular" : ['Mr S Chandran', 'food', 'snacks'], 
    "Office Food" : ['Hunger', 'Cake way'], 
    "Cooking Gas" : [],
    "Medical" : ['Pharma', 'medici'],
    "Flower" : ['flower', 'MANIGANDAN'], 
    "PujaOne" : ['puja'],
    "Miscellaneous" : [],
    "Fund Transfer" : ['Remitter', 'BANK'],
    "Savings": ['INDUSIND', 'save', 'LIMITED(RAZORPAY)/', 'LIMITED(ATOMTECH)/', 'gold'],
    "Bank Charges" : ['GST'],
    "Donation": ['Donati']
    }
    return subcategory_dropdown
