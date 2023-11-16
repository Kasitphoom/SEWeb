from class_module import *

a = Assignment("dff9328c-93ad-4b68-af6a-8934c809e5d0", "Assignment 1", 10, "2021-01-01")

a.summitWork(1100, ["test1", "test2"])
print(a.submitted_work[1100]["score"])

print(a.grading(1100, 10))

print(a.submitted_work[1100]["score"])