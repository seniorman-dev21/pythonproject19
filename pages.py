import streamlit as st
from player_class import *
from player_class import Midfielder

user = User()

def welcome():
    st.title("Welcome")
    st.write(f"Hello, **{st.session_state.user_name}** 👋")


def page1():
    st.title("Welcome")
    user = User()
    stats_filled = user.input_stats()
    player_created = user.create_a_new_player()

    if stats_filled and player_created:
        import Realwork as rw  # Assuming this has FORWARD_STATS etc.

        # Select position (optional)
        position = st.selectbox("Select Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"])

        # Create the player based on selected position
        if position == "Forward":
            player = Forward()
        elif position == "Midfielder":
            player = Midfielder()
        elif position == "Defender":
            player = Defender()
        else:
            player = Goalkeeper()

        rating = player.get_rating(user.stats)
        st.success(f"{user.player_name}'s Rating: {rating:.2f}")

        # Store in DB
        everything = Everything(user_id=1, player_id=user.player_id, rating=rating)  # Assuming user_id=1 for demo
        everything.store()


def page2():
    st.title("Page 2")
    st.write("This is Page 2 content.")