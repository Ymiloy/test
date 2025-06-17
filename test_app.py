import unittest
from job_offer_app.app import app
from job_offer_app.models import db, JobOffer
from datetime import datetime

class JobOfferAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Good practice for form testing
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_create_job_offer_model(self):
        """Test direct creation of a JobOffer model instance."""
        with app.app_context():
            initial_count = JobOffer.query.count()
            now = datetime.utcnow()
            offer = JobOffer(
                title="Software Engineer Test",
                description="Test description for a software engineer.",
                company="TestCorp",
                location="Testville",
                salary="100k-120k",
                posted_date=now
            )
            db.session.add(offer)
            db.session.commit()

            self.assertEqual(JobOffer.query.count(), initial_count + 1)
            retrieved_offer = JobOffer.query.filter_by(title="Software Engineer Test").first()
            self.assertIsNotNone(retrieved_offer)
            self.assertEqual(retrieved_offer.company, "TestCorp")
            self.assertEqual(retrieved_offer.location, "Testville")
            self.assertEqual(retrieved_offer.salary, "100k-120k")
            # For datetime, comparing directly might have microsecond differences with some DBs
            self.assertTrue((now - retrieved_offer.posted_date).total_seconds() < 1)

    def test_02_create_job_offer_route(self):
        """Test creating a job offer via the /create route."""
        with app.app_context():
            initial_count = JobOffer.query.count()

        response = self.client.post('/create', data={
            'title': 'Flask Developer',
            'description': 'Develop Flask apps.',
            'company': 'Flask Inc.',
            'location': 'Python City',
            'salary': '150k'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200) # Should redirect to home, then 200
        with app.app_context():
            self.assertEqual(JobOffer.query.count(), initial_count + 1)
            offer = JobOffer.query.filter_by(title='Flask Developer').first()
            self.assertIsNotNone(offer)
            self.assertEqual(offer.company, 'Flask Inc.')

    def test_03_read_job_offers(self):
        """Test reading job offers on the home page."""
        with app.app_context():
            offer = JobOffer(title="Reader Test Offer", description="Desc", company="Reader Co", location="Readsville")
            db.session.add(offer)
            db.session.commit()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Reader Test Offer", response.data)
        self.assertIn(b"Reader Co", response.data)

    def test_04_update_job_offer_route(self):
        """Test updating a job offer via the /edit/<id> route."""
        with app.app_context():
            offer = JobOffer(title="Original Title", description="Original Desc", company="Original Co", location="Originalville")
            db.session.add(offer)
            db.session.commit()
            offer_id = offer.id

        response = self.client.post(f'/edit/{offer_id}', data={
            'title': 'Updated Title',
            'description': 'Updated Desc.',
            'company': 'Updated Co.',
            'location': 'Updatedville',
            'salary': '200k'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            updated_offer = JobOffer.query.get(offer_id)
            self.assertEqual(updated_offer.title, 'Updated Title')
            self.assertEqual(updated_offer.company, 'Updated Co.')
            self.assertEqual(updated_offer.salary, '200k')

    def test_05_delete_job_offer_route(self):
        """Test deleting a job offer via the /delete/<id> route."""
        with app.app_context():
            offer = JobOffer(title="To Be Deleted", description="Delete me", company="DeleteCorp", location="Deleteville")
            db.session.add(offer)
            db.session.commit()
            offer_id = offer.id
            self.assertIsNotNone(JobOffer.query.get(offer_id))

        response = self.client.post(f'/delete/{offer_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertIsNone(JobOffer.query.get(offer_id))

    def test_06_edit_nonexistent_offer(self):
        """Test GET request to /edit/<id> for a non-existent offer."""
        response = self.client.get('/edit/999')
        self.assertEqual(response.status_code, 404)

    def test_07_delete_nonexistent_offer(self):
        """Test POST request to /delete/<id> for a non-existent offer."""
        response = self.client.post('/delete/999')
        self.assertEqual(response.status_code, 404)

    def test_08_empty_db_message(self):
        """Test that the 'No job offers' message appears when DB is empty."""
        # Ensure DB is empty (tearDown handles this before each test, setUp creates tables)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No job offers posted yet.", response.data)
        # Also check that the link to create one is there
        self.assertIn(b"Create one now!", response.data)


if __name__ == '__main__':
    unittest.main()
