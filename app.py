from flask import Flask, request, make_response, render_template
import pandas as pd
from datetime import datetime
import locale

def your_function(df):
    # CSV dosyasını oku
    df_original = df

    df = df_original[["Device", "Start Date", "End Date"]]

    # Tarihleri datetime nesnesine dönüştür
    df["Start Date"] = df["Start Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    df["End Date"] = df["End Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))


    # Tarihlerden yıl ve ay sütunlarını extract et
    df["start_year"] = df["Start Date"].apply(lambda x: x.year)
    df["start_month"] = df["Start Date"].apply(lambda x: x.month)
    df["end_year"] = df["End Date"].apply(lambda x: x.year)
    df["end_month"] = df["End Date"].apply(lambda x: x.month)


    current_year = min(min(df["start_year"]), min(df["end_year"]))
    max_year = max(max(df["start_year"]), max(df["end_year"]))

    current_month = 1

    while(1):
        
        df.loc[(df['start_year'] <= current_year) & (df['start_month'] <= current_month)  & (df['end_year'] >= current_year) & (df['end_month'] >= current_month) , current_month] = 1

        current_month += 1
        
        if current_month == 13:
            current_month = 1
            current_year += 1

        if current_year > max_year:
            break



    df.drop(columns=["Start Date", "End Date", "start_year", "start_month", "end_month"], inplace=True)

    df.rename(columns={"end_year":"Year"}, inplace=True)


    sum_df = df.groupby(by=['Device','Year']).sum()

    rst_indx_df = sum_df.reset_index(drop=False)

    # sorted_df = rst_indx_df.sort_values(by='Device', key=lambda x: locale.strcoll(x, 'tr_TR.UTF-8'))

    # sorted_df = sorted(rst_indx_df, key=lambda s: s.lower().translate(turkishTable))
    #abccdefgghiijklmnooprsstuuvyz
    #abcçdefgğhıijklmnoöprsştuüvyz
    # ascii_upper_letters   = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'
    ascii_upper_letters   = 'ABCCDEFGGHIIJKLMNOOPRSSTUUVYZ'
    turkish_upper_letters = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'

    # ascii_lower_letters   = 'abcçdefgğhıijklmnoöprsştuüvyz'
    ascii_lower_letters   = 'abccdefgghiijklmnooprsstuuvyz'
    turkish_lower_letters = 'abcçdefgğhıijklmnoöprsştuüvyz'

    turkish_letters = turkish_upper_letters + turkish_lower_letters
    ascii_letters = ascii_upper_letters + ascii_lower_letters


    turkishTable = str.maketrans(turkish_letters, ascii_letters)


    rst_indx_df['Device'] = rst_indx_df['Device'].apply(lambda x: x.translate(turkishTable))
    sorted_df = rst_indx_df.sort_values(by=['Device'])
    sorted_df = sorted_df.astype({col: int for col in sorted_df.columns if sorted_df[col].dtype == 'float64'})

    return sorted_df

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        new_df = your_function(df)
        return render_template('table.html',  tables=[new_df.to_html(classes='data')], titles = ['na', 'Monthly Issue Status of Power Plants'])
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)