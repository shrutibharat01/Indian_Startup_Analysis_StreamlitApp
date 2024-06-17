""""Validation Rules/ Logic"""

class validation:
    
    # Overall Analaysis
    
    # for Line Chart - Option 1
    @staticmethod
    def momg1(df):
        tdf = df.groupby(['Year', 'Month'])['Amount in Rs.'].sum().reset_index()
        tdf['Amount in Crores'] = tdf['Amount in Rs.'] / 10000
        tdf['Month'] = tdf['Month'].astype(str).apply(lambda x: x[:3])
        tdf['Month-Year'] = tdf.apply(lambda x: f"{x['Month']} '{x['Year'] - 2000}", axis=1)
        return tdf[['Month-Year', 'Amount in Crores']]

    # for Line Chart - Option 2
    @staticmethod
    def momg2(df):
        tdf2 = df.groupby(['Year', 'Month'])['Amount in Rs.'].count().reset_index()
        tdf2.rename(columns={'Amount in Rs.': 'Count of investments'}, inplace=True)
        tdf2['Month'] = tdf2['Month'].astype(str).apply(lambda x: x[:3])
        tdf2['Month-Year'] = tdf2.apply(lambda x: f"{x['Month']} '{x['Year'] - 2000}", axis=1)
        return tdf2[['Month-Year', 'Count of investments']]

    # (Pie Chart)
    @staticmethod
    def catpie(df):
        cat = df.groupby('Vertical')['Amount in Rs.'].sum()
        cat = cat.sort_values(ascending=False)
        return cat.head()
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    
    # Startup Analysis
    
    # for Top 5 Startups DF ...
    @staticmethod
    def top5start(df, y):
        top5 = df.groupby(['Startup Name', 'Year', 'Month'])['Amount in Rs.'].sum().reset_index()
        top5['Amount in Rs.'] = top5['Amount in Rs.'] / 10000
        top5.rename(columns={'Amount in Rs.': "Amount in Cr."}, inplace=True)
        top5.set_index('Startup Name', inplace=True)
        return top5
    
    # Startup details ...
    @staticmethod
    def startup_details(df, name):
        res = df[df['Startup Name'] == name][['Date', 'Vertical', 'Sub Vertical', 'City', 'Round', 'Amount in Rs.']]
        res.rename(columns={'Amount in Rs.': 'Amount in Cr.'}, inplace=True)
        res.set_index('Date', inplace=True)
        return res.head()

    # Startup round investment ...
    @staticmethod
    def round_inv(df, name):
        df.rename(columns={'Amount in Rs.': 'Amount in Cr.'}, inplace=True)
        res = df[df['Startup Name'] == name].groupby('Round')['Amount in Cr.'].sum()
        return res.head()

    # Startup investor(s) ...
    @staticmethod
    def startup_inv(df, name):
        res = df[df['Startup Name'] == name]['Investor']
        res = res.reset_index(drop=True)
        res.index = res.index + 1
        return res
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    
    # Investor Analysis
    
    # Investor list
    @staticmethod
    def investor_list(df):
        # Convert the investor column to string
        df['Investor'] = df['Investor'].astype(str)
        df['Investor'] = df['Investor'].fillna('')
        il = sorted(set(df['Investor'].str.split(', ').sum()))
        return il
    
    # for Top 5 Investors DF ...
    @staticmethod
    def top5inv(df, y):
        top5 = df.groupby(['Investor', 'Year', 'Month'])['Amount in Rs.'].sum().reset_index()
        top5['Amount in Rs.'] = top5['Amount in Rs.'] / 10000
        top5.rename(columns={'Amount in Rs.': "Amount in Cr."}, inplace=True)
        top5.set_index('Investor', inplace=True)
        return top5
    
    # Load the recent 5 investments of the investor
    @staticmethod
    def recent_inv(df, name):
        recent = df[df['Investor'].str.contains(name)][['Date', 'Startup Name', 'Vertical','City', 'Round', 'Amount in Rs.']].sort_values(by='Date',ascending=False)
        recent.rename(columns={'Amount in Rs.': 'Amount in Cr.'}, inplace=True)
        recent.set_index('Date', inplace=True)
        return recent.head()

    # Biggest investments(BAR chart)
    @staticmethod
    def big_inv(df, name):
        df.rename(columns={'Amount in Rs.': 'Amount in Cr.'}, inplace=True)
        big = df[df['Investor'].str.contains(name)].groupby('Startup Name')['Amount in Cr.'].sum()
        big.sort_values(inplace=True, ascending=False)
        big = big.reset_index()
        return big.head()

    # Sectors invested(Pie chart)
    @staticmethod
    def sector_inv(df, name):
        sec = df[df['Investor'].str.contains(name)].groupby('Vertical')['Amount in Cr.'].sum().head()
        return sec

    # Stages invested (Pie chart)
    @staticmethod
    def stage_inv(df, name):
        stg = df[df['Investor'].str.contains(name)].groupby('Round')['Amount in Cr.'].sum().head()
        return stg

    # Cities(Pie chart)
    @staticmethod
    def city(df, name):
        ct = df[df['Investor'].str.contains(name)].groupby('City')['Amount in Cr.'].sum().head()
        return ct

    # Year on Year investment(Line chart)
    @staticmethod
    def yrinv(df, name):
        df.rename(columns={'Amount in Cr.': 'Amount in Crores'}, inplace=True)
        yi = df[df['Investor'].str.contains(name)].groupby('Year')['Amount in Crores'].sum()
        return yi

