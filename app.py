import streamlit as st
import pandas as pd
import numpy as np

# Import your custom modules
from data import Data
from costs import (
    subjects_order_cost,
    empty_space_groups_cost,
    empty_space_teachers_cost,
    free_hour,
    hard_constraints_cost,
    check_hard_constraints
)
from scheduler import Scheduler

# Initialize the scheduler and data
data = Data()
scheduler = Scheduler(data)

# Streamlit app
st.title("Timetable Scheduler")

st.sidebar.header("Options")
num_generations = st.sidebar.number_input("Number of Generations", min_value=1, max_value=1000, value=100)
population_size = st.sidebar.number_input("Population Size", min_value=1, max_value=100, value=20)
mutation_rate = st.sidebar.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.01)

if st.sidebar.button("Generate Timetable"):
    with st.spinner("Generating timetable..."):
        best_timetable = scheduler.evolve(num_generations, population_size, mutation_rate)
        st.success("Timetable generated!")

    # Display the timetable
    st.subheader("Generated Timetable")
    timetable_matrix = best_timetable.get_matrix()
    timetable_df = pd.DataFrame(timetable_matrix)
    st.dataframe(timetable_df)

    # Calculate and display costs
    st.subheader("Cost Analysis")
    subjects_order = best_timetable.get_subjects_order()
    groups_empty_space = best_timetable.get_groups_empty_space()
    teachers_empty_space = best_timetable.get_teachers_empty_space()

    order_cost = subjects_order_cost(subjects_order)
    group_empty_cost, group_max_empty, group_avg_empty = empty_space_groups_cost(groups_empty_space)
    teacher_empty_cost, teacher_max_empty, teacher_avg_empty = empty_space_teachers_cost(teachers_empty_space)
    free_hour_info = free_hour(timetable_matrix)
    hard_cost, _, teacher_hard_cost, classroom_hard_cost, group_hard_cost = hard_constraints_cost(timetable_matrix, data)
    hard_constraints_overlaps = check_hard_constraints(timetable_matrix, data)

    st.write(f"Subjects Order Cost: {order_cost:.2f}%")
    st.write(f"Groups Empty Space Cost: {group_empty_cost}, Max per Day: {group_max_empty}, Avg per Week: {group_avg_empty:.2f}")
    st.write(f"Teachers Empty Space Cost: {teacher_empty_cost}, Max per Day: {teacher_max_empty}, Avg per Week: {teacher_avg_empty:.2f}")
    st.write(f"Free Hour: {free_hour_info}")
    st.write(f"Hard Constraints Cost: {hard_cost}")
    st.write(f"Hard Constraints Overlaps: {hard_constraints_overlaps}")
    st.write(f"Teachers Hard Cost: {teacher_hard_cost}")
    st.write(f"Classrooms Hard Cost: {classroom_hard_cost}")
    st.write(f"Groups Hard Cost: {group_hard_cost}")

else:
    st.write("Use the sidebar to configure the timetable generation options and press 'Generate Timetable'.")

