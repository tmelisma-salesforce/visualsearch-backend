#!python3

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Clothing Data Model
class ClothingItem:
    def __init__(self, brand, name, color, type, gender, product_number):
        self.brand = brand
        self.name = name
        self.color = color
        self.type = type
        self.gender = gender
        self.product_number = product_number

    def to_dict(self):
        return {
            "brand": self.brand,
            "name": self.name,
            "color": self.color,
            "type": self.type,
            "gender": self.gender,
            "product_number": self.product_number
        }

# Populate clothing inventory
clothing_inventory = [
    # Jeans
    ClothingItem("Levi's", "501 Original Fit Jeans", "Blue", "Pants", "Men's", "LEVI-501-BLUE-34-32"),
    ClothingItem("Wrangler", "Cowboy Cut Original Fit Jean", "Indigo", "Pants", "Men's", "WRAN-ORIG-INDIGO-36-34"),
    
    # Regular Pants
    ClothingItem("Dockers", "Classic Fit Khaki Pants", "Khaki", "Pants", "Men's", "DOCK-CLASS-KHAKI-34-30"),
    ClothingItem("Gap", "Slim Fit Chino Pants", "Navy", "Pants", "Men's", "GAP-SLIM-NAVY-32-32"),
    
    # Dresses
    ClothingItem("Anthropologie", "Midi Wrap Dress", "Floral Print", "Dress", "Women's", "ANTH-MIDI-FLORAL-S"),
    ClothingItem("Zara", "Satin Slip Dress", "Emerald Green", "Dress", "Women's", "ZARA-SLIP-EMERALD-M"),
    ClothingItem("Free People", "Bohemian Maxi Dress", "Rust", "Dress", "Women's", "FP-BOHO-RUST-L"),
    
    # Skirts
    ClothingItem("H&M", "A-Line Denim Skirt", "Light Blue", "Skirt", "Women's", "HM-ALINE-DENIM-S"),
    ClothingItem("Urban Outfitters", "Pleated Mini Skirt", "Black", "Skirt", "Women's", "UO-PLEATED-BLACK-M")
]

@app.route('/search')
def search_clothing():
    url = request.args.get('url', '')
    
    if url == 'https://melisma.net/jeans.jpg':
        results = [
            clothing_inventory[0].to_dict(),
            clothing_inventory[1].to_dict(),
            clothing_inventory[2].to_dict(),
            clothing_inventory[3].to_dict()
        ]
        return jsonify(results)
    
    elif url == 'https://melisma.net/dress.jpg':
        # Return 2 dresses and 1 skirt
        results = [
            clothing_inventory[4].to_dict(),
            clothing_inventory[5].to_dict(),
            clothing_inventory[6].to_dict(),
            clothing_inventory[7].to_dict(),
            clothing_inventory[8].to_dict()
        ]
        return jsonify(results)
    
    # For any other URL, return an empty JSON structure
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))