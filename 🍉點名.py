import streamlit as st
import pandas as pd
import json
import os
import random

# Load student data with caching
@st.cache_data
def load_students_data():
    return pd.read_excel("stu.xlsx")

# Save checked students list to file with timestamp
def save_checked_students():
    checked_students = st.session_state.checked_students
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    for student in checked_students:
        if "點名時間" not in student:
            student["點名時間"] = timestamp
    with open("checked_students.json", "w") as f:
        json.dump(checked_students, f)

# Load checked students list from file
def load_checked_students():
    if os.path.exists("checked_students.json"):
        with open("checked_students.json", "r") as f:
            return json.load(f)
    else:
        return []

# Initialize session state variables
if 'students_data' not in st.session_state:
    st.session_state.students_data = load_students_data()
if 'checked_students' not in st.session_state:
    st.session_state.checked_students = load_checked_students()  # Load from file

def main():
    st.image('school.jpg')
    st.title("高三小多元(Julia&數學)點名系統📚")

    students_data = st.session_state.students_data

    # 使用 st.form 包裹相關的元件，以支援按下 Enter 鍵
    with st.form("roll_call_form"):
        # Input for student ID
        student_id = st.text_input("請輸入學號：")

        # Button for roll call (inside the form)
        roll_call_button = st.form_submit_button("按我點名 🎉")

    # 判斷是否按下了 "點名" 按鈕或者按下了 Enter 鍵
    if roll_call_button:
        if student_id:
            student_name = get_student_name(student_id, students_data)

            if student_name is not None:
                if not is_student_checked(student_id):
                    st.success(f"你好，{student_name} 同學，很高興見到你！ 👋")
                    st.session_state.checked_students.append({"學號": int(student_id), "已點名": True})
                    save_checked_students()  # Save to file

                    # 隨機選擇 st.snow() 或 st.balloons() 顯示
                    random_effect = random.choice([st.snow, st.balloons])
                    random_effect()
                else:
                    st.warning("學號已經點過名，請不要重複點名。 ❌")
            else:
                st.warning("學號錯誤，請重新輸入。 ⚠️")
        else:
            st.warning("請輸入學號再點名。 ⌨️")

    # Display checked and unchecked student lists
    st.write("已點名學生列表：")
    display_checked_students()

    st.write("尚未點名的學生列表：")
    display_unchecked_students(students_data)

def get_student_name(student_id, students_data):
    student_info = students_data[students_data["學號"] == int(student_id)]
    return student_info.iloc[0]["姓名"] if not student_info.empty else None

def is_student_checked(student_id):
    return any(student["學號"] == int(student_id) for student in st.session_state.checked_students)

def display_checked_students():
    checked_students_df = pd.DataFrame(st.session_state.checked_students)
    st.table(checked_students_df)

def display_unchecked_students(students_data):
    unchecked_students = [student for student in students_data.to_dict(orient="records") if not is_student_checked(student["學號"])]
    st.table(pd.DataFrame(unchecked_students))

if __name__ == "__main__":
    main()
