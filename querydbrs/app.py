from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'monsterzero',  # Update with your database user
    'password': 'Monsterzero@8910',  # Update with your database password
    'database': 'dbrs'  # Update with your database name
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return redirect(url_for('sample_page'))

@app.route('/sample')
def sample_page():
    return render_template('sample.html')

@app.route('/member_transactions', methods=['POST'])
def member_transactions():
    # Retrieve form data from sample.html
    member_id = request.form['member_id']
    start_date = request.form['date_from_member']
    end_date = request.form['date_to_member']

    # Establish a database connection
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # SQL query to fetch member transaction data
    query = """SELECT TRAN_DATE, TRAN_ID, b.account_name , 
               DR_AMT AS total_debit, CR_AMT AS total_credit
               FROM detail_member_trans a
               LEFT JOIN mast_account b ON a.acc_id = b.account_id
               WHERE tran_date >= %s AND tran_date <= %s AND mbr_id = %s
               ORDER BY tran_date, tran_ID;
    """
    cursor.execute(query, (start_date, end_date, member_id))
    transactions = cursor.fetchall()

    # Format TRAN_DATE to dd-mm-yyyy
    for transaction in transactions:
        transaction['TRAN_DATE'] = transaction['TRAN_DATE'].strftime('%d-%m-%Y')

    cursor.close()
    connection.close()

    # Render the result page with formatted transactions
    return render_template('result.html', member_id=member_id, transactions=transactions)

@app.route('/account_entries', methods=['POST'])
def account_entries():
    # Retrieve form data from sample.html
    date_from = request.form['date_from_account']
    date_to = request.form['date_to_account']

    # Establish a database connection
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # SQL query to fetch account entries data
    query = """
        SELECT a.tran_date, a.tran_id, a.tran_sr_id, b.account_name, a.dr_amt, a.cr_amt
        FROM journal_entries a
        LEFT JOIN mast_account b ON a.account_id = b.account_id
        WHERE a.tran_date >= %s AND a.tran_date <= %s
        ORDER BY a.tran_date, a.tran_id;
    """
    cursor.execute(query, (date_from, date_to))
    transactions = cursor.fetchall()

    # Format tran_date to dd-mm-yyyy
    for transaction in transactions:
        transaction['tran_date'] = transaction['tran_date'].strftime('%d-%m-%Y')

    cursor.close()
    connection.close()

    # Render the result page with formatted account entries
    return render_template('result.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
