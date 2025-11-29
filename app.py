from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://ishanxstudio.space/rc?query={}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    vehicle_no = request.form.get('vehicle_no', '').strip().upper()
    
    if not vehicle_no:
        return jsonify({'status': 'error', 'message': 'कृपया गाड़ी का नंबर दर्ज करें!'})

    try:
        response = requests.get(API_URL.format(vehicle_no))
        data = response.json()
        rc_root = data.get("rc_chudai", {})
        
        if rc_root.get("status") and rc_root.get("data"):
            d = rc_root["data"][0]
            def get_val(key):
                val = d.get(key)
                return str(val) if val and val != "NA" else "N/A"

            result = {
                'status': 'success',
                'owner_info': {
                    'reg_no': get_val('reg_no'),
                    'owner': get_val('owner_name'),
                    'father': get_val('father_name'),
                    'mobile': get_val('mobile_no'),
                    'address': get_val('address'),
                    'financer': get_val('financer_details')
                },
                'vehicle_specs': {
                    'maker': get_val('maker'),
                    'model': f"{get_val('vehicle_model')} {get_val('vehicle_variant')}",
                    'color': get_val('vehicle_color'),
                    'fuel': f"{get_val('fuel_type')}",
                    'category': f"{get_val('vh_class')}",
                    'engine': f"{get_val('cubic_cap')} CC / {get_val('no_of_cyl')} Cyl",
                    'seats': get_val('no_of_seats')
                },
                'dates_status': {
                    'reg_date': get_val('regn_dt'),
                    'fitness': get_val('fitness_upto'),
                    'insurance': get_val('insUpto'),
                    'puc': get_val('puc_upto'),
                    'status': get_val('status'),
                    'rto': get_val('rto')
                },
                'extra': {
                    'insurer': get_val('insurance_comp'),
                    'price': get_val('resale_value')
                }
            }
            return jsonify(result)
        else:
            return jsonify({'status': 'error', 'message': '❌ डेटा नहीं मिला। नंबर सही डालें।'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': '⚠️ सर्वर एरर। बाद में प्रयास करें।'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)