from flask import Flask, render_template, request
import email.parser

app = Flask(__name__)

def parse_email_headers(email_headers):
    parsed_headers = email.parser.Parser().parsestr(email_headers)
    return parsed_headers

def check_spf(parsed_headers):
    spf_record = parsed_headers.get('Received-SPF')
    if spf_record:
        if 'pass' in spf_record.lower():
            return True
    return False

def check_dkim(parsed_headers):
    dkim_record = parsed_headers.get('DKIM-Signature')
    if dkim_record:
        return True
    return False


def analyze_email(parsed_headers):
    spf_result = check_spf(parsed_headers)
    dkim_result = check_dkim(parsed_headers)

    if spf_result and dkim_result:
        return "Safe"
    else:
        return "Potentially Harmful"

def get_headers_table(parsed_headers):
    headers_table = []
    for key, value in parsed_headers.items():
        headers_table.append((key, value))
    return headers_table

def get_spf_dkim_table(parsed_headers):
    spf_record = parsed_headers.get('Received-SPF')
    dkim_record = parsed_headers.get('DKIM-Signature')
    return [("SPF Record", spf_record), ("DKIM Record", dkim_record)]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    email_headers = request.form['email_headers']
    parsed_headers = parse_email_headers(email_headers)
    analysis_result = analyze_email(parsed_headers)
    headers_table = get_headers_table(parsed_headers)
    spf_dkim_table = get_spf_dkim_table(parsed_headers)
    return render_template('result.html', email_headers=email_headers, analysis_result=analysis_result, headers_table=headers_table, spf_dkim_table=spf_dkim_table)

if __name__ == '__main__':
    app.run(debug=True)
