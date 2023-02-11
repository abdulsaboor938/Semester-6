import numpy as np
import pandas as pd

# numpy functions

def grade_numpy(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14):
    with open('result.txt', 'w') as f:
        f.write('Numpy/n')
        f.write(f"Question 1: {np.array_equal(q1, np.arange(10))}\n")
        f.write(f"Question 2: {np.array_equal(q2, np.ones((3,3), dtype=bool))}\n")
        f.write(f"Question 3: {np.array_equal(q3, np.array([1,3,5,7,9]))}\n")
        f.write(f"Question 4: {np.array_equal(q4, np.array([[0,1,2,3,4],[5,6,7,8,9]]))}\n")
        f.write(f"Question 5: {np.array_equal(q5, np.array([[0,1,2,3,4],[5,6,7,8,9],[1,1,1,1,1],[1,1,1,1,1]]))}\n")
        f.write(f"Question 6: {np.array_equal(q6, np.array([1,1,1,2,2,2,3,3,3,1,2,3,1,2,3,1,2,3]))}\n")
        f.write(f"Question 7: {np.array_equal(q7, np.array([2,4]))}\n")
        f.write(f"Question 8: {np.array_equal(q8, np.array([1,2,3,4]))}\n")
        f.write(f"Question 9: {np.array_equal(q9, np.array([6,9]))}\n")
        f.write(f"Question 10: {np.array_equal(q10, np.array([6,7,9,8,9,7,5]))}\n")
        f.write(f"Question 11: {np.array_equal(q11, np.array([[1,0,2],[4,3,5],[7,6,8]]))}\n")
        f.write(f"Question 12: {np.array_equal(q12, np.array([[3,4,5],[0,1,2],[6,7,8]]))}\n")
        f.write(f"Question 13: {np.array_equal(q13, np.array([[6,7,8],[3,4,5],[0,1,2]]))}\n")
        f.write(f"Question 14: {np.array_equal(q14, np.array([[2,1,0],[5,4,3],[8,7,6]]))}\n\n")

# pandas functions

def grade_pandas(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15):
    with open('result.txt', 'a') as f:
        f.write('Pandas/n')
        orig = pd.read_csv('data.csv')

        f.write(f"Question 1: {orig.equals(q1)}\n")
        df = orig.head(3)
        f.write(f"Question 2: {df.equals(q2)}\n")
        df = orig[['name','age']]
        f.write(f"Question 3: {df.equals(q3)}\n")
        df = orig.loc[[3,4,8],['name','age','number_of_pets']]
        f.write(f"Question 4: {df.equals(q4)}\n")
        df = orig[orig['number_of_pets']>3]
        f.write(f"Question 5: {df.equals(q5)}\n")
        df = orig[orig['age'].isnull()]
        f.write(f"Question 6: {df.equals(q6)}\n")
        df = orig[~orig['name'].isin(['Dan','Alice'])]
        f.write(f"Question 7: {df.equals(q7)}\n")
        df = orig[(orig['age']>=30) & (orig['age']<=50)]
        f.write(f"Question 8: {df.equals(q8)}\n")
        df = orig['age'].sum()
        f.write(f"Question 9: {df.equals(q9)}\n")
        df = orig['age'].mean()
        f.write(f"Question 10: {df.equals(q10)}\n")
        df = orig['name'].count()
        f.write(f"Question 11: {df.equals(q11)}\n")
        df = orig.sort_values(by=['age','name'],ascending=[False,True])
        f.write(f"Question 12: {df.equals(q12)}\n")
        df = orig.assign(course='big data')
        f.write(f"Question 13: {df.equals(q13)}\n")
        df = orig.drop(columns='number_of_pets')
        f.write(f"Question 14: {df.equals(q14)}\n")
        df = orig.dropna()
        f.write(f"Question 15: {df.equals(q15)}\n\n")
