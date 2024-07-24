    fig = px.bar(quantity_df,x="Product line",y ='Quantity',text=['${:,.2f}'.format(x)for x in quantity_df['Quantity']],template = "seaborn")
