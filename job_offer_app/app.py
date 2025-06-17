from flask import Flask, render_template, request, redirect, url_for, abort
from .models import db, JobOffer

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

# Database tables will be created by test setup or a dedicated CLI command/init function

@app.route('/')
def home():
    offers = JobOffer.query.order_by(JobOffer.posted_date.desc()).all()
    return render_template('index.html', offers=offers)

@app.route('/create', methods=['GET', 'POST'])
def create_offer():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        location = request.form['location']
        salary = request.form['salary']

        new_offer = JobOffer(
            title=title,
            description=description,
            company=company,
            location=location,
            salary=salary
        )
        db.session.add(new_offer)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_offer.html')

@app.route('/edit/<int:offer_id>', methods=['GET', 'POST'])
def edit_offer(offer_id):
    offer = JobOffer.query.get_or_404(offer_id)
    if request.method == 'POST':
        offer.title = request.form['title']
        offer.description = request.form['description']
        offer.company = request.form['company']
        offer.location = request.form['location']
        offer.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_offer.html', offer=offer)

@app.route('/delete/<int:offer_id>', methods=['POST'])
def delete_offer(offer_id):
    offer = JobOffer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
