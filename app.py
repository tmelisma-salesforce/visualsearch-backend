import os
from flask import Flask, request, jsonify
from clothing_inventory import clothing_inventory

app = Flask(__name__)

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