import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

try:
    import plotly.express as px
except ImportError as e:
    raise ImportError("Plotly is not installed or accessible.") from e


# Load/Save Workout Data
def load_workouts():
    if os.path.exists('workouts.json'):
        with open('workouts.json', 'r') as f:
            return json.load(f)
    return []

def save_workout(workout_data):
    workouts = load_workouts()
    workouts.append(workout_data)
    with open('workouts.json', 'w') as f:
        json.dump(workouts, f)

# Main App
def main():
    st.set_page_config(page_title="Fitness Tracker", page_icon="💪", layout="wide")
    st.title("💪 Fitness Tracker")
    st.markdown("### Stay consistent, stay strong!")

    # Tabs for sections
    tab1, tab2, tab3 = st.tabs(["Log Workout", "Track Progress", "Leaderboard"])

    with tab1:
        st.subheader("Log Today's Workout")
        with st.form("workout_form"):
            date = st.date_input("Date", datetime.now())
            exercise = st.text_input("Exercise (e.g., Running, Yoga)")
            duration = st.number_input("Duration (minutes)", min_value=1, step=1)
            calories = st.number_input("Calories Burned", min_value=1, step=1)
            submit = st.form_submit_button("Log Workout")

            if submit:
                workout_data = {
                    "date": date.strftime("%Y-%m-%d"),
                    "exercise": exercise,
                    "duration": duration,
                    "calories": calories,
                }
                save_workout(workout_data)
                st.success("Workout logged successfully!")

    with tab2:
        st.subheader("Your Fitness Progress")
        workouts = load_workouts()
        if workouts:
            df = pd.DataFrame(workouts)
            df['date'] = pd.to_datetime(df['date'])
            st.dataframe(df)

            # Calories Burned Over Time
            fig = px.line(df, x="date", y="calories", title="Calories Burned Over Time", markers=True)
            st.plotly_chart(fig)

            # Total Calories Burned
            total_calories = df['calories'].sum()
            st.metric(label="Total Calories Burned", value=f"{total_calories} kcal")
        else:
            st.info("No workouts logged yet. Start tracking now!")

    with tab3:
        st.subheader("Leaderboard")
        workouts = load_workouts()
        if workouts:
            df = pd.DataFrame(workouts)
            leaderboard = df.groupby("exercise")['calories'].sum().reset_index()
            leaderboard = leaderboard.sort_values(by="calories", ascending=False)
            st.write(leaderboard)

            # Visualize Leaderboard
            fig = px.bar(leaderboard, x="exercise", y="calories", title="Calories Burned by Exercise")
            st.plotly_chart(fig)
        else:
            st.info("No data for leaderboard yet.")

if __name__ == "__main__":
    main()
