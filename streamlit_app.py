# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Variables


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """
    Choose the fruits you want in your custom Smoothie
  """
)
cnx = st.connection("snowflake")
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
#     index=None,
#     placeholder="Select your fruit"
# )

# st.write(f"Your favorite fruit is: {option}")


name_on_order = st.text_input("Name on Smoothie: ")
st.write(f"The name on your Smoothie will be: {name_on_order}")




#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5,
    
)

# New section to display smoothiefroot nutrition information
smoothiefroot_response = requests.get('https://my.smoothiefroot.com/api/fruit/watermelon')
st.text(smoothiefroot_response)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredient_string = ''

    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
        
    # st.write(ingredient_string)

    my_insert_stm = """
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('""" + ingredient_string + """', '""" + name_on_order + """');
    """

    #st.write(my_insert_stm)
    #st.stop()

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stm).collect()
        st.success(f"Your smoothie is ordered, {name_on_order}", icon="✅")
        name_on_order = ''
        ingredients_list = ''
    
