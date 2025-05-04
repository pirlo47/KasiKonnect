from flask import Flask, request, jsonify
from models import db, ServiceProvider, CustomerProfile

app = Flask(__name__)

@app.route('/api/service-provider-profile', methods=['POST'])
def create_service_provider_profile():
    data = request.json
    provider = ServiceProvider(name=data['name'], email=data['email'], service=data['service'])
    db.session.add(provider)
    db.session.commit()
    return jsonify({'message': 'Profile created!'})

@app.route('/api/customer-profile', methods=['POST'])
def create_customer_profile():
    data = request.json
    customer = CustomerProfile(name=data['name'], email=data['email'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Profile created!'})