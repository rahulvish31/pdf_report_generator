import pandas as pd
import jinja2
import pdfkit

interest_rates = [i*.01 for i in range(1,11)]
initial_account_sizes = [100, 500, 20000, 50000]
data_frames = []

path_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

base_path = "C:\\Users\\HP\\documents\\github\\pdf_generator"

templateLoader = jinja2.FileSystemLoader(searchpath=base_path)
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "pdf_interest_report.html"
template = templateEnv.get_template(TEMPLATE_FILE)

for interest_rate in interest_rates:
    df = {}
    for initial_account_size in initial_account_sizes:
        df['Account Size: ' + str(initial_account_size)] = [initial_account_size * (1 + interest_rate) ** year for year in range(1, 21)]
    df = pd.DataFrame(df)
    df.index.name = 'year'
    data_frames.append({'df':df,
        'interest_rate':interest_rate})

for d in data_frames:
    outputText = template.render(df=d['df'],
            interest_rate=d['interest_rate'])
    html_file = open("output_results\\"+str(int(d['interest_rate'] * 100)) + '.html', 'w')
    html_file.write(outputText)
    html_file.close()

for i in range(1,11):
    print(str(i)+'.html',str(i)+'.pdf')
    pdfkit.from_file(base_path+"\\output_results\\"+str(i)+'.html', base_path+"\\output_results\\"+str(i) + '.pdf',configuration=config)
