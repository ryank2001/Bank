from cardreader import CardReader
from apiconnect import apiconnect
from flask import Flask, render_template,  request, url_for, flash, redirect

card = CardReader()
api = apiconnect()  

import json 
# create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'

@app.route('/')
def index():
    return render_template('form.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        naam = request.form['naam']
        pincode = int(request.form['pincode'])
        email = request.form['email']
        iban = request.form['iban']
        data = iban
        card.writecard(data)
       
        data = card.checkcard()
        print(data)
        api.createrekening(iban, pincode, email)



      
    
        return render_template('form.html')

    return render_template('form2.html')
messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]



if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=4999)



